#
#  Penn2Dep.py
#
'''
converting head-annotated CTB style trees to dependency graphs, and then convert them to brackted representation (of dp tree)

usage:
  from A_Penn2Dep import penn2depgraph(tree_str) #tree string is a consitituent tree represented by Penn bracket
  Node, dep=penn2depgraph(tree_str)
  dep_str=depgraph2bracket(Node, dep) # dep_str is the bracketed representation of the dependency tree
  

'''

import nltk

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


#
# convert Penn/CTB style bracketed notation to Dependency Graph
#
def penn2depgraph(tree_str):


  tree=nltk.ParentedTree(tree_str)
 

  
  Head2Node=dict() # key:head-word ---> value node
  Node2Head=dict() # key:node --> value: head



  for subtree in tree.subtrees():

    position=subtree.treeposition()
    subscript=subtree.node[-1]

    if subscript in {'l','b','i','u'} : # the left_child is the head
      Head2Node[left_child(position)]=position
      Node2Head[position]=left_child(position)

    elif subscript in {'r','c'}:                 ##### <<<-----  'c' here we consider it as "right-headed", but also OK to be "left-headed", as long as consistency is kept
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

  pos2code[max_code]=0

  #
  # note: we keep and deal with preTerminal positions rather than the leave positions.

  for i in range(len(pos)):
    #print(pos[i])
    leave_pos=tree.leaf_treeposition(i)
    pre_terminal_pos=get_parent_pos(leave_pos)

    pos2code[pre_terminal_pos]=i+1

    #print(pre_terminal_pos)
    #print(tree[pre_terminal_pos])

    higher_pos=leave_pos

    while higher_pos in Head2Node:
      higher_pos=Head2Node[higher_pos]    

    #print('its_highest_position=', higher_pos, tree[higher_pos])

    parent=tree[get_parent_pos(higher_pos)]
    if len(higher_pos)>0:

      parent_head=Node2PreTerminal[parent.treeposition()]

      dep_tmp.append((parent_head, pre_terminal_pos, parent.node))
      #print('its_parent:',parent_head, tree[parent_head], '#######',parent, 'rel-type=',parent.node,'\n')

    #else: 
      #print('its_parent:  ROOT;  rel-type=Root','\n')
      #dep_tmp.append((max_code,pre_terminal_pos, 'ROOT'))

    #print('>>>', higher_pos,'<<<')

  Node=[(0,'Root')]
  Node.extend((i+1, pos[i] ) for i in range(len(pos)))
  #Node={(i+1, pos[i] ) for i in range(len(pos))}
  #Node.add((0, 'Root'))

  dep=[(pos2code[i[0]], pos2code[i[1]], i[2] ) for i in dep_tmp]
  #print('\nNode:')
  #for i in Node:
    #print(i)

  #print('\>Dependencies:')
  #for i in dep:
    #print(i)

  return Node, dep



#
# convert (un-typed) dependencies to bracketed format  
#
# eg: ((``/``) ((The/DT) (equity/NN) market/NN) was/VBD (illiquid/JJ) (./.))

'''
#idea: #of '(' to the left of the node == 1+#_of_incoming_left_edge,    if there is NO outgoing edge
                                          #_of_incoming_left_edge,      if it has outgoing dep edges

       # of ')' to the right of the node == 1+ #_of_incoming_right_edge  if there is NO outgoing edge
                                          #_of_incoming_left_edge,      if it has outgoing dep edges 

                                          
'''

def depgraph2bracket(Node, dep):

  Head2Mod=dict()
  for i in dep:
    
    head=i[0]
    if head>0:
      mod=i[1]

      if not head in Head2Mod:
        Head2Mod[head]=set()
      Head2Mod[head].add(mod)

  Head2LRboundary={i:(min(Head2Mod[i]) if min(Head2Mod[i])<i else i, max(Head2Mod[i]) if max(Head2Mod[i])>i else i) for i in Head2Mod}


  left_bracket_count=[0 for i in range(len(Node))]  
  right_bracket_count=[0 for i in range(len(Node))]


  for node in Node[1:]:  # skip the root node
    node_id=node[0]

    if not node_id in Head2LRboundary:
      left_bracket_count[node_id] += 1
      right_bracket_count[node_id] += 1

    else:
      left_bracket_count[Head2LRboundary[node_id][0]] += 1
      right_bracket_count[Head2LRboundary[node_id][1]] += 1

  dep_str=''
  for node in Node[1:]:
    node_id=node[0]
    dep_str += left_bracket_count[node_id]*' ( '

    dep_str += node[1][0]+'/'+node[1][1]

    dep_str += right_bracket_count[node_id]*' ) '

  #print(dep_str)
  return dep_str


  
  
def test():
  tree_str='(  NN_l  (  NN_r  (  NN_b  冰  )  (  NN_i  冻  )  )  (  NN_r  (  NN_i  三  )  (  NN_i  尺  )  )  )'
  #tree_str='(  NN_r  (  NN_l  (  NN_b  水  )  (  NN_i  手  )  )  (  NN_i  们  )  ) '
  #tree_str=' (  CD_c  (  CD_c  (  CD_c  (  CD_b  二  )  (  CD_i  千  )  )  (  CD_i  一  )  )  (  CD_i  百  )  )'
  
  #tree=nltk.ParentedTree('(  NN_r  (  NN_r  (  NN_r  (  NN_b  博  )  (  NN_i  物  )  )  (  NN_i  馆  )  )  (  NN_i  界  )  )')
  #tree=nltk.ParentedTree('(NN_u 水 )')

  Node, dep=penn2depgraph(tree_str)
  dep_str=depgraph2bracket(Node, dep)
  #print(dep_str)


#test()


  

      

      
