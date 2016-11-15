'''
Created on Nov 9, 2016

clean up the downloaded data from wiki pedia
@author: rsong_admin
'''
import csv


def remove_equation(sentence):
    '''
    remove the chemical reactaion equation from the sentence
    '''
    sentence_list = sentence.splitlines() # split the sentence by lines
    
    
    # remove the title line from the sentence
    for eachLine in sentence_list:
        if eachLine.startswith('==') and eachLine.endswith('=='):
            sentence_list.remove(eachLine)
    
    # remove the chemical reaction equation from the sentence
    for eachLine in sentence_list:
        if '???' in eachLine and '+' in eachLine:
            sentence_list.remove(eachLine)
        
    return ' '.join(sentence_list)
    

if __name__ == '__main__':
    with open('./data/positive_sentence_wiki.csv','rb') as myReadfile:
        with open('./data/sentence_cleanup.csv','wb') as myWriterfile:
            
            thisReader = csv.reader(myReadfile)
            thisWriter = csv.writer(myWriterfile)
            count = 0
            for eachRow in thisReader:
                thisResults = []
                count += 1
                if count >= 2: # skip the first line
                    thisProd = eachRow[0]
                    thisReact = eachRow[1]
                    thisResults.append(thisProd)
                    thisResults.append(thisReact)
                    
                    allSentence = eachRow[2:] # only dealing with the first sentence for now
                    for thisSentence in allSentence:
                        if thisSentence:
                            thisSentence = remove_equation(thisSentence) # remove equation and title line if exist
                            thisResults.append(thisSentence)
                        else:
                            break
            
                thisWriter.writerow(thisResults)
                
              
                

        
        
        
        
                
                
               
                