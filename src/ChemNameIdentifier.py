# -*- coding: utf-8 -*-
import urllib2, time, sys, getopt, json, csv
import multiprocessing as mp
from multiprocessing import Pool
import pandas as pd
import re



PubTator_username = ''


def identifyChem(text):
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
		print "Thanks for your submission. The session number is : "+ SessionNumber
		print "The request is received and processing....\n"
		#Receive
		url_Receive = "https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/" + SessionNumber + "/Receive/"
		
		code=404
		while(code == 404 or code == 501):
			time.sleep(5)
			try:
				urllib_result = urllib2.urlopen(url_Receive)
			except urllib2.HTTPError as e:
				code = e.code
			except urllib2.URLError as e:
				code = e.code
			else:
				code = urllib_result.getcode()

		# print urllib_result.read()
		responseJson = urllib_result.read()
		responseJson = json.loads(responseJson)
		return parseRespJson(responseJson, text)


def parseRespJson(respJson, text):
	denotations = respJson["denotations"]
	denotatedChemicals = []
	for denotation in denotations:
		chemicalName = text[int(denotation["span"]["begin"]):int(denotation["span"]["end"])]
		chemicalObj = denotation["obj"]
		chemicalType = chemicalObj[:chemicalObj.find(":")]
		chemicalID = chemicalObj[chemicalObj.find(":")+1:]
		denotatedChemicals.append([chemicalName, chemicalType, chemicalID])
	return denotatedChemicals


def identifyChem_wReplace(text, product, reactant):
	print "text:", text
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
		print "Thanks for your submission. The session number is : "+ SessionNumber
		print "The request is received and processing....\n"
		#Receive
		url_Receive = "https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/" + SessionNumber + "/Receive/"
		
		code=404
		while(code == 404 or code == 501):
			time.sleep(5)
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
				return [product, reactant, ""]
			else:
				responseJson = json.loads(responseJson)
				# print responseJson
				return parseRespJson_wReplace(responseJson, text, product, reactant)
		except:
			return [product, reactant, ""]



def parseRespJson_wReplace(respJson, text, product, reactant):
	if "denotations" in respJson:
		denotations = respJson["denotations"]
		denotatedChemicals = []
		for denotation in reversed(denotations):
			chemicalName = text[int(denotation["span"]["begin"]):int(denotation["span"]["end"])]
			# if chemicalName == product:
			# 	chemicalName = "CHEMICAL"
			# elif chemicalName == reactant:
			# 	chemicalName = "CHEMICAL"
			# else:
			# 	chemicalName = "CHEMICAL"
			chemicalName = "CHEMICAL"
			text = text[:int(denotation["span"]["begin"])] + chemicalName + text[int(denotation["span"]["end"]):]
			# chemicalObj = denotation["obj"]
			# chemicalType = chemicalObj[:chemicalObj.find(":")]
			# chemicalID = chemicalObj[chemicalObj.find(":")+1:]
		# print text
		# textList = text.split("|")
		denotatedChemicals = [product, reactant, text]
		return denotatedChemicals
	else:
		return [product, reactant, ""]


