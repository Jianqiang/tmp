#
# B_convert_psd_sent_2_segmentation.py
#

'''
convert the parsing results to segmentations

'''

from nltk import Tree

def convert_psd_sent_2_segmentation(parsed_corpus):

  SegCorpus=[]
  
  for top_k_psd_of_the_sent in parsed_corpus:
    segmentation=[]
    
    best_score, best_parse_tree_str= top_k_psd_of_the_sent[0]
    tree=Tree(best_parse_tree_str)

    # tree=ROOT,  tree[0]=S,  tree[0, ] is the subtrees of S, i.e. POS tags, we can use alternative methods
    # note that it is highly dependent on the format of the parser outputs!!
    for subtree in tree[0,]:
      segmentation.append(''.join(subtree.leaves()))

    SegCorpus.append(segmentation)

    if not ''.join(segmentation)==''.join(tree.leaves()):
      print('Error! Leaves/characters in thee segmentation != total characters in the tree (as leaves), Double check the format and/or code!')
      break


  return SegCorpus
                  

  
#alternative implementation ofconvert_psd_sent_2_segmentation   
def convert_psd_sent_2_segmentation_2(parsed_corpus):

  SegCorpus=[]
  
  for top_k_psd_of_the_sent in parsed_corpus:
    segmentation=[]
    
    best_score, best_parse_tree_str= top_k_psd_of_the_sent[0]
    tree=Tree(best_parse_tree_str)

    # tree=ROOT,  tree[0]=S,  tree[0, ] is the subtrees of S, i.e. POS tags, we can use alternative methods
    # note that it is highly dependent on the format of the parser outputs!!
    for subtree in tree.subtrees(lambda t: t.height()==tree.height()-2):
      segmentation.append(''.join(subtree.leaves()))

    SegCorpus.append(segmentation)

    if not ''.join(segmentation)==''.join(tree.leaves()):
      print('Error! Leaves/characters in thee segmentation != total characters in the tree (as leaves), Double check the format and/or code!')
      break
    
  return SegCorpus
