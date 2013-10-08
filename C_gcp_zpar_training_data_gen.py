#
# C_gcp_zpar_training_data_gen.py
#

'''
generate training data for Zpar, for the global constituent parsing model (gcp),

just like B_***.py serie codes
'''

import codecs
import sys
#import pickle
import re
import nltk

tag_word_pattern=re.compile('(.*)_([A-Z]*)')

class FlatTreeGen():

  def __init__(self):
    self.word2bracketed={}
    self.pos_corpus=[]
    self.annotation=[]

  def read_posCorpus(self, path_to_corpus):
    print('\n>reading pos-corpus from',path_to_corpus)
    f=codecs.open(path_to_corpus, 'rU','utf-8')
    self.pos_corpus=[[(tag_word_pattern.match(token).group(1), tag_word_pattern.match(token).group(2)) for token in line.split()] for line in f.readlines()]
    f.close()


  #getting word2tree method 2: from bracketed plain text representation of tree to get Word2Tree
  def build_word2tree_from_bracketed_txt(self, path_bracketed_text):
    print('\n\n>>building word2tree from bracketed plain text representation of trees')
    f=codecs.open(path_bracketed_text, 'rU','gb2312')   
    self.word2bracketed={ line.split()[0]:' '.join(line.split()[1:])  for line in f.readlines()}

  def gen_n_write_sent_flat_tree(self, path_to_out_annotation):

    print('\n>generating sent-level flat trees...')
    for line in self.pos_corpus:
      tmp_str=''.join([' ( S ']+[' ( '+pos_tag+'P '+self.word2bracketed[word]+' ) ' for (word, pos_tag) in line ]+[' ) '])

      #tree=nltk.Tree(tmp_str)
      #tree.chomsky_normal_form(factor = "left", horzMarkov = 0, vertMarkov = 0, childChar = "|", parentChar = "^")
      #tree.chomsky_normal_form(factor = "left", horzMarkov = 2, vertMarkov = 0, childChar = "B", parentChar = "^")
      #tree_str=tree.pprint(margin=100000)
      #new_str=' '.join([i[:-2]+' '+i[-1] if len(i)>1 and i[-2]=='_'  and i[-1] in {'b','i'} else i for i in tmp_str.split()])+'\n'
      #new_str=' '.join([i[:-2]+' '+i[-1] if len(i)>1 and i[-2]=='_'  else i for i in tree_str.split()])+'\n'

      self.annotation.append(tmp_str)
      #self.annotation.append(new_str)


    print('done!\n>writing the annotation to ', path_to_out_annotation)
    f=codecs.open(path_to_out_annotation, 'w', 'gb2312')
    for sent in self.annotation:
      f.write(sent)
    print('done!')




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
      FTG.gen_n_write_sent_flat_tree(prefix+identity+'.a'+str(x+1)+'.treebank')  


print('\n\n>>>Running  gcp_zpar_training_data_gen...')
#p_train='../working_data/train.ctb5.pos'
p_train='../working_data/top10.tmp'
trait=['raw.train.zpar']
prefix='../working_data/'

flag_split=False

if flag_split:
  p_train='../working_data/train.ctb5.pos.split.new'
  trait=['split.train.zpar']

p_annotation1='../working_data/word_str_annotation1.zpar'
p_annotation2='../working_data/word_str_annotation2.zpar'
p_annotation3='../working_data/word_str_annotation3.zpar'


path_corpora=[p_train]
#path_annotations=[p_annotation1, p_annotation2, p_annotation3]
path_annotations=[p_annotation1]

flat_treebank_gen(path_annotations, path_corpora, trait, prefix)

    
