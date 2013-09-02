#
# X_write_annotation.py
#

'''
write annotations in the PTB format as txt file

'''

import nltk

import codecs
import sys
import pickle


print('\n\n>>>Running X_write_annotation.py, which write annotation in PTB format as txt file')
print('Optional Argv: 1. proprocessed_word_structure_annotation,  2.word2tag mapping')

path_annotation='../working_data/annotation_nltk.data'
if len(sys.argv)>1:

  path_annotation=sys.argv[1]


print('\n\nprocessing annotation from ', path_annotation, '...  \nprograss:')
f=codecs.open(path_annotation, 'rU', 'utf-8')
lines=f.readlines()
f.close()


AnnotationPTB=[]

count=0
total_nth=int(len(lines)/10)
for line in lines:
  if count%total_nth==0:
    print(count/total_nth*10, '% finished')
  count +=1

  tree_string='( S '+line.strip()+' )'  #S is the extra root node (to indicate it is a word)

  AnnotationPTB.append(tree_string)

print('done!')

#
# gen single-char annotation from the corpus
#

print('\n\ngenerating rules for single-char words from corpus')

#---> one needs to run 2a_gen_tag_set_for_word_type.py to gen word2newtag.pickle before using it
path_word2newtag='../working_data/word2newtag.pickle'



if len(sys.argv)>2:
  path_word2newtag=sys.argv[2]

print('\nreading (intermedidate reuslt) Word2NewTag hashtable from ', path_word2newtag)
f=open(path_word2newtag, 'rb')


Word2NewTag=pickle.load(f) # word2Newtag, dict: key=word  value=set of possible tags
f.close()
print('processing...')
for word in Word2NewTag:
  if len(word)==1:
    tag_set=Word2NewTag[word]

    for tag in tag_set:

      tree_string='( S ( '+tag+'_u  '+word+' ) )'

      AnnotationPTB.append(tree_string)

    
print('done!')


path='../working_data/annotation_ptb.txt'
print('\nWriting annotation to ', path, '...')

f=codecs.open(path,'w','utf-8')
for tree_string in AnnotationPTB:
  f.write(tree_string+'\n')
print('\n\nEverything done!')
  

