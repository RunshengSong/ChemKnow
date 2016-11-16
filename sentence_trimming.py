'''
Created on Nov 14, 2016
preprocessing of the positive and negative sentences

@author: rsong_admin
'''

import pandas as pd
import numpy as np
import nltk
import string


def _tokenize_sentence(input_sentence, buffer=5):
    '''
    tokenize the sentence, with input buffer
    remove stop words and digits
    '''
    input_sentence = " ".join("".join([" " if ch in string.punctuation else ch for ch in input_sentence]).split()) # remove punctuation
    
    token_sentence = nltk.word_tokenize(input_sentence) # tokenize the sentence
    
    first_index = max(0, min(token_sentence.index("CHEMICAL1") - buffer, token_sentence.index("CHEMICAL2") - buffer)) # take the index of the first appearance of the product or reactant, whichever come first, minus the buffer
    last_index = min(len(token_sentence), max(token_sentence.index("CHEMICAL2") + buffer, token_sentence.index("CHEMICAL1") + buffer)) # the same logic as the one above
    
    output_sentence = token_sentence[first_index: last_index] # trimming here
    

def trim_sentence(df, buffer=5):
    '''
    this function trim the sentence to only get the words between each pair
    plus few words before and after each pair (depends on the buffer)
    '''
    for eachRow in df.iterrows():
        this_product = eachRow[1][0]
        this_reactant = eachRow[1][1]
        all_sentences = eachRow[1][2:]
        for eachSentence in all_sentences:
            if not pd.isnull(eachSentence): # check if a cell in pandas is not nan
                eachSentence = eachSentence.encode('ascii','ignore')
                
                eachSentence = eachSentence.replace(this_product,'CHEMICAL1') # replace the actual chemical name with chemical 1 and chemical 2
                eachSentence = eachSentence.replace(this_reactant,'CHEMICAL2') 
                
                ''' still need to replace other chemical names by CHEMICALOTHER '''
                
                _tokenize_sentence(eachSentence, buffer=5)
                
                raw_input()
    
    



if __name__ == '__main__':
#     df = pd.read_excel('./data/positive_cleanup.xlsx',header=None)
#     trim_sentence(df)
    from nltk.corpus import stopwords
    cachedStopWords = stopwords.words("english")
    
    print cachedStopWords
    
    
    
    
    