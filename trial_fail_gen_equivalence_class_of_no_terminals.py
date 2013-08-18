#
# 2d_gen_equivalence_class_of_non_terminals.py
#

'''
define a equivalent relation, denoted as "~" on non-terminals node.
1. binary branching P -->  L  R,  the set of head-children HC is a subset of {L,R},
   for each H in HC, we have  H ~ P

2. unary branching P --> U, we have P ~ U

3. nodes that have same leave types, i.e. if X.leaves=Y.leaves, we have X ~ U

In fact, from 3, we could start from the point where we treet nodes that yield same leaves as equivalent.


will try both top-down and bottom-up visit the tree.

top-down: root/word tag is given, they define the initial equivalent class (those roots have same tag are equivalent)

bottom-up: those uniray branching that yield same characters are equivalent, no root tag is used.
(this maybe more narrow...)

We implement this based on weighted quick_uninon with path compression algorithm (quick_union_wpc.py)

for each pair of equivalent relation, we do the Union operation

After visit the forest of trees, we have final equivalence class

'''
import pickle
import re
import sys
import codecs
from nltk import Tree
from nltk import ImmutableParentedTree

from quick_union_wpc import QuickUnion  #the quick-union implementation

pattern=re.compile('([A-Z]+)_([a-z]+)') # the pattern of tree nodes (tags), compiled, as will be called repeatedly


# -------- the following lines are copied from 2b_tag_vector_propagation.py to reduce dependencies ----------


#  !!! Start of Copy ------>

#
# function for finding the "head-children" of a tree (that represents word/subword, i.e. not a mini tree that only covers one single char)
#
def get_head_children(C):  # C is a tree/subtree

    head_children=[]

    match=pattern.match(C.node)

    if match:

        head_para=match.group(2)

        #right headed
        if head_para=='r':
            head_children.append(C[1])

        #left headed
        elif head_para=='l':
            head_children.append(C[0])

        #coordinate structure
        elif head_para=='c':
            #print(C[0])
            #print(C[1])
            head_children.append(C[0])
            head_children.append(C[1])
    else:
        print ('Error in get_head_children! The tag format is unrecognizable! e.g.', C.node)


    return head_children


p1='../working_data/word2newtag.pickle'
p2='../working_data/taglist.pickle'


p_annotation='../working_data/annotation_nltk.data'
print('\nArg: word_structure_annotation file. If no arg is provided, will use', p_annotation)


if len(sys.argv)>1:
  p_annotation=sys.argv[1]

print('\nLoading word-structure annotation from ',p_annotation)
f=codecs.open(p_annotation,'rU','utf-8')
Annotation=f.readlines()
f.close()
print('completed')

print('\nLoading word2newtag dictionary from ',p1)

f=open(p1,'rb')
Word2NewTag=pickle.load(f)
f.close()
print('completed')

        #
Vec={}  # main data structure of this code, the hashtable to keep the tag-vector propogation result,
        #key: a string, representing a word, sub-word or character.
        #value: set of tags that has been co-occurred with the key




# -------------------> End of Copy !!!!





########  Actual Code for Gen Equivalence Class Below (top-down approach) ###########


#Initialization Vec with unpickled Word2NewTag hashtable generated from the last step
#And build Word2Code, map strings to integers

#hastable keeps a mapping from string to int code


Str2Code={} 
type_count=0

Code2Str={}



for key in Word2NewTag:
  tag_collapsed='Z'.join(Word2NewTag[key])
  Vec[key]=tag_collapsed
  
print('done.')



Forest=[]
Tag2Word={}

# 1st pass: collect all strings that can be yielded from nodes of the trees
#           to update Str2Code

iter_count=0
print('First pass to collect all strings... ')
for sent in Annotation:

  iter_count +=1

  if iter_count%int(len(Annotation)/10)==0:
      print(iter_count/len(Annotation),'% having been processed ...')

  tree=ImmutableParentedTree(sent)

  word=''.join(tree.leaves())

  if word in Vec:  # word in the scope of our vocabulary/corpus, go on (ignore others)

    tag_collapsed=Vec[word]

    if tag_collapsed in Tag2Word:
      Tag2Word[tag_collapsed].add(word)
    else:
      Tag2Word[tag_collapsed]={word}


    Forest.append(tree)

    for subtree in tree.subtrees():

      string=''.join(subtree.leaves())

      if not string in Str2Code:
        Str2Code[string]=type_count
        Code2Str[type_count]=string
        type_count +=1

        

    

print('\nCurrent type count is:', type_count)
print('while current Vec size is:', len(Vec))
print('tmp test', type_count,len(Str2Code))


#
# EquivalenceClass init.
#  by joining words that are of same tag(vector)
#

Q=QuickUnion(len(Str2Code)) #quick union class, the data structure/algori to construct equivalence class



###########################
#
# --> True: top-down, using word type vector to start with; False: bottom-up, only using same-character and co-ordinate structure to boost
#
#############################

if True:  # False:don't do initilaization, i.e. do not use word-tag information


    print('\nEquivalenceClass initilization by UNION of words of same tag vectors')
    print('should yield ', len(Tag2Word), ' EqClass in the end')

    for i in Tag2Word:

        word_list=list(Tag2Word[i])

        first_code=Str2Code[word_list[0]]

        for j in word_list[1:]:

            code=Str2Code[j]
            Q.union(first_code, code)


    tmp_result=Q.gen_equivalence_class()
    print('done!',len(tmp_result),'equivalence class are constructed.')



        




#
#2nd pass to do the union operation for all the nodes that are equivalent


            
print('\nprocessing the 2nd pass to construct the Equivalence Class...')

iter_count=0
for tree in Forest:

  iter_count +=1
  if iter_count%int(len(Annotation)/10)==0:
      print(iter_count/len(Annotation),'% having been processed ...')

  S=[]  #S is the stack to keep track of node visit

  S.append(tree)

  while S:

    current_tree=S.pop()

    if current_tree.height()>2:

      head_children=get_head_children(current_tree)

      for child in head_children:

        S.append(child)

        p_string=''.join(current_tree.leaves())

        c_string=''.join(child.leaves())

        Q.union(Str2Code[p_string], Str2Code[c_string])



C=Q.gen_equivalence_class()
print(len(C))
  

    



    






  
