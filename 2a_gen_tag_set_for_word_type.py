#
# gen_tag_set_for_word_type.py
#

'''

2.a ==> generate the new-tag for each word type. This Output shall be a map:  Word (type) --> set of possible tags

The 'new tag' is actually the set of all possible tags for the word type in the corpus.
Such aggregated tag set reflects the syntactic distribution (clustering) of words.

adapted from word_pos_vectorization.py, instead of directly importing to minimize dependency



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



2. Generate hashtable Vec2Word and Word2NewTag

Vec2Word=dict() #hashtable: key:tag_set/tag_vec value: a list of all words, the tagvec of which is the key, sorted by word freq
Word2NewTag=dict() #hashtable: key:word (type), value: its tag_vec/new_tag
  

processing words in L_word and check the exisitance of the tag according to WordPOS2Freq

Then update Vec2Word and Word2NewTag


3. pickle the data object Vec2Word and Word2NewTag(the hashmap for the new tag that we need):


'''
import pickle
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



#scan the raw_txt format of the corpus, in which each sent is a line, and each token is the form "word_tag" pair
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



  
#
#  gen a hash table, key=word type  value: set of its possible tags, sorted alphabetally 
def word_newTag_hash_gen(WordPOS2Freq, L_word, L_tag):
  
  print ('Generating tag_set (newTag) for word types...')

  Vec2Word=dict() #hashtable: key:tag_set/tag_vec value: a list of all words, the tagvec of which is the key, sorted by word freq

  Word2NewTag=dict() #hashtable: key:word (type), value: its tag_vec/new_tag
  
    

  for i in L_word:
    vec1=[]
    #vec2=[]
    #sub_total=0
    
    for j in L_tag:

      word_tag=i+'_'+j
      freq=WordPOS2Freq.get_freq(word_tag)

      if freq>0:

        vec1.append(j)

    vec_profile=''


    vec_profile='_'.join(vec1)

    if vec_profile in Vec2Word:
      Vec2Word[vec_profile].append(i)

    else:
      d_list=[]
      d_list.append(i)
      Vec2Word[vec_profile]=d_list

    
    
    Word2NewTag[i]=vec1
        


  print('\nNum of unique pos-vectors:')
  print(len(Vec2Word.items()))
  #print(list(Vec2Word.items())[0])
  #print(len(list(Vec2Word.items())[0][1]))

  items=list(Vec2Word.items())

  items=sorted(items, key=lambda x:len(x[1]), reverse=True) #sort by num of words in the category
  

  for item in items:
    #print(item[0])
    x=L_tag
    y=item[0]

    print (y)


    for j in item[1][:min(20,len(item[1]))]:  #sample at most 20 words for each category
      print(j,  end='  ')
    print(' ')
    print('===')


  print('repeat ',end='')
  print('Num of unique pos-vectors:')
  print(len(Vec2Word.items()))



#
# store the Word2NewTag hashtable and Vec2Word hashtable to files using pickle.
#

  print('\n\n>>Store Vec2Word (hashtable, key:tag_set/tag_vec value: a list of all words, the tagvec of which is the key, sorted by word freq) vec2word.pickle')  

  p='../working_data/vec2word.pickle'
  print('to file ',p)
  f=open(p,'wb')
  pickle.dump(Vec2Word, f)
  f.close()

  

#
# store the Word2NewTag hashtable to file, using pickle.
#
  p='../working_data/word2newtag.pickle'
  print ('\n\n>>Store Word2NewTag hashtable (key:word (type), value: its tag_vec/new_tag) to file', p)
  f=open(p,'wb')
  pickle.dump(Word2NewTag, f)
  f.close()

  
  #f=open(p,'rb')
  #new_W2T=pickle.load(f)
  #f.close()
  #print (new_W2T==Word2NewTag)


#
# pickle the tag list
#  
  p='../working_data/taglist.pickle'
  print('\n\n>>pickle the tag list to ', p)
  f=open(p, 'wb')
  pickle.dump(L_tag,f)
  f.close()


if __name__=='__main__':
  print('\n>>>Running gen_tag_set_for_word_type.py')

  path='../working_data/all.txt'
  
  print('Arg: plain_txt version of corpus, if it is absent, ',path, ' will be used by default')

  
  if len(sys.argv)>1:
    path=sys.argv[1]
  
  WordPOS2Freq, L_word, L_tag=scan_corpus_build_hashtable(path)
  word_newTag_hash_gen(WordPOS2Freq, L_word, L_tag)
    
  
