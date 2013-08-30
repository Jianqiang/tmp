#
# pos2seg.py
#
'''
convert pos-tagged (and of course word-segmented) corpus to purely word-segmented corpus 

'''

import codecs
import re
import sys

print('\nConvert pos-tagged (and of course word-segmented) corpus to purely word-segmented corpus ')
print('Argv: 1. input_pos_tagged_corpus  2. output_seged_corpus')

tag_word_pattern=re.compile('(.*)_([A-Z]*)')

f1=codecs.open(sys.argv[1], 'rU','utf-8')
lines=f1.readlines()
f1.close()

print('reading original POS-tagged corpus from ', sys.argv[1],'....')
WordCorpus=[]
for l in lines:
  tokens=re.findall('\S+', l, re.U)

  word_seq=[tag_word_pattern.match(i).group(1) for i in tokens]

  WordCorpus.append('  '.join(word_seq))

print('writing word-segmented corpus to ',sys.argv[2],'...')

f2=codecs.open(sys.argv[2], 'w','utf-8')

for sent in WordCorpus:
  f2.write(sent+'\n')
f2.close()
print('done!')
