'''
Created on Nov 29, 2016

@author: rsong_admin
'''
from bs4 import BeautifulSoup
import requests
import csv
import re

class queryNIST:
    def __init__(self):
        pass
        
    def _get_url(self, cName):
        '''get the NIST chembook url with the chemical NAME you want serach'''
        cName.replace(" ","+")
        baseURL = 'http://webbook.nist.gov/cgi/cbook.cgi?Name=Acetone&Units=SI&cTG=on&cTC=on'
        thisURL =baseURL.replace('Acetone', cName)
        return thisURL
    
    def check_name(self, cName):
        cName = cName.lower().strip()
        thisURL = self._get_url(cName)
        this_page = requests.get(thisURL)
        this_text = this_page.text
        this_soup = BeautifulSoup(this_text, "lxml")
        thisFind_direct  = this_soup.find_all('a', title="IUPAC definition of empirical formula")
        thisFind_indrect = this_soup.find_all('ol')
        
        if thisFind_indrect:
            thisFind_indrect = thisFind_indrect[0].text.lower()
            thisFind_indrect = thisFind_indrect.splitlines()
        found_this = False

        for eachRes in thisFind_direct:
            thisContent = eachRes.text
            if thisContent == 'Formula':
                found_this = True
                return found_this
        
        for eachRes2 in thisFind_indrect:  
            eachRes2 = re.sub(r'\([^)]*\)', '', eachRes2)
            
            eachRes2 = str(eachRes2.strip())
            if eachRes2 == cName:
                found_this = True
                return found_this
        return found_this

if __name__ == '__main__':
    # test
    thisSearch = queryNIST()
    
    # return True if found chemical
    print thisSearch.check_name('sodium bisulfite')
    print thisSearch.check_name('isiii')
    print thisSearch.check_name('sodium bisulfite')
    print thisSearch.check_name('sodium bisulfite')
    print thisSearch.check_name('sodium bisulfite')
    print thisSearch.check_name('benzene')
    print thisSearch.check_name('sodium bisulfite')
    print thisSearch.check_name('sodium bisulfite')
    
    
    
    
    