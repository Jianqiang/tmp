#WordListGen.py   Generates a file that contains a list of lexical items given a corpus
# and also a raw(unsegmented corpus of the original corpus)
# input: corpus, path_word_list, path_corpus_raw  output: word_list, corpus_raw
#

import os
import codecs
import re
import sys


def main(corpus, wordlist, train_raw):
  d_set=set()
  set2=set()
  
  f3=codecs.open(corpus,'rU','utf-8')
  f4=codecs.open(train_raw,'w','utf-8')

  print('Writing the raw(unsegmented corpus to file)')
  lines=f3.readlines()
  for l in lines:
    charSeq=re.findall(r'\S',l, re.U)
    for j in charSeq:
      f4.write(j)
    f4.write('\n')

    
  f=codecs.open(corpus,'rU','utf-8')
  #wordlist='../wordlist.txt'
  f2=codecs.open(wordlist,'w','utf-8')
  

  lines=f.read()
  Lexicon=set() 
  words=re.findall(r'\S+',lines, re.U )
  Lexicon.update(words)
  #print(Lexicon)
  print('Writing resulting wordlist into ../wordlist.txt')
  for i in Lexicon:
    f2.write(i+'\n')


if __name__=='__main__':
  print('Running WordListGen.py')
  print('Input: a corpus file, path to wordlist file path_to_raw_corpus  Output: wordlist, raw_corpus')
  
  main(sys.argv[1], sys.argv[2],sys.argv[3])


