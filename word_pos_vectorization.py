#
# word_pos_vectorization.py
#

'''
Get vector representations of words in CTB5.0,
either 0/1 indicator in terms of POS tags, or normalized relative frequency in terms of POS tags.

e.g. of 0/1 indicator:
[1,1,0,0...] represents a word has occurred as a noun, verb, but not any other POS in the corpus
[0,1,0,0...] represents a word has only occurred as a verb in the corpus... etc
    

implementation:

// we explicitly use the format of word_pos pair (as following). In a different corpus, a new pattern match is needed

1. Scan the corpus in the form of token sequences of word_POS pair, e.g. '希望_VV 能_VV 借_P 此_DT 机会_NN'

to build
a. WordPOS2Freq hashtable, key:word_POS pairs value:their frequency in the corpus
//(may not need this value)  b. Word2POS hashtable, key: word  value: POS tag co-occurred with the word
c. POS2Freq hashtable, key: pos value: its frequency in the corpus
d. Word2Freq hashtable, key: word value: its frequency in the corpus

from Word2Freq gen a list of word according to their total frequncy in the corpus  L_word (obvious), then delete POS2Freq?
from POS2Freq gen a list of distinct tag according to their frequency in the corpus L_tag (obvious), then delete Word2Freq?



2. Generate two types of vectors for each word

gen the 0/1 indicator matrix by processing words in L_word and check the exisitance of the tag according to WordPOS2Freq
gen the normalized relative frequency matrix by processing words in L_word and compute the relative frequency of the tag, according to WordPOS2Freq

Then write them to file


3. POS vector profiling:

try to see how many unique POS combinations for words.

e.g.


'''

import codecs
import sys
import os
import re 


# a simple hashtable implementation

class SimpleHash:

  def __init__(self):
    self.table={}


  # make key==item hash to value==freq, allow overide of previous results 
  def insert_item_freq(self, item, freq):
    self.table[item]=freq
    

  def add_item(self, item):

    if item in self.table:
      freq=self.table[item]
      freq=freq+1
      self.table[item]=freq
    else:
      #freq=1
      self.table[item]=1
      
  def get_freq(self, item):

    if item in self.table:
      return self.table[item]
    else:
      return 0




def scan_corpus_build_hashtable(p):

  # init of the 3 hashtable
  WordPOS2Freq=SimpleHash()
  POS2Freq=SimpleHash()
  Word2Freq=SimpleHash()

  f=codecs.open(p,'r','utf-8')
  lines=f.readlines()
  for line in lines:
    tokens=re.findall('\S+', line, re.U)
    for token in tokens:

      #print(token,' is being processed')

      WordPOS2Freq.add_item(token)

      match=re.search('(.+)_([A-Z]+)', token)  #<-----------------  this pattern matching depends on the concrete format of the corpus
      try:
        word=match.group(1)
        tag=match.group(2)

        POS2Freq.add_item(tag)
        Word2Freq.add_item(word)
        

      except:
        print('Error!!! word-tag pair are not in the expected form word_tag')



  print(len(WordPOS2Freq.table.items()))
  print(len(POS2Freq.table.items()))
  print(len(Word2Freq.table.items()))


  L=POS2Freq.table.items()
  L=sorted(L, key=lambda x:x[1], reverse=True)
  L_tag=[i[0] for i in L]
  print(L_tag)

  L=Word2Freq.table.items()
  L=sorted(L, key=lambda x:x[1], reverse=True)
  L_word=[i[0] for i in L]
  print(L_word[:50])


  return WordPOS2Freq, L_word, L_tag



  



def pos_vec_profiling(WordPOS2Freq, L_word, L_tag):

  print('profiling pos_vectors of words...')


  Vec2Word=dict()
  

  M1=[]
  M2=[]

  

  for i in L_word:
    vec1=[]
    vec2=[]

    sub_total=0
    
    for j in L_tag:

      word_tag=i+'_'+j

      freq=WordPOS2Freq.get_freq(word_tag)

      vec1.append((freq>0)*1)
      vec2.append(freq)
      sub_total=sub_total+freq

    vec2=[v/sub_total for v in vec2]


    vec_profile=''

    if len(vec1)!=34:
      print('@Warning@')
      print(len(vec1))

    for num in vec1:
      vec_profile=vec_profile+str(num)

    if vec_profile in Vec2Word:
      Vec2Word[vec_profile].append(i)

    else:
      d_list=[]
      d_list.append(i)
      Vec2Word[vec_profile]=d_list

    
    
    
        

    

    M1.append(vec1)
    M2.append(vec2)


    #vec1.append(i)   #-----------------------> These few lines are for looking/observing data only
    #vec2.append(i)
    #print(vec1)
    #print(vec2)
    #print('===')


  print('\nNum of unique pos-vectors:')
  print(len(Vec2Word.items()))
  #print(list(Vec2Word.items())[0])
  #print(len(list(Vec2Word.items())[0][1]))

  items=list(Vec2Word.items())
  for item in items:
    #print(item[0])
    x=L_tag
    y=item[0]
    z=[bool(int(y[i]))*x[i] for i in range(len(x))]
    for pos in z:
      if pos!='':
        print(pos, end=' ')
    print('==>num of words:',len(item[1]))

    for j in item[1][:min(20,len(item[1]))]:  #sample at most 20 words for each category
      print(j,  end='  ')
    print(' ')
    print('===')


  print('repeat ',end='')
  print('Num of unique pos-vectors:')
  print(len(Vec2Word.items()))


  print('\nOutput unredundant pos-vector repres. matrix to m0.txt')

  p='../working_data/m0.txt'
  f=codecs.open(p,'w','utf-8')
  
  for i in L_tag:
    f.write(str(i)+'  ')

  f.write('\n')

  for i in items:
    for j in i[0]:
      f.write(str(j)+'  ')
    f.write('\n')
    
  
  #print('\n\n')
  #for x in L_tag:
    #print(x,end=' ')
  #print('\n')

  #for i in Vec2Word:

    #signal=[bool(j) for j in i]
    #print(len(signal))

    #print(len(L_word))
    #print(i)
    #out=[signal[j]*L_word[j] for j in range(len(L_word))]

    #print(out)
    


  


  # writing to files:
def write_matrix_to_file(M1, M2):

  print('\n\n>>>Write two POS matrix to m1.txt and m2.txt')

  prefix='../working_data/'

  p1=prefix+'m1.txt'
  p2=prefix+'m2.txt'
  
  f=codecs.open(p1, 'w','utf-8')

  for vec1 in M1:
    for entry in vec1:
      f.write(str(entry)+'  ')
    f.write('\n')


  f=codecs.open(p2, 'w','utf-8')

  for vec2 in M2:
    for entry in vec2:
      f.write(str(entry)+'  ')
    f.write('\n')
  

  

  
        



if __name__=='__main__':
  WordPOS2Freq, L_word, L_tag=scan_corpus_build_hashtable(sys.argv[1])
  pos_vec_profiling(WordPOS2Freq, L_word, L_tag)
    
  
