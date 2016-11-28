# -*- coding: utf-8 -*-
from chemspipy import ChemSpider
from pyjarowinkler import distance
import urllib2, time, sys, getopt, json, csv
import multiprocessing as mp
from multiprocessing import Pool


CS_TOKEN = "c751f22b-9f36-4830-a66c-cc6f50da6bd5"


class annotateChem:
	def __init__(self):
		# print "in class"
		self.cs = ChemSpider(CS_TOKEN)


	"""
		Annotate the searchText. 
		  Return 1 if it is a chemical name; otherwise, return 0
	"""
	def annotate(self, searchText):
		resultList = self.cs.search(searchText)
		match = 0
		if len(resultList) >= 3:
			resultList = resultList[:3]
		for result in resultList:
			resultChemName = result.common_name.lower().strip().encode('ascii', 'ignore')
			originalChemName = searchText.lower().strip().encode('ascii', 'ignore')
			# print resultChemName, originalChemName, levenshtein(resultChemName, originalChemName), levenshtein(originalChemName, resultChemName), distance.get_jaro_distance(resultChemName, originalChemName, winkler=True, scaling=0.1), distance.get_jaro_distance(originalChemName, resultChemName, winkler=True, scaling=0.1)
			if result.common_name.lower().strip() == searchText.lower().strip() or \
					distance.get_jaro_distance(resultChemName, originalChemName, winkler=True, scaling=0.1) >= 0.8:
				match = 1
		return match
	

	"""
		Annotate the sent 
		  Return a list of strings with identified chemicals replaced by "chem"
	"""
	def annotateSent(self, listOfString):
		annotatedSent = []
		identifiedChemSet = set()
		for string in listOfString:
			if self.annotate(string) == 1:
				annotatedSent.append("chem")
				identifiedChemSet.add(string.lower().strip())
			else:
				annotatedSent.append(string.lower().strip())
		return annotatedSent, list(identifiedChemSet)


# Christopher P. Matthews
# christophermatthews1985@gmail.com
# Sacramento, CA, USA
def levenshtein(s, t):
	''' From Wikipedia article; Iterative with two matrix rows. '''
	if s == t: return 0
	elif len(s) == 0: return len(t)
	elif len(t) == 0: return len(s)
	v0 = [None] * (len(t) + 1)
	v1 = [None] * (len(t) + 1)
	for i in range(len(v0)):
		v0[i] = i
	for i in range(len(s)):
		v1[0] = i + 1
		for j in range(len(t)):
			cost = 0 if s[i] == t[j] else 1
			v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
		for j in range(len(v0)):
			v0[j] = v1[j]
			
	return v1[len(t)]


def identifyChem_wReplace(text):
	PubTator_username = ''
	# print "text:", text
	trigger = "tmChem"

	#Submit

	url_Submit = "https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/" + trigger + "/Submit/"

	InputSTR = '{"sourcedb":"PubMed","sourceid":"25421723","text":"' + text + '"}'

	urllib_submit = urllib2.urlopen(url_Submit, InputSTR)
	urllib_result = urllib2.urlopen(url_Submit, InputSTR)
	SessionNumber = urllib_submit.read()

	if PubTator_username != '':
		print "Thanks for your submission (Session number: " + SessionNumber + ").\nThe result will be sent to your E-mail: " + email + ".\n"
	else:
		# print "Thanks for your submission. The session number is : "+ SessionNumber
		# print "The request is received and processing....\n"
		#Receive
		url_Receive = "https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/" + SessionNumber + "/Receive/"
		
		code=404
		while(code == 404 or code == 501):
			time.sleep(3)
			try:
				urllib_result = urllib2.urlopen(url_Receive)
			except urllib2.HTTPError as e:
				code = e.code
			except urllib2.URLError as e:
				code = e.code
			else:
				code = urllib_result.getcode()

		try:
			responseJson = urllib_result.read()
			# print responseJson
			if responseJson == "" or len(responseJson) < 1:
				return "", []
			else:
				responseJson = json.loads(responseJson)
				# print responseJson
				return parseRespJson_wReplace(responseJson, text)
		except:
			return "", []


def parseRespJson_wReplace(respJson, text):
	identifiedChemSet = set()
	if "denotations" in respJson:
		denotations = respJson["denotations"]
		denotatedChemicals = []
		for denotation in reversed(denotations):
			chemicalName = text[int(denotation["span"]["begin"]):int(denotation["span"]["end"])]
			identifiedChemSet.add(chemicalName.lower().strip())
			# if chemicalName == product:
			# 	chemicalName = "CHEMICAL"
			# elif chemicalName == reactant:
			# 	chemicalName = "CHEMICAL"
			# else:
			# 	chemicalName = "CHEMICAL"
			chemicalName = "chem"
			text = text[:int(denotation["span"]["begin"])] + chemicalName + text[int(denotation["span"]["end"]):]
			# chemicalObj = denotation["obj"]
			# chemicalType = chemicalObj[:chemicalObj.find(":")]
			# chemicalID = chemicalObj[chemicalObj.find(":")+1:]
		# print text
		# textList = text.split("|")
		denotatedChemicals = text
		return denotatedChemicals, list(identifiedChemSet)
	else:
		return "", []


if __name__ == "__main__":
	sent = "butanol manufactured industrially hydration butene butene sulfuric acid used catalyst convension"

	"""
		script to call ChemSpider to annotate a sentence (a list of words in the sentence)
		  return with a list of words of this sentence with chemical names replaced with "chem"
	"""
	# sentList = sent.split(" ")
	# ac = annotateChem()
	# annotatedSentList, chemicals = ac.annotateSent(sentList)
	# print " ".join(annotatedSentList)
	# print chemicals


	"""
		script to call tmChem to annotate a sentence (a list of words in the sentence)
		  return with a list of words of this sentence with chemical names replaced with "chem"
	"""
	annotatedSent, chemicals = identifyChem_wReplace(sent)
	annotatedSentList = annotatedSent.split(' ')
	print " ".join(annotatedSentList)
	print chemicals
