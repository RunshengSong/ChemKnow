# -*- encoding: utf-8 -*-
'''
Created on Dec 10, 2017

search the reactant information for a given chemical name
from multiply sources

@author: runsheng
'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import sys, os
import wikipedia as wiki
from textblob import TextBlob
from packages import txt2ChemReaction

current_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(current_dir_path)

from packages.modeling_tools import *
from packages.txt2ChemReaction import *

CURRENT_MODEL = path.join(current_dir_path, "models", 'random_forest_0_0_1128')

class search_reactants():
    def __init__(self):
        self.thisModel = ScoreSentence.load_model(CURRENT_MODEL)
    
    def search_wiki(self, prod_chem_name, find_chem_name=True):
        """
        search the reactant information from wikipedia
        for prod_chem_name
        """
        print "searching from wiki..."
        product_name = prod_chem_name.lower()        
        this_page = wiki.WikipediaPage(product_name)
        raw_text = this_page.content
        identified_sent, identified_chems = self.search_raw_text(raw_text, product_name, find_chem_name)
        return identified_sent, identified_chems
        
    def search_raw_text(self, raw_text, product_name, find_chem_name=True):
        """
        search from raw text
        """
        zen = TextBlob(raw_text)
        identified_sent = []
        identified_chems = set()
        for eachSen in zen.sentences:
            eachSen = eachSen.lower()
            word_in_this_sen = self.__findWholeWord(product_name)(str(eachSen))
            if word_in_this_sen:
                is_related_sent, chemicals_in_this_sent = self.search_in_single_sentence(eachSen, find_chem_name)
                if is_related_sent:
                    identified_sent.append(eachSen)
                    for each_chem in chemicals_in_this_sent:
                        identified_chems.add(each_chem)
            else:
                continue
        return identified_sent, list(identified_chems)
    
    def search_in_single_sentence(self, sent, find_chem_name=True):
        """
        score and find chemical name in a single sentence
        """
        try:
            thisScore, this_names = self.thisModel.score(sent, hide_chem_name = find_chem_name)
        except UnicodeDecodeError:
            return 0, []
        return thisScore, this_names
        
    def __findWholeWord(self, w):
        '''
        if w in the sentence following this function
        '''
        return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search
    
if __name__ == '__main__':
    # test
#     sent = 'In 1836, the French chemist Auguste Laurent named the substance "phène"; \
#     [17] this word has become the root of the English word "phenol", which is hydroxylated benzene, \
#     and "phenyl", the radical formed by abstraction of a hydrogen atom (free radical H•) from benzene.'

#      
    this_search = search_reactants()
    sentence, chemicals = this_search.search_wiki("benzene", True)
#     this_search.search_in_single_sentence(sent, True)
#     
    print sentence
    print chemicals
            