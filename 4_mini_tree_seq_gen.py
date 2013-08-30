#
# 4_mini_tree_seq_gen.py
#

import re
import pickle
import sys
import codecs

#from nltk import Tree
from nltk import ParentedTree

from utility_proj import set2str
from utility_proj import decompose_tag
from utility_proj import pattern

'''

4. mini-tree sequence generation: using word-structure annotation and segmented sentence to get the final token-level annotation.

Before action, try to test the coverage, to make sure each word type in the corpus has an annotation. And also, removing duplicated annotations for the same string (char/word/subword)

1. check duplication, i.e. for each word type, whether there are more than 1 annotated trees, if so, choose one.

2. check whether there is any word type  (len>1) that has no annotation.  Word list can be gen from ../working_data/word2newtag.pickle , which is one output of 2a_gen_tag_set_for_word_type.py

3. gen single character word derivation, i.e.  T_u --> char, where subscript 'u' indicates unary derivation.  Or shall we make it T_u --> T_b -->char?  It appears that this extra derivation is not so helpful at this moment. 


Need a hashtable  String2Tree to keep the full annotation of each word, including subscripts. In the mini-tree sequence generation, i.e. the process of substituting each word token with its annotated tree for each sentence in the corpus, we can dynamically generate 3 version:

1.  keep all the subscripts       Corpus1
2. remove all the subscripts     Corpus2
3. remove the c/r/l  subscripts while keeping b/i subscripts  Corpus3

Then write them as PTB style bracketed txt file


'''

class Str2Hash():

  def __init__(self):

    self.table={}
    self.count=0
    self.prefix='T'

  def str2code(self, string):

    if not string in self.table:

      self.table[string]=self.count
      self.count += 1
      
    return self.prefix+str(self.table[string])

  
    



print('\n>>>Running mini_tree_seq_gen.py, generates sentences that are sequences of mini-trees (mts). Each tree represents the structure of a word.')
print('\nArg: path_t0_word_segmented_corpus, mts_corpus1, mst_corpus2, mst_corpus3')


##############  Loading data, NewForest, UpdatedVec and Word2Tag from pickled file #######
p1='../working_data/new_annotation.pickle'

print('\nloading word structure trees from ', p1, '...')

f=open(p1,'rb')
NewForest=pickle.load(f)
f.close()


p2='../working_data/updated_Vec.pickle'
print ('\nloading string2tag mapping UpdatedVec from',p2, '...')

f=open(p2,'rb')
UpdatedVec=pickle.load(f)
f.close()


p3='../working_data/word2newtag.pickle'

print('\nloading word2tag table from',p3, '...')

f=open(p3,'rb')
Word2Tag=pickle.load(f)
f.close()



#############  check duplication of trees ############

Word2treeID={}  #hashtable that maps a word to a set of index of NewForest. each NewForest[i] is a (parented) tree.


words_have_multiple_trees=set()
words_have_conflict_trees=set()

for index in range(len(NewForest)):

  tree=NewForest[index]

  word=''.join(tree.leaves())

  if word in Word2treeID:

    Word2treeID[word].add(index)

  else:
    Word2treeID[word]={index}


# check duplication
print('\nchecking conflicting trees for words:')

duplication_count=0
for word in Word2treeID:

  index_set=Word2treeID[word]

  if len(index_set)>1:

    duplication_count += len(index_set)

    words_have_multiple_trees.add(word)

    tree_list=[NewForest[index] for index in index_set]

    conflict=False
    d_tree=tree_list[0]

    for tree in tree_list[1:]:

      if d_tree!=tree:
        conflict=True

    if conflict:

      words_have_conflict_trees.add(word)

print('sample of conflicting trees: ')



for word in list(words_have_conflict_trees)[: min(10, len(words_have_conflict_trees))] :
	d_id_set=Word2treeID[word]
	tree_list=[NewForest[index] for index in d_id_set]
	
	print('\n',word)
	for tree in tree_list:
		print(tree)
                                            
print('\n\n># of words have conflict multiple trees=',len(words_have_conflict_trees))
print('# of word types in the annotation',len(Word2treeID))
print('the ratio of the two',len(words_have_conflict_trees)/len(Word2treeID))

print('\nMany conflicts only differ in the subscripts, most of which are just nnotation inconsistency ')
print('So we resolve this by keeping the tree, the root node of which has highest alphabetic order...')


word2uniqID_tmp={} #keep the uniq (chosen tree index) code for those words that have multiple trees
for word in words_have_multiple_trees:
  
  d_index_set=Word2treeID[word]

  d_list=[(index, NewForest[index]) for index in d_index_set]

  d_list.sort(key=lambda x: x[1].node)

  word2uniqID_tmp[word]=d_list[0][0]

  #print(word, d_list[0][0])



#
# update Word2treeID, to remove duplication and conflicts trees
#
for word in Word2treeID:

  index_list=list(Word2treeID[word])

  if len(index_list)==1:

    Word2treeID[word]=index_list[0]

  else:
    Word2treeID[word]=word2uniqID_tmp[word]

    



  
#
#  check whether there is any word type  (len>1) that has no annotation.  
#
print('\n\n\n>>> Checking the lexicon coverage of the trees, w.r.t. corpus lexicon')

Lexicon=set(Word2Tag.keys())
    
Uncovered=set()
SingleCharWord=set()

