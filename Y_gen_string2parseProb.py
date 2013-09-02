#
# Y_gen_string_prob_table.py
#

import codecs
import sys
import re
import pickle
import math

#(the log_sum_exp trick) given log probability, compute the log of the sum of the raw probabilities
def log_sum_exp_log(list_of_log_probs):

  max_log_prob=-1e100


  for log_prob in list_of_log_probs:

    if log_prob > max_log_prob:
      max_log_prob=log_prob

  new_list_of_log_probs=[i-max_log_prob for i in list_of_log_probs]

  #print(new_list_of_log_probs)

  log_sum_exp_log=max_log_prob+math.log(sum([math.e**log_prob  for log_prob in new_list_of_log_probs]))

  return log_sum_exp_log



d_function=log_sum_exp_log

print('\n>>>Reading ngram file and build string2prob table...')
print('Argv: 1.ngram_file, 2.parsing_prob_pickle (parse_prob.picle by default), 3.output_result (string2parseProb.pickle)')

f=codecs.open(sys.argv[1],'rU','utf-8')

print('reading ngram file ', sys.argv[1],' ...')

Ngram=[]

k=0
for line in f:
  if not k%100000:
    print(k,'lines have been finished...' )

  k += 1

  l=line.strip()
  #print(l)
  if l:
    tokens=l.split()
    ngram=''.join(tokens)
    Ngram.append(ngram)

f.close()

path2='parse_prob.pickle'

if len(sys.argv)>2:
  print (sys.argv)
  path2=sys.argv[2]

print('\nloading ParseProbList from', path2, '...')
f=open(path2, 'rb')
ProbList=pickle.load(f)
f.close()

d_len=0
if len(ProbList)!=len(Ngram):
  print('Error! Num. of itmes in Ngram table and ProbList table are not same:', len(ProbList), len(Ngram))

else:
  d_len=len(ProbList)

print('\nGenerating String2ParseProb table...')
String2ParseProb={Ngram[i]:d_function(ProbList[i]) for i in range(d_len)}
print('done')

path3='string2parseprob.pickle'
if len(sys.argv)>3:
  path3=sys.argv[3]

print('\nStoring String2ParseProb table to', path3, '...')
f=open(path3, 'wb')
pickle.dump(String2ParseProb, f)
f.close()
print('Done!')
