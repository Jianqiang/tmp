#
# X_baseline_grammar.py
#

'''
implement a baseline grammar from the original annotation
(pre-processed by 1_pre_proc_annotation.py to comply with PTB format,
defaul file: annotation_nltk.data)



dependency: this code needs the result word2newtag.pickle from running 2a_gen_tag_set_for_word_type.py 
'''

import nltk

import codecs
import sys
import pickle


print('\n\n>>>Running X_baseline_grammar.py, which gen a baseline grammar directly from the word-struture annotaiton')
print('Optional Argv: 1. proprocessed_word_structure_annotation,  2.word2tag mapping')

path_annotation='../working_data/annotation_nltk.data'
if len(sys.argv)>1:

  path_annotation=sys.argv[1]


print('\n\nprocessing annotation from ', path_annotation, '...  \nprograss:')
f=codecs.open(path_annotation, 'rU', 'utf-8')
lines=f.readlines()
f.close()

Production=[]

count=0
total_nth=int(len(lines)/10)
for line in lines:
  if count%total_nth==0:
    print(count/total_nth*10, '% finished')
  count +=1

  tree_string='( W '+line.strip()+' )'  #W is the extra root node (to indicate it is a word)

  tree=nltk.Tree(tree_string)

  tree.collapse_unary(collapsePOS = False) # collapting unary rule is not neccessary for this annotation
  tree.chomsky_normal_form(horzMarkov = 2) # binarization seems to be unnecesary for this annotation

  Production +=tree.productions()

print('done!')

#
# gen single-char annotation from the corpus
#

print('\n\ngenerating rules for single-char words from corpus')

#---> one needs to run 2a_gen_tag_set_for_word_type.py to gen word2newtag.pickle before using it
path_word2newtag='../working_data/word2newtag.pickle'



if len(sys.argv)>2:
  path_word2newtag=sys.argv[2]

print('\nreading (intermedidate reuslt) Word2NewTag hashtable from ', path_word2newtag)
f=open(path_word2newtag, 'rb')

Word2NewTag=pickle.load(f) # word2Newtag, dict: key=word  value=set of possible tags
f.close()

#Annotation_singleCharWord=[]  #no use so far, so blocked
Production_singleCharWord=[]

for word in Word2NewTag:
  if len(word)==1:
    tag_set=Word2NewTag[word]

    for tag in tag_set:

      tree_string='( W ( '+tag+'_u  '+word+' ) )'

      #Annotation_singleCharWord.append(tree_string)

      tree=nltk.Tree(tree_string)

      tree.collapse_unary(collapsePOS = False)
      tree.chomsky_normal_form(horzMarkov = 2)

      Production_singleCharWord += tree.productions()
      
      

print('done!')


#merge productions
Production += Production_singleCharWord


#
# inducing PCFG from the productions
#
print('\n\nInducing PCFG from the producitons occurre the treebank...')

W=nltk.Nonterminal('W')

baseline_grammar=nltk.induce_pcfg(W, Production)

print('done!')

path_grammar='../working_data/baseline.grammar.pickle'

print('\nSaving the induced grammar to',path_grammar,' ...')
f=open(path_grammar, 'wb')
pickle.dump(baseline_grammar, f)
f.close()
   
  

