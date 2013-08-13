'''
1. extract_pure_text_form_xml.py

--> remove all the xml tags from original files, leave only sentences in the form "word1_tag1  word2_tag2...."

code to process CTB-5 corpus. of "Mana" project

'''

import os
import re
import codecs
import sys


def match_pattern(x):
    p=re.compile(r"<DOC>")
    p2=re.compile(r"</DOC")
    
    p_docid=re.compile('<DOCID>\S+</DOCID>')
    p_header=re.compile(r'<HEADER>.*</HEADER>', re.DOTALL)
    
    
    p_sentence=re.compile('<S ID=(\d)*>')
    
    
    print(p.match(x))


def read_raw_file(p1):
    
    print('Reading file from'+p1)
    
    Sent=[]
    f=codecs.open(p1, 'rU', 'utf-8')
    lines=f.readlines()
    for l in lines:
        Sent.append(l.strip())
    return Sent
    
def write_as_flat_txt(p2, Sent):
    f=codecs.open(p2, 'w', 'utf-8')
    for i in Sent:
        f.write(i+'\n')
     
    f.close()
        
    


def main(p1, p2):
    
    print('\n\n>>>Running extract_pure_text_form_xml.py...')
    
    print('Reading file from: '+p1)
    Sent=read_raw_file(p1)
    Clean=[]
    #print('print sentence...')
    
    print('Cleaning...')
    for i in Sent:
        
        non_sent=re.compile('<.*>') # non-xml-format lines
          
        
        if(not non_sent.match(i)):
            #print('\n>>Got it')
            Clean.append(i)
    
    print('#-of-sent-in-corpus='+str(len(Clean)))
        
    print('Writing sentences as txt file to: '+p2)
    write_as_flat_txt(p2, Clean)
    print('Jobs Done!\n')
    
     



if __name__=='__main__':
    
    print('argv: input_corpus_xml, output_corpus_txt')
    main(sys.argv[1], sys.argv[2])
  







