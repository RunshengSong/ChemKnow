# coding=utf-8
'''
Created on Nov 9, 2016

@author: yiting
'''

import csv, json, os, requests, re
import traceback
import logging
import pprint
from bs4 import BeautifulSoup
from segtok.segmenter import split_single, split_multi

from bingSearch import Bing_search_cog_API
from nltk.tokenize import sent_tokenize
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



DATA_FOLDER_PATH = "/home/yiting/Dropbox/Fall2016/CS273/project/data"





def getChemicalsNReactors(chemicalListCSV):
	chemicalNameList = []
	reactorNameList = []
	with open(chemicalListCSV, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		rowCounter = 0
		for row in spamreader:
			rowCounter += 1
			if rowCounter > 1:
				chemicalName = row[1]
				reactorName = row[23]
				chemicalNameList.append(chemicalName)
				reactorNameList.append(reactorName)
	return chemicalNameList, reactorNameList


"""
	scrape web contents of a webpage
	  return with a list of text sentences
"""
def scrapeWebContent(url):
	s = requests.Session()
	s.headers['User-Agent'] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36"

	try:
		r = s.get(url, timeout=20)
		r.raise_for_status()
		text = BeautifulSoup(r.text, 'lxml')
		for script in text(["script", "style"]):
			script.extract()    # rip it out
		
		soup_text = text.get_text(" ", strip=True)	# get rid of script and style, and join text with '|''
		# soup_text = ".".join(soup_text.split("|"))
		soup_text = re.sub('\s+', ' ', soup_text)
		soup_text = soup_text.lower()
		sentences = textToSent(soup_text)
		# for sentence in sentences:
		# 	print sentence
		return sentences

	except requests.exceptions.ReadTimeout:
		print('\nServer not available. Skipped %s\n' % url)
		return []
	except Exception as e:
		logging.error(traceback.format_exc())
		return []

def textToSent(text):
	sents = []
	sents1 = sent_tokenize(text)
	sents2 = split_single(text)
	sents3 = split_multi(text)
	sents = sents + list(sents1) + list(sents2) + list(sents3)
	sents = list(set(sents))
	sentsToReturn = []
	for sentA in sents:
		sentAInlcude = False
		for sentB in sents:
			if sentB != sentA and sentB in sentA:
				sentAInlcude = True
				break
		if sentAInlcude == False:
			sentsToReturn.append(sentA)
	return sentsToReturn


def filterSent(sentList, chem1, chem2):
	filteredSentList = []
	for sent in sentList:
		if chem1 in sent and chem2 in sent and len(sent) <= 500:
			filteredSentList.append(sent)
	return filteredSentList


def writeToCSVAppend(chem1, chem2, sentList, csvFilePath):
	with open(csvFilePath, 'a') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		print [chem1, chem2]+sentList
		spamwriter.writerow([chem1, chem2]+sentList)


def getReactionSentsFromBingNWrite():
	chemicalListCSV = os.path.join(DATA_FOLDER_PATH, "chemical_list.csv")
	chemicalList, reactorList = getChemicalsNReactors(chemicalListCSV)
	for i in range(len(chemicalList))[:]:
		chem = chemicalList[i]
		reactor = reactorList[i]
		bingQuery = Bing_search_cog_API(str(chem) + " " + str(reactor))
		urlList = bingQuery.getWebpagesURLs()
		sentListToWrite = []
		if len(urlList) > 0:
			for url in urlList:
				htmlContentInSents = scrapeWebContent(url)
				if len(htmlContentInSents) <= 1:
					continue
				sentList = filterSent(htmlContentInSents, chem, reactor)
				sentListToWrite += sentList
			writeToCSVAppend(chem, reactor, sentListToWrite, os.path.join(DATA_FOLDER_PATH, "reaction_Sents2.csv"))
			print i, len(sentListToWrite)
			# if i == 800:
			# 	break
		else:
			writeToCSVAppend(chem, reactor, [], os.path.join(DATA_FOLDER_PATH, "reaction_Sents2.csv"))
			print i, 0




if __name__ == '__main__':

	getReactionSentsFromBingNWrite()
