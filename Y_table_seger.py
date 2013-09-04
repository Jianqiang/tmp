#
# Y_table_seger.py
#
'''
using the parsing probability of a string in String2ParseProb TABLE as the score function,
of the candiadte, then find the best segmentation with Viterbi algorithm.

'''
import codecs
import sys
import re
import pickle
import math
import copy


class TableBasedSegmenter():

  def __init__(self, path_to_score_table):

    print('\n>>>Initialization of TableBasedSegmenter...')

    print('loading score table from ', path_to_score_table, '...')
    f=open(path_to_score_table, 'rb')

    self.String2ParseProb=pickle.load(f)
    f.close()


    self.max_word_len=8
    print('done')

  def score(self, word_candidate):  # log (prob, 2) as score
    #return -1000

    candidate_string=''.join(word_candidate)

    if candidate_string in self.String2ParseProb:
      return self.String2ParseProb[candidate_string]
    else:
      return -1000  #2**-1000== almost zero


  def viterbi_segment(self, sentence):

    if 0:
      print('Current sent',sentence)
      print(len(sentence))
      print('***')
   

    BestSeg={}  #key: end_of_partial_sentence (python index style)
                #value: (best_segmentation, segmentation_score)
    BestSeg[0]=([],1)

    
    for i in range(1, len(sentence)+1):

      #print(i)

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


  def segment_corpus(self, corpus_path):

    f=codecs.open(corpus_path, 'rU','utf-8')
    corpus=f.readlines()
    

   
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

    prefix=re.findall('[^/]+', corpus_path)
    prefix_str='/'+'/'.join(prefix[:-1])
    path_out=prefix_str+'/table_seg.out'
    

    f3=codecs.open(path_out, 'w', 'utf-8')
    print('\nPriting out segmented corpus to file ', path_out)
    for r in Result:
      f3.write(' '.join(r)+'\n')

    print('\n','   --- Segmentation Done!  ---   ')
    print('# of sentence being segmented:', sent_count)
    print('# of sentence in test corpus(see whether it matches last num):', len(corpus))

  


#
# testing  ------------
#
print('\n\n>>>Testing Table based Segmenter...')
print('Arg: 1. path_to_string2probTable (string2parseprob.pickle by default),  2.path_to_test_corpus(test.seg by default)')

path_string2prob='string2parseprob.pickle'

#corpus_path='/Users/jma/dropbox/code/LatentPoS/working_data/top100.seg'
corpus_path='/Users/jma/dropbox/code/LatentPoS/working_data/test.seg'

if len(sys.argv)>1:
  path_string2prob=sys.argv[1]

  if len(sys.argv)>2:
    corpus_path=sys.argv[2]

TSeg=TableBasedSegmenter(path_string2prob)


print('\n###Segmenting corpus', corpus_path, '...')

TSeg.segment_corpus(corpus_path)

