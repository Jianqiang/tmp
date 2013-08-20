#
# 4_mini_tree_seq_gen.py
#

import re
import pickle
#from nltk import Tree
from nltk import ParentedTree


from utility_proj import set2str
#from utility_proj import str2set



print('\n>>>Running mini_tree_seq_gen.py, generates sentences that are sequences of mini-trees. Each tree represents the structure of a word.')


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

  tag_set=Word2Tag[single_char_word]
  tag_str=set2str(tag_set)

  tree_str='( '+tag_str+'_u '+single_char_word+' )'

  tree=ParentedTree(tree_str)

  index=len(NewForest)
  NewForest.append(tree)

  Word2treeID[single_char_word]=index

print('done! Such trees have been appended to NewForest, and word2treeId mapping has been stored in Word2treeID hashtable.')
  


