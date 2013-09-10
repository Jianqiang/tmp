#
#  Penn2Dep.py
#
'''
converting head-annotated CTB style trees to dependency trees

'''

import nltk

tree=nltk.ParentedTree('(  NN_r  (  NN_l  (  NN_b  水  )  (  NN_i  手  )  )  (  NN_i  们  )  ) ')
#tree=nltk.ParentedTree('(NN_u 水 )')

# visit (binary) tree in post-oder

#Node2HeadLeave=dict()

#LeavePos2HighestNodePos=dict() # position of leave to its highest node
Head2Node=dict() # key:head-word ---> value node
Node2Head=dict() # key:node --> value: head

def get_parent_pos(tree_pos):
  x=list(tree_pos)
  return tuple(x[:-1])

def left_child(tree_pos):

  x=list(tree_pos)
  x.append(0)

  return tuple(x)


def right_child(tree_pos):
  x=list(tree_pos)
  x.append(1)

  return tuple(x)


for subtree in tree.subtrees():

  position=subtree.treeposition()
  subscript=subtree.node[-1]

  if subscript in {'l','c','b','i','u'} : # the left_child is the head
    Head2Node[left_child(position)]=position
    Node2Head[position]=left_child(position)

  elif subscript=='r':
    Head2Node[right_child(position)]=position
    Node2Head[position]=right_child(position)

  else:
    print('Error! Unknown subscript!')
    break
    
    


pos=tree.pos()

#Pos2Leave=dict()

Node2PreTerminal={}
for node in Node2Head:
  head=Node2Head[node]

  while head in Node2Head:
    if type(tree[Node2Head[head]])!=str:
      head=Node2Head[head]
    else:
      break

  Node2PreTerminal[node]=head

pos2code=dict()
dep_tmp=[]
max_code=len(pos)

pos2code[max_code]=max_code

#
# note: we keep and deal with preTerminal positions rather than the leave positions.

for i in range(len(pos)):
  print(pos[i])
  leave_pos=tree.leaf_treeposition(i)
  #pre_terminal_pos=tree.treeposition_spanning_leaves(i, i+1)
  
  #tmp=list(leave_pos)
  pre_terminal_pos=get_parent_pos(leave_pos)

  pos2code[pre_terminal_pos]=i

  print(pre_terminal_pos)
  print(tree[pre_terminal_pos])

  higher_pos=leave_pos

  while higher_pos in Head2Node:
    higher_pos=Head2Node[higher_pos]

  #Node2Leave[higher_pos]=leave_pos

  

  print('its_highest_position=', higher_pos, tree[higher_pos])

  parent=tree[get_parent_pos(higher_pos)]
  if len(higher_pos)>0:

    parent_head=Node2PreTerminal[parent.treeposition()]

    dep_tmp.append((parent_head, pre_terminal_pos, parent.node))
    print('its_parent:',parent_head, tree[parent_head], '#######',parent, 'rel-type=',parent.node,'\n')
  else:
    print('its_parent:  ROOT;  rel-type=Root','\n')

    dep_tmp.append((max_code,pre_terminal_pos, 'ROOT'))

  print('>>>', higher_pos,'<<<')


Node={(i, pos[i] ) for i in range(len(pos))}
Node.add((max_code, 'Root'))

dep=[(pos2code[i[0]], pos2code[i[1]], i[2] ) for i in dep_tmp]
print(Node)
print(dep)

  

      

      

      
