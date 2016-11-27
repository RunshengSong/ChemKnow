'''
Created on Nov 21, 2016
package script to generate predictive models
@author: runshengsong
'''

import numpy as np
import pandas as pd

import generate_features as gf
import data_preparation as dp

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import cross_val_score
from sklearn.externals import joblib
import sklearn.metrics as metrics
from pygments.lexer import this

def create_random_forest_model(positive_file, negative_file):
    '''
    create the first predictive model
    '''
    x_trn, x_tst, y_trn, y_tst = gf.load_pos_neg_samples(positive_file, negative_file)
    trn_features, tst_features, vec = gf._create_bag_of_word_features(x_trn,x_tst)

    # try random forest
    clf = RandomForestClassifier(n_estimators=10)
    clf.fit(trn_features, y_trn)
    predicted = clf.predict(tst_features)
    print metrics.confusion_matrix(y_tst, predicted)
    print metrics.classification.accuracy_score(y_tst,predicted)
    return clf, vec

class CreateClassifier:
    def __init__(self, models, feature_methods):
        self.model = models
        self.vec = feature_methods
    
    def train(self,trn_feature, y_trn):
        self.model.fit(trn_feature, y_trn)
        print 'model trained'
    
    def score(self,tst_feature, y_tst):
        pred = self.model.predict(tst_feature)
        print metrics.confusion_matrix(y_tst, pred)
        print metrics.classification.accuracy_score(y_tst,pred)
    
    def fit_vec(self,trn_sen,tst_sen):
        self.vec.fit(trn_sen)
        trn_feature = self.vec.transform(trn_sen).toarray()
        tst_feature = self.vec.transform(tst_sen).toarray()
        return trn_feature, tst_feature
    
    def save_model(self, file_path):
        return joblib.dump(self,file_path, compress=True)
    
    @staticmethod
    def from_file(file_path):
        return joblib.load(file_path)

class ScoreSentence:
    def __init__(self, input_model, feature_generator):
        self.model = input_model
        self.feature_generator = feature_generator
    
    def score(self, input_sentence):
        '''
        classify if a sentence is true or false
        '''
        trimmed_sentence = dp.prepare_single_sentence(input_sentence)
        sentence_feature = self.feature_generator.transform(trimmed_sentence)
        return self.model.predict_proba(sentence_feature)[0]

if __name__ == '__main__':
    # test
    pos_file = '../data/trimmed_indentified_chemical_positive.csv'
    neg_file = '../data/trimmed_indentified_chemical_negative.csv'

    x_trn, x_tst, y_trn, y_tst = gf.load_pos_neg_samples(pos_file, neg_file, test_size=0.35)
    thisClf = CreateClassifier(RandomForestClassifier(n_estimators=10), CountVectorizer(ngram_range=(1,3)))
    trn_feature, tst_feature = thisClf.fit_vec(x_trn, x_tst)
    thisClf.train(trn_feature, y_trn)
    thisClf.score(tst_feature, y_tst)

    
    
    
    