for i in Lexicon:
  if len(i)==1:
    SingleCharWord.add(i)

  elif not i in Word2treeID:
      Uncovered.add(i)


print('There are',len(Uncovered),' words uncovered by the annotation..., top 20 of which are:')
for i in list(Uncovered)[:min(20, len(Uncovered))]:
  print(i, Word2Tag[i])



#
# Do annotation for single-character word
#

print('\n\n\n>>>Generating word structure trees for single char character...')


for single_char_word in SingleCharWord:

  if single_char_word in UpdatedVec:
    tag_set=UpdatedVec[single_char_word]

  else:
    #tag_set=Word2Tag[single_char_word]
    print('Fail!')
    break

  tag_str=set2str(tag_set)

  tree_str='( '+tag_str+'_u '+single_char_word+' )'

  tree=ParentedTree(tree_str)

  index=len(NewForest)
  NewForest.append(tree)

  Word2treeID[single_char_word]=index

print('done! Such trees have been appended to NewForest, and word2treeId mapping has been stored in Word2treeID hashtable.')









#
# Generating mini-tree-sequence annotation of the word-segmented corpus
#
print('\n\n\n ====== Generating mini-tree sequence  ============')


word_tag_pattern=re.compile('(.+)_([A-Z]+)') #word_pos pair pattern


#def keep_all_subscript(tree, StrEncoder):
#  new_tree=tree.copy(deep=True)
#  for subtree in new_tree.subtrees():
#    subtree.node=StrEncoder.str2code(subtree.node)

#  return new_tree


# remove all subcript of the nodes in the tree
#def remove_all_subscript(tree, StrEncoder):
def remove_all_subscript(tree):
  #new_tree=ParentedTree(tree.pprint())
  new_tree=tree.copy(deep=True) 
  for subtree in new_tree.subtrees():
    tag, subscript=decompose_tag(subtree.node)
    #subtree.node=StrEncoder.str2code(tag)
    subtree.node=tag

  return new_tree


#def remove_crl_subscript(tree, StrEncoder):
def remove_crl_subscript(tree):
  new_tree=tree.copy(deep=True)
  for subtree in new_tree.subtrees():
    tag, subscript=decompose_tag(subtree.node)
    if subscript in {'l','r','c'}:
      subtree.node=tag

    else:
      subtree.node=subtree.node

  return new_tree
  

Corpus1=[]
Corpus2=[]
Corpus3=[]

RawCorpus=[]
path='../working_data/all.txt'
if len(sys.argv)>1:
  path=sys.argv[1]

print('\nReading word-segmented corpus from ',path, '...')

f=codecs.open(path, 'rU','utf-8')
lines=f.readlines()

count=0

is_corpus_tagged=True

for line in lines:
  if count%int(len(lines)/5)==0:
    print(int(count/len(lines)*100),'% finished...')

  count +=1

  tokens=re.findall('\S+', line, re.U)

  if is_corpus_tagged==True:
    word_tokens=[word_tag_pattern.match(token).group(1) for token in tokens]

  # it assumes the format of the input file is tha each token is made of word_tag format:
  # e.g. 上海_NR 浦东_NR 开发_NN 与_CC 法制_NN 建设_NN 同步_VV
  # i.e. we are using POS tagged version of CTB, of course, at this step, it is not necessary
  #       one could use word-segmented version as well.

    RawCorpus.append(word_tokens)

  else:
    RawCorpus.append(tokens)

print('done!')


print('\nGenerating three vesions of mini-tree-seq annotation...')

count=0

#Encoder1=Str2Hash()
#Encoder2=Str2Hash()
#Encoder3=Str2Hash()


for sent in RawCorpus:

  
  if count%int(len(lines)/10)==0:
    print(int(count/len(lines)*100),'% finished...')
  count +=1
  
  mini_tree_seq1=[]
  mini_tree_seq2=[]
  mini_tree_seq3=[]


  for word in sent:
    index=Word2treeID[word]
    tree=NewForest[index]

    mini_tree_seq1.append(tree.pprint(margin=10000))
    mini_tree_seq2.append(remove_all_subscript(tree).pprint(margin=10000))
    mini_tree_seq3.append(remove_crl_subscript(tree).pprint(margin=10000))

    #mini_tree_seq1.append(keep_all_subscript(tree, Encoder1).pprint(margin=10000))
    #mini_tree_seq2.append(remove_all_subscript(tree,Encoder2).pprint(margin=10000))
    #mini_tree_seq3.append(remove_crl_subscript(tree, Encoder3).pprint(margin=10000))


  Corpus1.append(mini_tree_seq1)
  Corpus2.append(mini_tree_seq2)
  Corpus3.append(mini_tree_seq3)

print('\ndone!')
    

p2='../working_data/corpus1.mts'
p3='../working_data/corpus2.mts'
p4='../working_data/corpus3.mts'

if len(sys.argv)>4:
  p2=sys.argv[2]
  p3=sys.argv[3]
  p4=sys.argv[4]

print('\n\nWriting corpus1/2/3 to ',p2,p3,p4, 'respectively')


def write_mst_corpus(Corpus, file):

  f=codecs.open(file,'w','utf-8')
  for sent in Corpus:
    f.write(' '.join(sent)+'\n')

  print(file, ' written: done!')

write_mst_corpus(Corpus1, p2)
write_mst_corpus(Corpus2, p3)
write_mst_corpus(Corpus3, p4)


