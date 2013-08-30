#
# uniq_ngram_gen.py
#

'''
input: a un-segmented corpus

output: all distinct ngrams up to N

'''


import sys
import codecs
import re


print('\>>>Running uniq_ngram_gen.py')
print('(Arg1)input: a un-segmented corpus; (Arg2)output: all distinct ngrams (character sep by space) up to N')

path_input=sys.argv[1]
path_output=sys.argv[2]

N=10  #maximum length of the word candidate

Ngram=set()

f1=codecs.open(path_input, 'rU','utf-8')
lines=f1.readlines()
f1.close()

print('\ncollection...')

count=0
total_nth=int(len(lines)/10)
for line in lines:
  if count%total_nth==0:
    print(count/total_nth*10, '% finished')
  count +=1
  
  char_seq=' '.join(re.findall('\S', line, re.U))

  for i in range(len(char_seq)):
    for j in range(i+1,min(len(char_seq), i+N)+1):
      Ngram.add(char_seq[i:j])


print('\nWriting results to', path_output, '...')
f2=codecs.open(path_output, 'w','utf-8')
for i in Ngram:
  f2.write(i+'\n')


      
  
