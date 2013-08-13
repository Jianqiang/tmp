#
# tag_vector_propagation.py
#
'''
=========  Algorithms for tag vector propagation =========

Input: A forest/set (F) of character trees (T) that describe the word structure, with headness annotation. e..g

For  each binary branching  (X (L) (R) ), we don't know the tag of any node, rather, we know X.head==L, R or C (i.e. coordinate, ==left& right direction) .   #X.head= Tree.node.subscript
We also know the tag vector of the root of each Tree, which represents a word.

Output: A updated hashtable Vec, key: a string, could be word/sub-word/character, value:set of tags that has been co-occurred with the key
The tag vector are propogated from higher node in the tree to its 'head children'. And the update is based on type and done in a accumulative manner,
i.e. each (sub)tree of a string should have the same tag-vector.



>>> Implementation based on a NLTK-style Tree structure implementation


Data Structure:  
Vec, a hashtable, key: a string, representing a word, sub-word or character.  value: set of tags that has been co-occurred with the key

Symbol, a set to record all the character, words and sub-words.

Each node of the tree has .symbol,  .vec , .head , attributes, which represents the symbol(word, subword, character) presented by the node, the tag vector of that node, and the head (which links to one or two  of its children)

A stack S is needed to keep the sub-trees to be processed
A  variable tag_set is needed to record the set of tags from the root to be updated for sub-tree nodes.


1. Unpickle  Word2NewTag, from the result from 2.a (word2newtag.pickle)

2. Initialize Vec, by copy keys from Word2NewTag, and associate them with the set(Word2NewTag[key]), i.e. converting the list into set.

3. Actual propagation, algorithm design using Tree data structure:

For each T(ree) in Forest:

    T_symbol=''.join(T.leaves())  #T.leaves gives back a list, but we need a str   
    
    tag_set=Vec[T_symbol]  # update the tagset of each "head child" with this tagset

    S.push(T)


    while S:  # while S is not empty

        C=S.pop()    # C is the current (sub)tree 
        C_symbol=''.join(C.leaves())
        Vec[C_symbol].update(tag_set)
        
        if C.height()>2:  # C is not a leave/string, but a non-terminal
            head_children=get_head_child(C) 
            if  head_children: #set of head-children is non-empty
                for Child in head_child:
                    S.push(Child)
            else:
                print('Error! No head-children found in tag_propagation! \nProgram Exit. ')
                break
                       

using regular expression pattern=re.compile('([A-Z]+)_([a-z]+)')
write a get_head_children function, the code should be self-explanative.

'''

import pickle
import re
import sys
import codecs
from nltk import Tree
from nltk import ImmutableParentedTree


pattern=re.compile('([A-Z]+)_([a-z]+)') # the pattern of tree nodes (tags), compiled, as will be called repeatedly


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

# 
# -------------------> start the main procedure <------------------#
#

p1='../working_data/word2newtag.pickle'
p2='../working_data/taglist.pickle'

print('\n===== Running tag_vector_propogation.py, which propogate tag-vector/set top-down, from parent to head-children...')

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


#Initialization Vec with unpickled Word2NewTag hashtable generated from the last step
print('\nInitializing Vec hashtable...')
for key in Word2NewTag:
  Vec[key]=set(Word2NewTag[key])
print('done.')






#
# tag-vector propagation...
#
print('\nMain procedure: Propogating Tag-vectors topdown, tree by tree...')



count=0
not_covered=0 #those annotation, the words of which have not occurred in our corpus

Symbols=set()
Symbols2=set()

OOV=set()
           #
Forest=[]  # list of parsed trees, an output of this program
           #
            

for sent in Annotation:

  S=[] # S is the stack for tree node visit
  
  tree=ImmutableParentedTree(sent)  #using NLTK.Tree data structure, representing the tree


  #
  #count unique strings(leaves) associated with subtrees
  #



  #print(tree)
  #print(tree.leaves())

  string=''.join(tree.leaves())

  #If the word has occurred in the corpus...
  
  if string in Vec:

    Forest.append(tree)

    

    tag_set=Vec[string]
    
    S.append(tree)

    for s in tree.subtrees():
      Symbols2.add(''.join(s.leaves()))

    while S:

      current_tree=S.pop()

      string=''.join(current_tree.leaves())

      Symbols.add(string)


      # propogate the tagset to current tree, note: one useless update for the root node
      if string in Vec:
        Vec[string].update(tag_set)
      else:
        Vec[string]=tag_set


      #top-down visit the sub-trees that correspond to words or subwords
      if current_tree.height()>2:

        #print('##CurrentTree=',current_tree,'  height=',current_tree.height())

        head_children=get_head_children(current_tree) #get head-children by calling the same-name function


        if  head_children: #if the list of head-children is non-empty
          for child in head_children:

            S.append(child)

        else:
          print('Error! No head-children found in tag-propagation!\nProgram Exit.')
          break
    
    
    count=count+1

    #displaying the progress
    if count%int(len(Annotation)/10)==0:
      print ('current tree leaves and tagset:',''.join(tree.leaves()),tag_set,' /--->',str(count/len(Annotation)*100)[:2], '% finished')


  #if the word has not occurred in the corpus (indicating coverage problem! Sth is wrong!)
  else:
    #print('word ',string, 'has not occurred in the corpus')
    not_covered +=1
    OOV.add(string)
    pass


print('done!')

print('\n>>Result of the Vec:')
#for i in Vec:
  #print(i, Vec[i])

print('Num of entries in Vec=',len(Vec))
print('Num of entries in Word2NewTag=',len(Word2NewTag))
print('Num of words in Annotation=', len(Annotation))

print('Num of words not in our corpus=',not_covered)
print('Non-coverage rate=',not_covered/len(Annotation))


'''
for i in Vec:
  if not i in Word2NewTag:
    print(i, Vec[i])
'''


print('\nFor those words that have occurred in the corpus, the covrage of all the subwords/characters after update is:', end=' ')
print(len(Symbols)/len(Symbols2))

#diff=Symbols2.difference(Symbols)
#for i in diff:
  #print(i)


diff2=Symbols2.difference(set(Vec.keys()))



print('\nCoverage for all the subtrees =', (len(Symbols2)-len(diff2))/len(Symbols2))

#print('\n\n>>>##Printing out OOVs...')
#for i in OOV:
#    print(i)
print('\nOOV rate of the annotation w.r.t. vocabulary extracted from corpus:', len(OOV)/len(Annotation))


print('\nSubtrees that have no tag-update:')
unicount=0
for i in diff2:
    if len(i)==1:
        unicount +=1
        #print (i)
print('unanalyzed single-character count=',unicount, '  % is ',unicount/len(diff2))


###########Output 1: tree representation of the annotation

p_tree='../working_data/annotated_trees.list.pickle'

print('\n\n>>>Store the tree representations of the annotation in ',p_tree)

f_tree=open(p_tree,'wb')
pickle.dump(Forest, f_tree)
f_tree.close()


#######Output 2: Vec hashtable, which keeps a mapping from string(char/word/subword) to their tag
p_vec='../working_data/string2tag.hash.pickle'
print('\n\n>>>Store the Vec hashtable, which keeps a mapping from string(char/word/subword) to their tag to file ',p_vec)

f_vec=open(p_vec, 'wb')
pickle.dump(Vec, f_vec)
f_vec.close()


      

