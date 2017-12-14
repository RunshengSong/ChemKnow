#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Nov 27, 2016

@author: runshengsong
'''
import sys
from os import path
import os, csv
import re, traceback

from textblob import TextBlob

# append packages
current_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(current_dir_path)

from modeling_tools import *
from chemical_name_identifier.annotateChem import *

CURRENT_MODEL = path.join(current_dir_path, "models", 'random_forest_0_0_1128')

def _findWholeWord(w):
	'''
	if w in the sentence following this function
	'''
	return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

def run_predict_on_text(input_text, input_chemical_name, model=CURRENT_MODEL, find_chem_name=True):
	'''
	run prediction on input text file
	1) break text file into single sentence
	2) score each sentence (text transformation here) only if the chemical name in the sen
	3) if score == 1 and chemical name exist in the sentence return 
	index of chemical name in the sentence
	4) check the chemical name from the orig
	'''
	try:
		print model
		thisModel = ScoreSentence.load_model(model)
		input_text = input_text.decode('utf-8')
		zen = TextBlob(input_text)
		input_chemical_name = input_chemical_name.lower()
		identified_sen = []
		identified_chems = []
		for eachSen in zen.sentences:
			eachSen = eachSen.lower()
# 			print str(eachSen)
			# check if the chemical exist in this sentence, reduce the run time of chemspider
			word_in_this_sen = _findWholeWord(input_chemical_name)(str(eachSen))
			if word_in_this_sen:
				thisScore, thisNames = thisModel.score(eachSen, hide_chem_name = find_chem_name)
				if thisScore == 1 and word_in_this_sen:
					identified_sen.append(str(eachSen)) # append the sentence to outputs
					# append chemical name if it is not in the existing list:
					for eachName in thisNames:
						if eachName not in identified_chems:
							identified_chems.append(eachName)
				else:
					continue
			else:
				continue
		
		return identified_sen, identified_chems

	except Exception, e:
		traceback.print_exc()
		pass

def writeCSV(sentList, chemList):
	with open(os.path.join(current_dir_path, "theResult.csv"), 'wb') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		spamwriter.writerow(sentList)
		spamwriter.writerow(chemList)

if __name__ == '__main__':
# 	pass
	# test
#  	text = str(sys.argv[1])
#  	chemical = str(sys.argv[2])
#  	hideChemName = str(sys.argv[3])
# 	find_chem_name = str(sys.argv[2])
	# print text
	# print chemical
# 	if hideChemName == "True":
# 		hideChemName = True
# 	else:
# 		hideChemName = False
	# print hideChemName
	
	text = 'Toluene hydrodealkylation converts toluene to benzene. \
			In this hydrogen-intensive process, toluene is mixed with hydrogen, \
			then passed over a chromium, molybdenum, \
			or platinum oxide catalyst at 500–600 °C and 40–60 atm pressure.\
			Sometimes, higher temperatures are used instead of a catalyst (at the similar reaction condition).\
			In the 19th and early 20th centuries, benzene was used as an after-shave lotion because of its pleasant smell.\
			Trace amounts of benzene are found in petroleum and coal. '
 	
	# find_chem_name = True if you want to hide and detect chemical names
	this_sen, this_chems = run_predict_on_text(text, input_chemical_name="Benzene",
											   model = CURRENT_MODEL, 
											   find_chem_name=True)        
	print this_sen, this_chems
# 	writeCSV(this_sen, this_chems)

#     input_sentence = 'chem prepared commercially reaction chem gas acidic solid catalyst chem although impractical prepared reaction methyl'
#     
#     thisModel = ScoreSentence.load_model('../models/random_forest_0_0_1127')
#     print thisModel.score(input_sentence)


	
	