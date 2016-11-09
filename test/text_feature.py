'''
Created on Oct 21, 2016

@author: rsong_admin
'''
import re



def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


if __name__ == '__main__':
    if findWholeWord('good day')('today is a good day'):
        print 'Find'
    else:
        print 'No'
    

