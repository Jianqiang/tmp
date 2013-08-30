



import sys
import codecs
import re
import math
import copy


# the log-sum trick, to avoid overflow
def log_sum_exp_log(list_of_log_probs):

  max_log_prob=-1e100


  for log_prob in list_of_log_probs:

    if log_prob > max_log_prob:
      max_log_prob=log_prob

  new_list_of_log_probs=[i-max_log_prob for i in list_of_log_probs]

  #print(new_list_of_log_probs)

  log_sum_exp_log=max_log_prob+math.log(sum([math.e**log_prob  for log_prob in new_list_of_log_probs]))

  return log_sum_exp_log





def viterbi_seg(self, sentence, score_function, sent_id):
    if 0:
      print('YYYYsent',sentence)
      print(len(sentence))
      print('***')
   

    BestSeg={}  #key: end_of_partial_sentence (python index style)
                #value: (best_segmentation, segmentation_score)
    BestSeg[0]=([],1)

    
    for i in range(1, len(sentence)+1):
      best_score=-1000000
      best_ptr=0
     
      for j in range(-1, -(min(i+1,len(sentence)+1, self.max_word_len+1)),-1):     
        
        word=''.join(sentence[i+j:i])
        word_score=math.log(self.LM.get_raw_word_score(word), 2) ##===>score function
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
    return final_seg       

#
# overwrite the segment_corpus method
def segment_corpus(self):

    print('\n###Segmenting the testing corpus...')

    Result=[]

    sent_count=0
    for l in self.corpus:
      
      char_seq=l.replace(" ", "") # even if it is a gold standard corpus, we use the raw form (discarding the original segmentation)

      #print('XXXchar_seq',char_seq)
      result=self.segment(char_seq, sent_count)
      Result.append(result)
      sent_count=sent_count+1

    tmp_index=self.path_to_test.rfind('/')+1
    path_out=self.path_to_test[tmp_index:]+'.seg'

    f3=codecs.open(path_out, 'w', 'utf-8')
    print('\nPriting out segmented corpus to file ', path_out)
    for r in Result:
      f3.write(' '.join(r)+'\n')

    print('\n','   --- Segmentation Done!  ---   ')
    print('# of sentence being segmented:', sent_count)
    print('# of sentence in test corpus(see whether it matches last num):', len(self.corpus))




