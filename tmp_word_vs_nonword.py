#
# word_vs_non_word.py
#

import re
import codecs

p1='../working_data/test.dic'
f=codecs.open(p1,'rU','utf-8')
lines=f.readlines()
f.close()

corpus=[re.findall('\S',line, re.U) for line in lines]
new_corpus=[ line[i:j] for line in corpus for i in range(len(line)) for j in range(i+1, len(line)+1)  if len(line)>1]

output_corpus='\n'.join([' '.join(line) for line in new_corpus])

p2='../working_data/t.txt'
f=codecs.open(p2, 'w','utf-8' )
f.write(output_corpus)
f.close()
