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


def get_sentence_for_chem_in_list(list_excel, output_name):
    
    df = pd.ExcelFile(list_excel,header=0).parse('Sheet1')
    
    count = 0
    
    with open(output_name,'wb') as myfile:
        thisWriter = csv.writer(myfile)
        for eachRows in df.iterrows():
            count += 1
            this_product = eachRows[1]['Product'].lower()
            this_rect = eachRows[1]['Reactant'].lower()
            this_results = []
            
            try:
                this_page = wiki.WikipediaPage(this_product)
                raw_text = this_page.content
                
                zen = TextBlob(raw_text)
                for eachSentence in zen.sentences:
                    thisSentence = str(eachSentence).lower()
                    find_product = findWholeWord(this_product)(thisSentence)
                    find_reactant = findWholeWord(this_rect)(thisSentence)
                    
                    if find_product and find_reactant:
                        this_results.append(thisSentence)
                        print 'Sample found for:', this_product,'...', count
     
            except (wiki.exceptions.PageError, wiki.exceptions.DisambiguationError):
                continue

            # write into file
            thisWriter.writerow([this_product, this_rect]+this_results)

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

            
def search_wiki_match_name(chemical_name):
    '''
    experiment
    '''
    chemical_name = chemical_name.lower()
    this_page = wiki.WikipediaPage(chemical_name)
    
    raw_text = this_page.content
    zen = TextBlob(raw_text)
    for eachSentence in zen.sentences:
        thisSentence = str(eachSentence).lower()
        find_or_not = findWholeWord(chemical_name)(thisSentence)
        if find_or_not:
            print thisSentence
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
    list_excel = 'chemical_list.xlsx'
    output_name = 'positive_sentence_wiki.csv'
    
#     get_sentence_for_chem_in_list(list_excel, output_name)
    search_wiki('ethylenediamine tetraacetic acid')
           
                
        
        
    
    
    

            
    
        
            
       
        
 
        
        
        
        
        
