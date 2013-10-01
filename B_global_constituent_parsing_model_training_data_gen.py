#
# B_global_constituent_parsing_model_training_data_gen.py
#

'''
reading training corpus and generate flat trees using word structure annotation;
then writing the result to PTB bracket format.

prerequisit: word-structure annotation

'''

import nltk

import codecs
import sys
import pickle
import re


tag_word_pattern=re.compile('(.*)_([A-Z]*)')

print('Optional Argv: 1. proprocessed_word_structure_annotation,  2.word2tag mapping,   3 training_corpus (.pos)')

path_annotation='../working_data/annotation_nltk.data'
if len(sys.argv)>1:

  path_annotation=sys.argv[1]


print('\n\nprocessing annotation from ', path_annotation, '...  \nprograss:')
f=codecs.open(path_annotation, 'rU', 'utf-8')
lines=f.readlines()
f.close()

#need:  word2tree: hashtable, key: word, value: NLTK Tree of that word

class FlatTreeGen():

  def __init__(self):
    self.Word2Tree={}
    self.pos_corpus=[]
    self.annotation=[]

  def read_posCorpus(self, path_to_corpus):
    print('\n>reading pos-corpus from',path_to_corpus)
    f=codecs.open(path_to_corpus, 'rU','utf-8')
    self.pos_corpus=[[(tag_word_pattern.match(token).group(1), tag_word_pattern.match(token).group(2)) for token in line.split()] for line in f.readlines()]
    f.close()

  # getting word2tree method 1: from .pickle file load Word2Tree, if it is already gen
  def load_word2tree_from_pickle(self, path_to_word2tree_pickle):
    print('\n\n>>loading word2tree from pickel file ', path_to_word2tree_pickle,'...')
    f=open(path_to_word2tree_pickle, 'rb')
    self.Word2Tree=pickle.load(f)
    f.close()

  #getting word2tree method 2: from bracketed plain text representation of tree to get Word2Tree
  def build_word2tree_from_bracketed_txt(self, path_bracketed_text):
    print('\n\n>>building word2tree from bracketed plain text representation of trees')
    f=codecs.open(path_bracketed_text, 'rU','utf-8')   
    Forest=[nltk.Tree(tree_str) for tree_str in f.readlines()]
    self.Word2Tree={''.join(tree.leaves()):tree for tree in Forest}

  def gen_n_write_sent_flat_tree(self, path_to_out_annotation):

    print('\n>generating sent-level flat trees...')
    self.annotation=[[' ( ( S ']+[' ( '+pos_tag+'POS  '+self.Word2Tree[word].pprint(margin=10000)+' ) ' for (word, pos_tag) in line ]+[' ) ) \n'] for line in self.pos_corpus]

    print('done!\n>writing the annotation to ', path_to_out_annotation)
    f=codecs.open(path_to_out_annotation, 'w', 'utf-8')
    for sent in self.annotation:
      f.write(' '.join(sent))
    print('done!')

  

#test..
p_dev='../working_data/dev.ctb5.pos.split'  # added .split, to use the splitted version
p_test='../working_data/test.ctb5.pos.split'
p_train='../working_data/train.ctb5.pos.split'

p_annotation1='../working_data/word_str_annotation1.txt'
p_annotation2='../working_data/word_str_annotation2.txt'
p_annotation3='../working_data/word_str_annotation3.txt'


prefix='../working_data/'

trait=['train','test','dev']
path_corpora=[p_train, p_test, p_dev]
path_annotations=[p_annotation1, p_annotation2, p_annotation3]

def flat_treebank_gen(p_annotations, p_corpora, trait, prefix):

  print('\n\n>>>Generating flat_treebanks using word structure annonotation in', [i.split('/')[-1] for i in p_annotations ], ' for following corpora:',[i.split('/')[-1] for i in p_corpora ] )
  print('')
  #prefix='../working_data/'
  
  for x in range(len(p_annotations)):
    annotation=p_annotations[x]
    
    FTG=FlatTreeGen()
    FTG.build_word2tree_from_bracketed_txt(annotation)

    for i in range(len(path_corpora)):
      corpus=path_corpora[i]
      identity=trait[i]

      FTG.read_posCorpus(corpus)
      FTG.gen_n_write_sent_flat_tree(prefix+identity+'.a'+str(x+1)+'.gcp.txt.split')  #!!! added .split suffix

    
flat_treebank_gen(path_annotations, path_corpora, trait, prefix)

    
