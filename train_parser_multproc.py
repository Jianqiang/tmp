#
# train_parser_multiproc.py
#


from multiprocessing import Process
import os
import sys
import codecs
import time


def do_training( parameter_str, training_corpus, max_mem):
  #model, input_corpus, parsed_corpus= the_argv
  print(str(parameter_str))
  print(training_corpus)
  real_path=os.path.realpath(training_corpus)
  prefix='/'+'/'.join(real_path.split('/')[:-1])
  corpus_name=real_path.split('/')[-1].replace('.','')

  grammar_file=prefix+'/'+'G_'+corpus_name+'_'+''.join(parameter_str.split()).replace('-','')+'.ser.gz'
  
  
  cmd='java -server -mx'+max_mem+ ' -cp  stanford-parser.jar edu.stanford.nlp.parser.lexparser.LexicalizedParser  -encoding UTF-8 -headFinder edu.stanford.nlp.trees.LeftHeadFinder '
  cmd += parameter_str+' -saveToSerializedFile '+grammar_file+' -train '+training_corpus
  os.system(cmd)

def get_training_corpora(path_to_training_file):
  f=codecs.open(path_to_training_file,'rU','utf-8')
  corpora=[line.strip() for line in f.readlines()]
  return corpora

def get_parameter_set(path_to_parameter_file):
  f=codecs.open(path_to_parameter_file,'rU','utf-8')
  parameter_set=[line.strip() for line in f.readlines()]
  return parameter_set


if __name__=='__main__':
  print('\nrunning parallel command line Stanford Parser task...')
  print('@Arg: 1. path_to_training_set (file keeps names of training corpora), 2.path_to_parameter_set (file keeps parameters: -PCFG -vMarkov -hMarkov -umw)\n3.max memory (e.g 3g) for each process')

  start=time.mktime(time.localtime())

  path_to_training_set=sys.argv[1]
  path_to_parameter_set=sys.argv[2]
  max_mem=sys.argv[3]

  print('\nRetrieval of training_corpora names and parameter set')
  corpora=get_training_corpora(path_to_training_set)
  parameter_set=get_parameter_set(path_to_parameter_set)

  proc=[]

  print('\nRunning parallel trianing...')
  for training_corpus in corpora:
    for parameter_string in parameter_set:
      p=Process(target=do_training, args=(parameter_string, training_corpus, max_mem))
      p.start()
      proc.append(p)

  for p in proc:
    p.join()

  elapsed=time.mktime(time.localtime())-start
  print('\n>>>All the jobs are done!')
  print('time elapsed:', elapsed, 'seconds')  


  
