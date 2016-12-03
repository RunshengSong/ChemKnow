#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Nov 6, 2016

@author: runshengsong
'''

import pandas as pd
import nltk
import csv
import re
import wikipedia as wiki
from textblob import TextBlob
from random import shuffle
import data_preparation as dp


important_words = ['produced',
                   'manufactured',
                   'derivative',
                   'industrially']


def get_positive_sentence_for_chem_in_list(list_excel, output_file_name):
    '''
    This function get data for the chemical pair in the list
    Search sentence from wikipedia
    
    This is the function for the positive sentences
    '''
    
    df = pd.ExcelFile(list_excel,header=0).parse('Sheet1')
    
    count = 0
    this_results_positive = []

    with open(output_file_name,'wb') as myfile:
        thisWriter = csv.writer(myfile)
        for eachRows in df.iterrows():
            count += 1
            this_product = eachRows[1]['Product'].lower()
            this_rect = eachRows[1]['Reactant'].lower()
            
            
            try:
                this_page = wiki.WikipediaPage(this_product)
                raw_text = this_page.content
                
                zen = TextBlob(raw_text)
                for eachSentence in zen.sentences:
                    thisSentence = str(eachSentence).lower()
                    find_product = _findWholeWord(this_product)(thisSentence)
                    find_reactant = _findWholeWord(this_rect)(thisSentence)
                    
                    # if both products and reactant show up in the sentence
                    # this will be a positive sentence
                    if find_product and find_reactant:
                        this_results_positive.append(thisSentence)
                        print 'Positive Sample found for:', this_product,'...', count
     
            except (wiki.exceptions.PageError, wiki.exceptions.DisambiguationError):
                continue

            # write into file, positive
            thisWriter.writerow([this_product, this_rect]+this_results_positive)

def get_negative_sentence_for_chem_in_list(list_excel, output_file_name):     
    '''
    get negative sentence from wikipedia
    Rule: the chemical list show up in the sentence but the reactant must not showen up
    '''
    df = pd.ExcelFile(list_excel,header=0).parse('Sheet1')   
    count = 0
    this_results_negative = []   
    
    with open(output_file_name,'wb') as myfile:
        thisWriter = csv.writer(myfile)   
        for eachRows in df.iterrows():
            # for each chemical:
            
            count += 1
            this_product = eachRows[1]['Product'].lower()
            this_rect = eachRows[1]['Reactant'].lower() 
            try:
                this_page = wiki.WikipediaPage(this_product)
                raw_text = this_page.content
                
                zen = TextBlob(raw_text)
                for eachSentence in zen.sentences:
                    
                    thisSentence = str(eachSentence).lower()
                    thisSentence = dp._clean_up_wiki_sentence(thisSentence)
                    
                    find_product = _findWholeWord(this_product)(thisSentence)
                    find_reactant = _findWholeWord(this_rect)(thisSentence)
                    find_important_word = _check_important_word(thisSentence)
                  
                    # if the product name in the sentence, reactant name is not in the list
                    # and the imporatn word is not in the list
                    if find_product and not find_reactant and not find_important_word:
                        
                        print 'Negative Sample found for:', this_product,'...', count
                        this_results_negative.append(thisSentence)
                
                # shuffle the elements in the sentence
                # get rid of the bias of the structure of wiki
                shuffle(this_results_negative)
                
                # only get the first 10 sentences
                this_results_negative = this_results_negative[0:5]
                
            except (wiki.exceptions.PageError, wiki.exceptions.DisambiguationError):
                continue
            
            thisWriter.writerow([this_product, this_rect]+this_results_negative)
            
def _check_important_word(sentence):
    sentence = sentence.split()
    return any(word for word in important_words if word in sentence)
            
def _findWholeWord(w):
    '''
    if w in the sentence following this function
    '''
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

            
def _search_wiki_match_name(product_name, reactant_name):
    '''
    experiment
    '''
    product_name = product_name.lower()
    reactant_name = reactant_name.lower()
    
    this_page = wiki.WikipediaPage(product_name)
    
    raw_text = this_page.content
    zen = TextBlob(raw_text)
    for eachSentence in zen.sentences:
        thisSentence = str(eachSentence).lower()
        find_or_not = _findWholeWord(reactant_name)(thisSentence)
        if find_or_not:
            print thisSentence
            raw_input()
        else:
            print 'No'


def search_wiki(chemical_name):
    '''
    experiment
    '''
    chemical_name = chemical_name.lower()
    this_page = wiki.WikipediaPage(chemical_name)
    
    raw_text = this_page.content
    zen = TextBlob(raw_text)
    print zen

            
            
if __name__ == '__main__':
    # test
    
    list_excel = '../data/chemical_list.xlsx'
    output_name = '../data/raw_data/negative_sentence_wiki.csv'
    
    get_negative_sentence_for_chem_in_list(list_excel, output_name)            
        
        
    
    
    

            
    
        
            
       
        
 
        
        
        
        
        
