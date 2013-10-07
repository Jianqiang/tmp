#
# B_pos_tagged_sent_splitter.py
#

'''
<Update> We now split pos_tagged sentences, rather than raw or segmented sentences

Stanford parser simply breaks down when the token count >250 or so.
Also, longer sentences make parsing extremely slow.
---> We use a quick sentence splitter to split sent into shorter forms, by using 逗号 句号 分号 顿号 和 括号 和 书名号.
Note this may lead to "cheating", but using this simple pattern involves minimum effort is well justified.

'''
import codecs
import sys
import re

pos_pattern=re.compile('(.*)_([A-Z]+)')

print ('\nRunning pos_tagged_sent_spliter, which split sentences into difference lines of subsentences')
print('@Arg: 1.input_corpus  2_output_sent_splitted_corpus')
input_corpus=sys.argv[1]
output_corpus=sys.argv[2]

splitted_corpus=[]
#punctuations={'，','；','、','。','（','）','《', '》','“','”'}
punctuations={'，','；','、','。','（','）'} #only use the basic  punctuations

print('reading input corpus from', input_corpus)
f=codecs.open(input_corpus,'rU','utf-8')

longest_chunk=(0,'')
old_longest_sent=0
for line in f.readlines():
  sent=[]
  chunk=[]
  for token in line.split():
    if len(line.split())>old_longest_sent:
      old_longest_sent=len(line.split())
      
    if pos_pattern.match(token).group(1) in punctuations:
      chunk.append(token)
      sent.append(' '.join(chunk))
      
      if len(chunk)>longest_chunk[0]:
        longest_chunk=(len(chunk),' '.join(chunk))
      chunk=[]
      #chunk=[char] #duplicate the punctuation

    else:
      chunk.append(token)

  if len(chunk)>0:
    sent.append(' '.join(chunk))
    if len(chunk)>longest_chunk[0]:
      longest_chunk=(len(chunk),' '.join(chunk))

  splitted_corpus.append(sent)

f.close()
print('writing output corpus to', output_corpus)
f=codecs.open(output_corpus, 'w','utf-8')
count=0
count_old=0
for sent in splitted_corpus:
  count_old += 1
  for chunk_str in sent:
    f.write(chunk_str.strip()+'\n')
    count += 1
f.close()


print('\nThere are',count, 'splitted setences (original sent count=',count_old,') ratio=',count/count_old)
print('\nAnd the longest splitted sent:',longest_chunk[1],'\nlength=',longest_chunk[0])
print('\nLongest original sent, length=', old_longest_sent)
print('done!')
