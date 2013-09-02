#
# stanford_parser_prob_collector.py
#

'''
collect top N anaylsis of stanford parser

'''


import codecs
import sys
import re
import pickle

#N=3

print('\n>>>Collecting Stanford parser tree probabilities...')
print('Arg: 1.parsing results (Viterbi output), 2.path_to_keep_pickle_file')
f=codecs.open(sys.argv[1], 'rU','utf-8')

path_out='parse_prob.pickle'
if len(sys.argv)>2:
  path_out=sys.argv[2]

ProbList=[]


sent_prob=[]

k=0
print('Start procesing...')
for line in f:
  if not k%100000:
    print(k,'lines have been finished...' )

  k += 1

  l=line.strip()
  #print(l)
  if l:
    tokens=re.findall('\S+',l, re.U)

    if tokens[0]=='#':
      if tokens[2]=='1' and sent_prob:
        ProbList.append(sent_prob)
        sent_prob=[]
      sent_prob.append(float(tokens[-1]))

if sent_prob:
  ProbList.append(sent_prob)
      

f.close()
print('\nThere are probability entries of ',len(ProbList),'sentences')
print('first one:', ProbList[0])


f=open(path_out, 'wb')
print('Pickling ProbList to', path_out,'...')
pickle.dump(ProbList, f)
f.close()
print('done!')






    
  
  
