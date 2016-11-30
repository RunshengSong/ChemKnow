#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Nov 15, 2016

@author: rsong_admin
'''

import QueryFromNIST as qNT
import csv


if __name__ == '__main__':
    # test
    
    file_path = '../data/old_data/positive_sentence_trimmed.csv'
    output_file = '../data/old_data/identified_positive_sentence_trimmed_NIST_test.csv'
    thisNIST = qNT.queryNIST()

    with open(output_file, 'wb') as myoutput:
        thisWriter = csv.writer(myoutput)
        with open(file_path, 'rb') as myfile:
            thisReader = csv.reader(myfile)
            for eachSen in thisReader:
                output_sen = []
                token_sen = eachSen[0].split(' ')
                for eachWord in token_sen:
                    eachWord.decode('utf-8')
                    print 'check NIST...'
                    is_chem = thisNIST.check_name(eachWord)
                    if is_chem:
                        output_sen.append('chem')
                    else:
                        output_sen.append(eachWord)
                
                output_sen = " ".join(output_sen)
                thisWriter.writerow([output_sen])
            
                    