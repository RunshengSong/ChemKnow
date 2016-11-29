'''
Created on Nov 15, 2016

@author: rsong_admin
'''

import sys
sys.path.append('../packages')

from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.wordnet import WordNetLemmatizer


if __name__ == '__main__':
    # test

    sen = 'Toluene hydrodealkylation converts toluene to benzene produced produce.'
    steammer = WordNetLemmatizer()
    
    sen_tok = sen.split(' ')
    sen_tok = [steammer.lemmatize(word) for word in sen_tok]
    
    print sen_tok