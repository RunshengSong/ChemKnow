import urllib2, time, sys, getopt, json



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




if __name__ == '__main__':
	text = "exhaust gas from an internal combustion engine whose fuel includes nitromethane will contain nitric acid vapour, which is corrosive, and when inhaled causes a muscular reaction making it impossible to breathe."
	identifiedChem = identifyChem(text)
	for chem in identifiedChem:
		print chem
