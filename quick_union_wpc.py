#
# quick_union_wpc.py
#

'''
weighted quick_uninon with path compression algorithm (a efficient find_union method).

adapted from slides http://www.cs.princeton.edu/~rs/AlgsDS07/01UnionFind.pdf

'''

class QuickUnion:
  
  def __init__(self,num_of_item):
    
    self.d_id=[i for i in range(num_of_item)] #init  id of each item
    self.size=[1 for i in range(num_of_item)]

  def get_root(self,item):
    while item!=self.d_id[item]:
      self.d_id[item]=self.d_id[self.d_id[item]] #path compression: point the id to the id of its pareent, to flat the tree
      item=self.d_id[item]
    return item

  def find (self, p, q):
    return (self.get_root(p)== self.get_root(q))

  def union(self, p, q):
    i=self.get_root(p)
    j=self.get_root(q)

    if self.size[i]<self.size[j]:  #weighting: merge smaller trees to smaller trees
      self.d_id[i]=j
      self.size[j] +=self.size[i]
    else:
      self.d_id[j]=i
      self.size[i] += self.size[j]


  def gen_equivalence_class(self):

    self.d_classTable={}

    for i in range(len(self.d_id)):
      d_class=self.d_id[i]

      if d_class in self.d_classTable:
        self.d_classTable[d_class].add(i)

      else:
        self.d_classTable[d_class]={i}

    return list(self.d_classTable.values())



if False:   #test example  
  Q=QuickUnion(10)

  seq=[(3,4),(4,9),(8,0),(2,3),(5,6),(5,9),(7,3),(4,8),(6,1)]
  for i in seq:
    Q.union(i[0],i[1])
    print(Q.d_id)

  print('\n')
  d=Q.gen_equivalence_class()
  for i in d:
    print(i)
    #print(d[i])


