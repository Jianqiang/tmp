#
# seg2char.py
#

import codecs
import sys

print('\n>>>Converting segmented sentences into white-spaced character sentences')
print('\n@Arg: 1. input_segmented_corpus, 2.output_char_corpus')
print('\nReading segmented corpus from ', sys.argv[1])

f=codecs.open(sys.argv[1],'rU','utf-8')
charSeq=[' '.join(''.join(line)) for line in f.readlines()]
f.close()

print('\nWriting white-spaced char corpus into ', sys.argv[2])
f=codecs.open(sys.argv[2],'w','utf8')
for line in charSeq:
  f.write(' '.join(line))
f.close()
