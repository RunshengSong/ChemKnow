#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Nov 27, 2016

@author: runshengsong
'''
import sys
from os import path
import re

from textblob import TextBlob

# append packages
current_dir_path = path.dirname(path.realpath(__file__))
sys.path.append(path.join(path.dirname(current_dir_path),"packages"))

from modeling_tools import ScoreSentence

current_model = '../models/random_forest_0_0_1127'

def _findWholeWord(w):
    '''
    if w in the sentence following this function
    '''
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

def run_predict_on_text(input_text, input_chemical_name ,model=current_model):
    '''
    run prediction on input text file
    1) break text file into single sentence
    2) score each sentence (text transformation here)
    3) if score == 1 and chemical name exist in the sentence return 
    index of chemical name in the sentence
    4) check the chemical name from the orig
    '''
    thisModel = ScoreSentence.load_model(current_model)
    input_text = input_text.decode('utf-8')
    zen = TextBlob(input_text)
    for eachSen in zen.sentences:
        thisScore = thisModel.score(eachSen)
        word_in_this_sen = _findWholeWord(input_chemical_name)(str(eachSen))
        if thisScore == 1 and word_in_this_sen:
            return eachSen
        else:
            continue

if __name__ == '__main__':
    # test
    
    text = 'Toluene hydrodealkylation converts toluene to benzene. \
            In this hydrogen-intensive process, toluene is mixed with hydrogen, \
            then passed over a chromium, molybdenum, \
            or platinum oxide catalyst at 500–600 °C and 40–60 atm pressure.\
            Sometimes, higher temperatures are used instead of a catalyst (at the similar reaction condition).\
            In the 19th and early 20th centuries, benzene was used as an after-shave lotion because of its pleasant smell.\
            Trace amounts of benzene are found in petroleum and coal. '
    
    print run_predict_on_text(text,input_chemical_name='benzene')        
#     input_sentence = 'chem prepared commercially reaction chem gas acidic solid catalyst chem although impractical prepared reaction methyl'
#     
#     thisModel = ScoreSentence.load_model('../models/random_forest_0_0_1127')
#     print thisModel.score(input_sentence)