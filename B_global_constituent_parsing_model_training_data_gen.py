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

print('Optional Argv: 1. proprocessed_word_structure_annotation,  2.word2tag mapping,   3 training_corpus (.pos)')

path_annotation='../working_data/annotation_nltk.data'
if len(sys.argv)>1:

  path_annotation=sys.argv[1]


print('\n\nprocessing annotation from ', path_annotation, '...  \nprograss:')
f=codecs.open(path_annotation, 'rU', 'utf-8')
lines=f.readlines()
f.close()
