#
# pos2charSeq.py
#


import codecs
import sys
import re

pos_pattern=re.compile('(.*)_([A-Z]+)')
print('\n>>>Converting pos-tagged sentences into white-spaced character sentences')
print('\n@Arg: 1. input_pos_tagged_corpus, 2.output_char_corpus')
print('\nReading POS-tagged corpus from ', sys.argv[1])
f=codecs.open(sys.argv[1],'rU','utf-8')

print('\nConverting...')
wordCorpus=[ [pos_pattern.match(token).group(1) for token in line.split()] for line in f.readlines() ]
charCorpus=[''.join(line) for line in wordCorpus]
f.close()

print('\nWriting white-spaced char corpus into ', sys.argv[2])
f=codecs.open(sys.argv[2],'w','utf8')
for line in charCorpus:
  f.write(' '.join(line)+'\n')
f.close()



