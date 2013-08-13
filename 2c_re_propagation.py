#
# 2c_re_propagation.py
#

'''
"Similarity-based 2nd-order Tag propagation"

A top-down similar production-rule based tag guessing (initial: with one-hot representation)


There are two types of unknown terminals in a production rule:

X --> L[?]  R |  L  R[?]

in which '?' marks the non-terminal (node) to be guessed


keep 2 hashtables for actually known nodes in a tree:

InduceLeftNode       # if tree.right_sibling and not(tree.left_sibing())
InduceRightNode     # if tree.left_sibling and not(tree.right_sibling())


key: known node, <X, R>, <X,L> and  for above 2 hashtable, respectively
value: list of actual tag for the pseudo-unknown node (i.e. L,R,for the above three tables, respectively

Algorithm Sketch:


1st pass:

process the annotated tree:
    for each head_children C (C.leaves.toString in Vec), 
           update the tag of the node with Vec[C.leaves.toString]  #get the aggregated tag
           
            update 2 hash tables.

     for each non-head children C
            copy the old_tags
  

batch processing: pass the each hashtable, re-set the value to x, which is the element has max count in the original value (list)


2nd pass:
top-down similarity based propagation

keep a set L_fail, R_fail, to keep record of update failures
keeps a counter, update_success,

process the annotated tree:
     for subtree:
         if the node is not a head_child:
              check whether possible to update with the tag by retrieving relevent Hashtable
              if doable:
                    do the update
                    update_sucucess++
              else:
                    add this instance to L_fail or R_fail according to their type



see how successful it is......

'''

#  Extra notes:
# 1. for a production X_sub ---> Y_sub  Z_sub, we consider it as X_sub --> Y  Z (ignore the subscript on the RHS)
# 2. we assume list.sort() works in a consistent manner, we sort and concatenate set of tags to make tag_vec
#    without mainting a global sorted tag list.
#



import re
import pickle
from nltk import Tree
from nltk import ImmutableParentedTree
from nltk import ParentedTree


pattern=re.compile('([A-Z]+)_([a-z]+)') # the pattern of tree nodes (tags), compiled, as will be called repeatedly



print('\n>>>Running re_propogation.py, A top-down similar production-rule based tag guessing code')
print('ak 2nd-order Tag propagation')


#
# Loading Forest of trees and Vec hashtable via pickle
#

p_tree='../working_data/annotated_trees.list.pickle'

print('\n>>>Loading the tree representations of the annotation from',p_tree,' ....', end='  ')
f=open(p_tree, 'rb')

Forest=pickle.load(f)  # Forest contains all the relevant annotations as a list of (ImmutableParented) trees
f.close()
print('done.')

p_vec='../working_data/string2tag.hash.pickle'
print('\n>>Loading the Vec hashtable, which keeps a mapping from string(char/word/subword) to their tag to file ',p_vec, end='...  ')

f=open(p_vec, 'rb')
Vec=pickle.load(f)
print('done.')
f.close()



#
# utilities
#

# convert a set of item to a single str representation
def set2str(d_set):
  new_list=[]
  new_list.extend(d_set)
  new_list.sort()

  return ''.join(new_list)  #might cause ambiguity in theory, but works OK with CTB tag set.



#decompose tags in the form  "tag_subscript"
def decompose_tag(complex_tag):
  match=pattern.match(complex_tag)

  try:
    match=pattern.match(complex_tag)
    
    tag=match.group(1)
    subscript=match.group(2)

    return tag, subscript

  except:
    print ('Error in tag format! The tag format is unrecognizable! e.g.',complex_tag)
    return False

#clean up error-handling later...


  

# a simple hashtable, value is a list of items
class Hash_list_value:

  def __init__(self):
    self.table={}

    

  def add_item(self, item, value):
    if not item in self.table:
      self.table[item]=[]
    #else, no need to create new entry

    self.table[item].append(value)

  def __getitem__(self, key):
    return self.table[key]

      
  
  # for each key, return the item in the value list, such that the count of that value is the max in the list
  def compute_max_hash(self):

    self.max_hash={}

    for item in self.table:
      d_list=self.table[item]

      local_hash={}
      d_set=set(d_list)
      for key in d_set:
        local_hash[key]=d_list.count(key)

      key_value_list=local_hash.items()

      sorted_key_value=sorted(key_value_list, key=lambda x: x[1], reverse=True)

      self.max_hash[item]=sorted_key_value[0][0]


    return self.max_hash
      




##################### Core Code Starts Here ######################


#
#two hashtables to record X->LR production rule patterns in the annotation
#
InduceLeftNode=Hash_list_value()
InduceRightNode=Hash_list_value()


NewForest=[] # keep updated trees

 


#
# 1st pass processing to update InduceLeftNode and InduceRightNode hashtables.
#

count=0
print('\n>>1st pass of process the trees')
for tree in Forest:

  count +=1
  if count%int(len(Forest)/10)==0:
      print('progress------->',str(count/len(Forest)*100)[:2], '% finished')


  new_tree=ParentedTree(tree.pprint())


  

  for subtree in new_tree.subtrees():  #update current tree

    string=''.join(subtree.leaves())

    if  string in Vec:  #leaves/string in the record

      tag, subscript= decompose_tag(subtree.node)

      match=pattern.match(subtree.node)

      tag_vec_str=set2str(Vec[string]) #get the tag-set of the node according to the leaves and convert it to str

      subtree.node=tag_vec_str+'_'+subscript  #update the node with the new_tag

      #print('\n')
      #print(subtree.node, ''.join(subtree.leaves()))


  for subtree in new_tree.subtrees(lambda x: len(x)>1 and ''.join(x.leaves()) in Vec ):  # extraction known production rules

    string=''.join(subtree.leaves())


    left_child=subtree[0]
    right_child=subtree[1]

    if ''.join(left_child.leaves()) in Vec and ''.join(right_child.leaves()) in Vec:  #Parent, LeftChidl and Rightchild are All known!
        
      
      #print(left_child.leaves(),left_child.node,  right_child.leaves(), right_child.node)

      l_tag, l_sub=decompose_tag(left_child.node)
      r_tag, r_sub=decompose_tag(right_child.node)

      key_l=subtree.node+'-'+r_tag
      InduceLeftNode.add_item(key_l, l_tag)

      key_r=subtree.node+'-'+l_tag
      InduceRightNode.add_item(key_r, r_tag)

'''
print('\n<<-----')
for i in InduceLeftNode.table:
  print(i, InduceLeftNode[i])


print('\n----->>')
for i in InduceRightNode.table:
  print(i, InduceRightNode[i])
        
'''
print('\nsome analytics:')
print(len(InduceLeftNode.table))
print(len(InduceRightNode.table))

x=InduceLeftNode.table.values()
y=set()

for i in x:
  for j in i:
    y.add(j)
  
  
z=list(y)
zz=sorted(z, key=lambda item:len(item))
for i in zz:
  print(i)
      
