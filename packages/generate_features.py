'''
Created on Nov 17, 2016

@author: rsong_admin
'''

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cross_validation import train_test_split

import csv
import numpy as np


DEFAULT_BOW_NGRAM_RANGE = (1,1)
DEFAULT_BOW_MAX_FEATURES = None
DEFAULT_BOW_BINARY = True
# ENTITY_REGEX = re.compile(r"GGVARENTTY[0-9]+GG|MMVARENTTY[0-9]+MM", re.IGNORECASE)

def load_pos_neg_samples(pos_file, neg_file, test_size=0.25):
    '''
    testing script
    load the temp. positive and negative files
    '''
    samples = []
    labels = []
    
    # load positive samples
    with open(pos_file,'rb') as myfile:
        thisReader = csv.reader(myfile)
        for eachLine in thisReader:
            eachLine = " ".join(eachLine)
            samples.append(eachLine)
            labels.append(1)
    
    # load negative samples        
    with open(neg_file,'rb') as myfile:
        thisReader = csv.reader(myfile)
        for eachLine in thisReader:
            eachLine = " ".join(eachLine)
            samples.append(eachLine)
            labels.append(0)
    
    # split the training and testing dataset
    x_train, x_test, y_train, y_test = train_test_split(samples, labels, test_size=test_size)
    return x_train, x_test, y_train, y_test
    
def _create_bag_of_word_features(trn_samples, tst_samples, ngram_range = DEFAULT_BOW_NGRAM_RANGE,
                       max_features=DEFAULT_BOW_MAX_FEATURES ,binary=DEFAULT_BOW_BINARY):
    '''
    convert both training samples and test samples to bag of word vectors
    '''
    # input samples should have been handle already
    vec = CountVectorizer(analyzer='word',
                          tokenizer=None,
                          preprocessor=None,
                          stop_words=None,
                          max_features=max_features,
                          binary= binary,
                          ngram_range=ngram_range)
    
    trn_data_features = vec.fit_transform(trn_samples).toarray()
    tst_data_features = vec.transform(tst_samples).toarray()
    
    return trn_data_features, tst_data_features, vec


    
   
if __name__ == '__main__':
    # test
    pass
    
   
    
    
    