def readChemSent_csv(csvFile):
	chemSentList = []
	with open(csvFile, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		rowCounter = 0
		for row in spamreader:
			print row
			rowCounter += 1
			product = row[0]
			reactant = row[1]
			if len(row) == 3:
				sents = [row[2]]
			elif len(row) > 3:
				sents = row[2:]
			else:
				sents = []
			chemSentList.append([product, reactant, sents])
	print rowCounter, len(chemSentList)
	return chemSentList


def readChemSent(excelFile):
	df = pd.read_excel(excelFile, header=None)
	chemSentList = []
	rowCounter = 0
	for row in df.iterrows():
		rowCounter += 1
		product = row[1][0].strip()
		reactant = row[1][1].strip()
		sents = list(row[1][2:])
		validSents = []
		for sent in sents:
			if not pd.isnull(sent):
				sent = sent.encode('ascii', 'ignore')
				sent = re.sub("\n"," ", sent)
				sent = re.sub("\t"," ", sent)
				sent = re.sub("="," ", sent)
				sent = re.sub("\?"," ", sent)
				sent = re.sub(product+"s+", "CHEMICAL", sent)
				sent = re.sub(reactant+"s+", "CHEMICAL", sent)
				sent = re.sub("\s+"," ", sent)
				validSents.append(sent)
			else:
				break
		# print product, reactant
		# print validSents
		chemSentList.append([product, reactant, validSents])
	print rowCounter, len(chemSentList)
	return chemSentList





# def readChemSent_Aggregate(csvFile):
# 	chemSentList = readChemSent(csvFile)
# 	chemSentListR = []
# 	for chemSent in chemSentList:
# 		product = chemSent[0]
# 		reactant = chemSent[1]
# 		sents = chemSent[2]
# 		sentToFeed = ""
# 		if len(sents) == 1:
# 			sentToFeed = sents[0]
# 		elif len(sents) > 1:
# 			for sent in sents:
# 				if sent!="":
# 					sentToFeed += sent + " | "
# 			sentToFeed = sentToFeed[:-3]
# 		chemSentListR.append([product, reactant, sentToFeed])
# 	return chemSentListR


def identifyChem_FromChemSentList(chemSent):
	identifiedTextList = []
	# print len(chemSent[2]), chemSent[2]
	identifiedChemList = []
	for sent in chemSent[2]:
		if(len(sent)<1):
			print "break"
			break
		identifiedChemList = identifyChem_wReplace(sent, chemSent[0], chemSent[1])	# [product, reactant, ""]
		if len(identifiedChemList[2]) ==  0:
			# write un-annotated sents
			listToWrite = [chemSent[0], chemSent[1], sent]
			with open("/home/yiting/Dropbox/Fall2016/CS273/project/data/unidentified_chemical_positive_cleanup1.csv", 'a') as csvfile:
				spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				# print listToWrite
				spamwriter.writerow(listToWrite)
		else:
			identifiedTextList.append(identifiedChemList[2])
	if len(identifiedChemList) > 2:
		listToWrite = [identifiedChemList[0], identifiedChemList[1]]
		listToWrite += identifiedTextList
		print listToWrite
		with open("/home/yiting/Dropbox/Fall2016/CS273/project/data/identified_chemical_positive_cleanup1.csv", 'a') as csvfile:
			spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			# print listToWrite
			spamwriter.writerow(listToWrite)



def multi_ident():
	chemSentList = readChemSent("/home/yiting/Dropbox/Fall2016/CS273/project/data/positive_cleanup.xlsx")
	# pool = mp.Pool(processes=4)
	print "start multiprocessing..."
	# for chemSent in chemSentList:
	# 	print chemSent
	# 	pool.apply_async(identifyChem_FromChemSentList, args=(chemSent, "/home/yiting/Dropbox/Fall2016/CS273/project/data/identified_chemical_positive_cleanup.csv")) 

	pool = Pool(processes = 8)
	pool.map(identifyChem_FromChemSentList, chemSentList)

	# for chemSent in chemSentList[17:20]:
	# 	identifyChem_FromChemSentList(chemSent)

def cleanText(text):
	pass



if __name__ == '__main__':
	# text = "exhaust gas from an internal combustion engine whose fuel includes nitromethane will contain nitric acid vapour, which is corrosive, and when inhaled causes a muscular reaction making it impossible to breathe."
	# identifiedChem = identifyChem(text)
	# for chem in identifiedChem:
	# 	print chem

	multi_ident()

	# identifyChem_FromChemSentList(["trichloroethylene", "1,1,2,2-tetrachloroethane", ["2-butanol is manufactured industrially by the hydration of 1-butene or 2-butene:sulfuric acid is used as a catalyst for this conversion."]])


	# chemSentList = readChemSent("/home/yiting/Dropbox/Fall2016/CS273/project/data/positive_cleanup.xlsx")
	# for chemSent in chemSentList[:5]:
	# 	print chemSent
