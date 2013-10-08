#
# D_gcp_basline_grammar.py
#

'''
generate the baseline grammar directly from Zhang's original annotation

(pre-processed by 1_pre_proc_annotation.py to comply with PTB format,
defaul file: annotation_nltk.data)



dependency: this code needs the result word2newtag.pickle from running 2a_gen_tag_set_for_word_type.py 
'''

from nltk import Tree
import re

import codecs
import sys
import pickle
import string

from utility_proj import decompose_tag


def remove_all_subscript_from_str(d_str):
  return d_str[:-2]+d_str[-1] if len(d_str)>2 and d_str[-2]=='_' and d_str[-1] in string.ascii_lowercase else d_str
    

def remove_crl_subscript_from_str(d_str):
  return d_str[:-2]+d_str[-1] if len(d_str)>2 and d_str[-2]=='_' and d_str[-1] in {'l','r','c'} else d_str



tag_word_pattern=re.compile('(.*)_([A-Z]*)')


word_pos2tree_str={}  ##### main data of this code, a dictionary, key: (word, pos)  value: tree_str of the annotation


print('\n\n>>>Running X_baseline_grammar.py, which gen a baseline grammar directly from the word-struture annotaiton')
print('Optional Argv: 0. pos_tagged_corpus_to_be_annotated  1. proprocessed_word_structure_annotation,  2.word2tag mapping')

path_annotation='../working_data/annotation_nltk.data'
if len(sys.argv)>2:

  path_annotation=sys.argv[2]


print('\n\nprocessing annotation from ', path_annotation, '...  \nprograss:')
f=codecs.open(path_annotation, 'rU', 'utf-8')
lines=f.readlines()
f.close()

Production=[]

count=0
total_nth=int(len(lines)/10)
for line in lines:
  if count%total_nth==0:
    print(count/total_nth*10, '% finished')
  count +=1

  tree=Tree(line.strip())
  tag, subscript=decompose_tag(tree.node)
  word=''.join(tree.leaves())

  word_pos2tree_str[(word, tag)]=line.strip()
  

print('done!')

#
# gen single-char annotation from the corpus
#

print('\n\ngenerating rules for single-char words from corpus')

#---> one needs to run 2a_gen_tag_set_for_word_type.py to gen word2newtag.pickle before using it
path_word2newtag='../working_data/word2newtag.pickle'



if len(sys.argv)>3:
  path_word2newtag=sys.argv[3]

print('\nreading (intermedidate reuslt) Word2NewTag hashtable from ', path_word2newtag)
f=open(path_word2newtag, 'rb')

Word2NewTag=pickle.load(f) # word2Newtag, dict: key=word  value=set of possible tags
f.close()


for word in Word2NewTag:
  if len(word)==1:
    tag_set=Word2NewTag[word]

    for tag in tag_set:

      tree_string='( '+tag+'_u  '+word+'  )'

      tree=Tree(tree_string.strip())
      tag, subscript=decompose_tag(tree.node)
      word=''.join(tree.leaves())
      word_pos2tree_str[(word, tag)]=tree_string.strip() 
          

print('done!')



word2tree_str={i[0]:word_pos2tree_str for i in word_pos2tree_str} # word to tree_str mapping, for backup/smoothing of unseen (word, tag) pairs


#### -----------------------> why the above situation would ever happen???? Suggesting incompleteness of path_word2newtag='../working_data/word2newtag.pickle'??? Why?   @@@@@ 3######  XXXXX  <------------


#
#
############>>> Generate sentence-leavel annotationn, i.g. training data for global consitituent parsing model from the base grammar
# 
#

p_tagged_corpus='../working_data/train.ctb5.pos'
flag_split=False

if flag_split:
  p_tagged_corpus='../working_data/train.ctb5.pos.split.new'

#just in case that we need to 
if len(sys.argv)>1:
  p_tagged_corpus=sys.argv[1]

trait='train'+flag_split*'.split'

print('\nreading pos-tagged corpus from', p_tagged_corpus, '...')

f=codecs.open(p_tagged_corpus, 'rU','utf-8')
pos_corpus=[[(tag_word_pattern.match(token).group(1), tag_word_pattern.match(token).group(2)) for token in line.split()] for line in f.readlines()]
f.close()

print('\n\n>>>Generating flat_treebanks using baseline grammar (word-structure annotation...)')

Annotation1=[]
Annotation2=[]
Annotation3=[]

for line in pos_corpus:

  middle_list=[]
  for (word,pos_tag) in line:
    if (word, pos_tag) in word_pos2tree_str:
      middle_list.append(' ( '+pos_tag+'POS  '+word_pos2tree_str[(word, pos_tag)]+' ) ')
    elif word in word2tree_str:
      middle_list.append(' ( '+pos_tag+'POS  '+word_pos2tree_str[word]+' ) ')
    else:
      print('Error! unseen character in the TRAINING data!!!')
  
  tree_str=''.join([' ( ( S ']+[' ( '+pos_tag+'POS  '+word_pos2tree_str[(word, pos_tag)]+' ) ' for (word, pos_tag) in line ]+[' ) ) \n'])
  tree_str2=remove_all_subscript_from_str(tree_str)
  tree_str3=remove_crl_subscript_from_str(tree_str)
  
  tree_str1=' '.join([i[:-2]+i[-1] if len(i)>1 and i[-2]=='_' else i for i in tree_str.split()]) # remove '_' to merge subscript to merge it to the non-terminal
  #tree_str2 have already remove all the subscripts, so don't do anything to it
  tree_str3=' '.join([i[:-2]+i[-1] if len(i)>1 and i[-2]=='_' else i for i in tree_str3.split()]) # remove '_' to merge subscript to merge    Annotation1.append((new_tree_str1, counter))

  Annotation1.append(tree_str1)
  Annotation2.append(tree_str2)
  Annotation3.append(tree_str3)


prefix='../working_data/'
p1=prefix+trait+'.b1.basetree'
p2=prefix+trait+'.b2.basetree'
p3=prefix+trait+'.b3.basetree'


def write_trees(annotation, path_to_out_annotation):
  print('done!\n>writing the annotation to ', path_to_out_annotation)
  f=codecs.open(path_to_out_annotation, 'w', 'utf-8')
  for sent in annotation:
    f.write(sent)
  print('done!')

print('\nWriting flat treebank into')

write_trees(Annotation1, p1)
write_trees(Annotation2, p2)
write_trees(Annotation3, p3)
    

   
  

