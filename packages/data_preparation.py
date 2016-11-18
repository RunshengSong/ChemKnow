'''
Created on Nov 17, 2016

@author: rsong_admin
'''
import csv
from nltk.corpus import stopwords

import csv
import re
import pandas as pd
import numpy as np
import nltk
import string
from nltk.corpus import wordnet

def _remove_plural(sentence, product, reactant):
    '''
    use lancaster stemmer to remove tense and plural from a sentece
    '''
    st = nltk.PorterStemmer()
    sentence = sentence.split()
    sentence = " ".join(st.stem(word) for word in sentence)
    print sentence

def _has_number(a_word):
    '''
    check if a word has a number in it,
    if so this might be a chemical formula
    '''
    return bool(re.search(r'\d', a_word))
   
def _replace_chem_name(sentence, product, reactant=None):
    '''
    function to handle the case when product or reactant is in one of the other
    e.g. product: sodium; reactant: sodium hydroxide
    
    also need to deal with the pluarl form of chemical names 
    '''
    
#     product = product.strip()
#     reactant = reactant.strip()
#     
#     # deal with negative samples, only replace products
#     if reactant is None:
#         sentence = re.sub(product+'s?', 'chem', sentence)
#         
#     elif product not in reactant and reactant not in product:
#         # if products and reactants are exclusive
#         sentence = re.sub(product+'s?', 'chem', sentence)
#         sentence = re.sub(reactant+'s?','chem', sentence)
#     elif product in reactant:
#         # order matters now
#         sentence = re.sub(reactant+'s?', 'chem', sentence)
#         sentence = re.sub(product+'s?','chem', sentence)
#     elif reactant in product:
#         # order matters 
#         sentence = re.sub(product+'s?', 'chem', sentence)
#         sentence = re.sub(reactant+'s?','chem', sentence)
# 
#     return sentence
    
    # stop using this function for data generation
    # use Yiting's API to deal with all positive and negative
    return sentence

def _clean_up_wiki_sentence(input_sentence):
    '''
    FUNCTION for WIKI
    
    clean up the equations in each sentence in the input files
    write the results in the output_file
    
    1. remove equations by lines
    2. remove title
    3. 
    
    '''
    sentence_list = input_sentence.splitlines() # split the sentence by lines

    for eachLine in sentence_list:
        # remove the title line from the sentence
        if eachLine.startswith('==') and eachLine.endswith('=='):
            sentence_list.remove(eachLine)
        # remove the chemical reaction equation from the sentence
        if '???' in eachLine and '+' in eachLine:
            sentence_list.remove(eachLine)
        
    return ' '.join(sentence_list)  

def _clean_up_sentence(input_sentence):
    pass

def _trimming(token_sentence, buffer=5):
    '''
    take the sentence between the first and last occurance of 'chem'
    plus buffer
    '''
    first_idx = 0
    last_idx = len(token_sentence)
    for idx, eachWord in enumerate(token_sentence):
        if eachWord == 'chem':
            first_idx = idx
            break
    
    for idx, eachWord in enumerate(reversed(token_sentence)):
        if eachWord == 'chem':
            last_idx = len(token_sentence) - idx - 1
            
    first_idx = max(0, first_idx - buffer)
    last_idx = min(last_idx + buffer, len(token_sentence))
    
    token_sentence = token_sentence[first_idx: last_idx] # trimming here
    return token_sentence
        
def _tokenize_sentence(input_sentence, buffer=5):
    '''
    tokenize the sentence, with input buffer
    remove stop words and digits
    
    Also stem the tokenized sentence
    '''

    # remove punctunation
    input_sentence = " ".join("".join([" " if ch in string.punctuation else ch for ch in input_sentence]).split()) 
    
    token_sentence = nltk.word_tokenize(input_sentence) # tokenize the sentence
    
    # convert each element to string
    token_sentence = map(str, token_sentence) 
    
    
    # remove stop words
    token_sentence = [word for word in token_sentence if word not in stopwords.words('english')]
    
    # remove digits
    token_sentence = [word for word in token_sentence if not _has_number(word)]
               
    # remove len < 3
    token_sentence = [word for word in token_sentence if not len(word)<3]

        # remove chemical formula here

    # trim sentence, get only the part between the first and the last occurance of 'chem'
#     token_sentence = _trimming(token_sentence,buffer = buffer)
        
    return token_sentence
    
def trim_positive_sentence(df, buffer=10):
    '''
    this function trim the sentence to only get the words between each pair
    plus few words before and after each pair (depends on the buffer)
    
    return a list of trimmed sentence regardless the product and reatancts
    '''
    trimmed_sentence = []
    for eachRow in df.iterrows():
        this_product = eachRow[1][0].strip()
        this_reactant = eachRow[1][1].strip()
        all_sentences = eachRow[1][2:]
        for eachSentence in all_sentences:
            if not pd.isnull(eachSentence): # check if a cell in pandas is not nan
                eachSentence = eachSentence.encode('ascii','ignore')

                # check if each sentence contains both the reactants and products
                if this_product in eachSentence and this_reactant in eachSentence:
                    
                    eachSentence = _replace_chem_name(eachSentence, this_product, this_reactant)
                    print this_product, this_reactant
                    print eachSentence
                    eachSentence = _tokenize_sentence(eachSentence, buffer=buffer)
                    trimmed_sentence.append(eachSentence)
                else:
                    # if the sentence does not have both product and reactants
                    continue
            else:
                # break for null sentence, indicating the end of this line
                break
    return trimmed_sentence

def trim_negative_sentence(df, buffer=10):
    '''
    this function trim the sentence to only get the words between each pair
    plus few words before and after each pair (depends on the buffer)
    
    return a list of chemicals
    '''
    trimmed_sentence = []
    count = 0
    for eachRow in df.iterrows():
        count +=1
        this_product = eachRow[1][0].strip()
        this_reactant = eachRow[1][1].strip()
        all_sentences = eachRow[1][2:]
        print count
        
        for eachSentence in all_sentences:
            if not pd.isnull(eachSentence): # check if a cell in pandas is not nan

#                 eachSentence = eachSentence.encode('ascii','ignore')

                # check if each sentence contains both the reactants and products
                if this_product in eachSentence:
                    eachSentence = _replace_chem_name(eachSentence, this_product)

                    eachSentence = _tokenize_sentence(eachSentence, buffer=buffer)
                    eachSentence = ' '.join(eachSentence)
                    trimmed_sentence.append(eachSentence)
                else:
                    # if the sentence does not have both product and reactants
                    continue
            else:
                # break for null sentence, indicating the end of this line
                break
    return trimmed_sentence


if __name__ == '__main__':
    # test
    df = pd.read_csv('../data/raw_data/negative_sentence_wiki.csv',header=0)
    trimmed_negative = trim_negative_sentence(df)
    
    with open('negative_sentence_trimmed.csv','wb') as myfile:
        thisWriter = csv.writer(myfile)
        for eachSen in trimmed_negative:
            thisWriter.writerow([eachSen])
    

    

