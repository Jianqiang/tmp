#
#B_sentence_spliter.py
#

'''
Stanford parser simply breaks down when the token count >250 or so.
Also, longer sentences make parsing extremely slow.
---> We use a quick sentence splitter to split sent into shorter forms, by using 逗号 句号 分号 顿号 和 括号 和 书名号.
Note this may lead to "cheating", but using this simple pattern involves minimum effort is well justified.
'''

import codecs
import sys
print ('\nRunning sentence_spliter, which split sentences into difference lines of subsentences')
print('@Arg: 1.input_corpus  2_output_sent_splitted_corpus')
input_corpus=sys.argv[1]
output_corpus=sys.argv[2]

splitted_corpus=[]
puctuations={'，','；','、','。','（','）','《', "》"}

print('reading input corpus from', input_corpus)
f=codecs.open(input_corpus,'rU','utf-8')
for line in f.readlines():
  sent=[]
  chunk=[]
  for char in line.strip():
    if char in puctuations:
      chunk.append(char)
      sent.append(''.join(chunk))
      chunk=[]
      #chunk=[char] #duplicate the punctuation

    else:
      chunk.append(char)

  if len(chunk)>1:
    sent.append(''.join(chunk))
  
  splitted_corpus.append(sent)

f.close()

print('writing output corpus to', output_corpus)
f=codecs.open(output_corpus, 'w','utf-8')
for sent in splitted_corpus:
  for chunk_str in sent:
    f.write(chunk_str.strip()+'\n')
f.close()
print('done!')

