#
# X_baseline_parser.py
#

'''
X_baseline_parsing_seg.py: a class that implement a parser that gives the probability
of best probably analysis of a character string by parsing it with the baseline grammar.
And it use such score of each word hypothesis to run Viterbi algorithm to get the best segmentation of the words.

'''

import pickle
import sys
import re
import codecs
import copy
import math

#from multiprocessing import Pool

from nltk import ViterbiParser
#from nltk.parse import pchart




class ParserSeger():

  def __init__(self, the_grammar):

    print('Initialization of ParserSeger...')

    self.parser=ViterbiParser(the_grammar)
    self.max_word_len=4
    print('done')

  def score(self, word_candidate):  # log (prob, 2) as score
    #return -1000

    parseTree_list=self.parser.nbest_parse(word_candidate)

    if parseTree_list:  # if there is any parse
      return parseTree_list[0].logprob()
    else:
      return -1000  #2*-1000== almost zero


  def viterbi_segment(self, sentence):

    if 0:
      print('Current sent',sentence)
      print(len(sentence))
      print('***')
   

    BestSeg={}  #key: end_of_partial_sentence (python index style)
                #value: (best_segmentation, segmentation_score)
    BestSeg[0]=([],1)

    
    for i in range(1, len(sentence)+1):

      print(i)
      best_score=-1000000
      best_ptr=0
     
      for j in range(-1, -(min(i+1,len(sentence)+1, self.max_word_len+1)),-1):     
        
        word=sentence[i+j:i]
        word_score=self.score(word)
        seg_score=-1000000

        if i+j>0:
          
          best_sub_seg_record=BestSeg[i+j]
          best_sub_seg=best_sub_seg_record[0]
          best_sub_score=best_sub_seg_record[1]

          seg_score=best_sub_score+word_score

        else:
          seg_score=word_score
        
        if seg_score>best_score:

          best_ptr=i+j
          best_score=seg_score


      b=BestSeg[best_ptr]
      best_seg=copy.copy(b[0])    
      best_seg.append(''.join(sentence[best_ptr:i]))
      BestSeg[i]=(best_seg, best_score)


    final_seg_record=BestSeg[len(sentence)]
    final_seg=final_seg_record[0]
    #print(final_seg)
    return final_seg           


  def segment_corpus(self, corpus):
    

   
    Result=[]

    sent_count=0

    for sent in corpus:

      if sent_count%int(len(corpus)/100)==0:
        print(math.ceil(sent_count/len(corpus)*100),'% finished...')

      char_list=re.findall('\S',sent, re.U)# even if it is a gold standard corpus, we use the raw form (discarding the original segmentation)
      #char_seq=l.replace(" ", "") 
      #print('XXXchar_seq',char_seq)

      result=self.viterbi_segment(char_list)
      Result.append(result)
      sent_count += 1


    path_out='../working_data/base_seg.out'
    

    f3=codecs.open(path_out, 'w', 'utf-8')
    print('\nPriting out segmented corpus to file ', path_out)
    for r in Result:
      f3.write(' '.join(r)+'\n')

    print('\n','   --- Segmentation Done!  ---   ')
    print('# of sentence being segmented:', sent_count)
    print('# of sentence in test corpus(see whether it matches last num):', len(lines))





path_grammar='../working_data/baseline.grammar.pickle'

print('\nloading the induced grammar to',path_grammar,' ...')
f=open(path_grammar, 'rb')
grammar=pickle.load(f)
f.close()

PSeg=ParserSeger(grammar)

corpus_path='../working_data/top100.seg'
#corpus_path='../working_data/test.seg'

print('\n###Segmenting corpus', corpus_path, '...')

f=codecs.open(corpus_path, 'rU','utf-8')
corpus=f.readlines()


PSeg.segment_corpus(corpus)

#sent='张'+' '+'持'+' '+'坚'
#tokens=re.findall('\S+',sent, re.U)
#parser=ViterbiParser(grammar)
#parse = parser.nbest_parse(tokens)


