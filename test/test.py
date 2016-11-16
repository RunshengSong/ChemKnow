'''
Created on Nov 15, 2016

@author: rsong_admin
'''
import nltk
import re


sentence = 'important epoxy resins are produced from combining epichlorohydrin and bisphenol a to give bisphenol a diglycidyl ethers.'
words = 'epoxy resin'

this_match = re.sub('epoxy resins?','CHEMICAL1',sentence)
print this_match