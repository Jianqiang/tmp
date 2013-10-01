#
# cmd_multiproc.py
#

'''
support running linux command in parallel with Python multiprocessing

'''

from multiprocessing import Process
import os
import sys
import codecs
import time

def file_split(path_to_original_corpus, num_of_splits):
  print('splitting corpus', path_to_original_corpus, 'into ', num_of_splits, 'parts...')
  real_path=os.path.realpath(path_to_original_corpus)
  #prefix='/'+'/'.join(real_path.split('/')[:-1])
  #name=real_path.split('/')[-1]

  f=codecs.open(path_to_original_corpus,'rU','utf-8')
  lines=f.readlines()
  f.close()
  splits=[]
  last_iter=0
  for i in range(1, num_of_splits+1):
    current_iter=int(len(lines)*i/num_of_splits)
    splits.append(lines[last_iter:current_iter])
    last_iter=current_iter

  list_subcorpus_names=[]
  for i, subcorpus in enumerate(splits):
    subcorpus_name=real_path+'.sub'+str(i)
    list_subcorpus_names.append(subcorpus_name)

    f=codecs.open(subcorpus_name, 'w','utf-8')
    for line in subcorpus:
      f.write(line)
    f.close()

  return list_subcorpus_names
  


def parallelization_parse( model, input_corpus, parsed_corpus):
  #model, input_corpus, parsed_corpus= the_argv
  cmd='java -mx8g -cp "stanford-parser.jar" edu.stanford.nlp.parser.lexparser.LexicalizedParser  -printPCFGkBest 10 -sentences newline '
  cmd += model+' '+input_corpus+' > '+parsed_corpus
  os.system(cmd)





if __name__=='__main__':
  print('\nrunning parallel command line Stanford Parser task...')
  print('@Arg: 1. model 2. corpus_to_be_parsed, 3.number_of_splits')

  start=time.mktime(time.localtime())

  #input
  path_to_model=os.path.realpath(sys.argv[1])
  path_to_corpus_to_be_parsed=sys.argv[2]
  num_of_splits=int(sys.argv[3])

  #split input corpus and get names of subcorpora
  list_subcorpus_names=file_split(path_to_corpus_to_be_parsed, num_of_splits)

  #gen arguments for the function
  argv_list=[(path_to_model, path_input_corpus, path_input_corpus+'.subpsd') for path_input_corpus in list_subcorpus_names]

  #
  # >> call running-parser function in parallel
  proc=[]
  print('\nRunning parallel parsing tasks...')
  for i, the_argv in enumerate(argv_list):
    print('#Initializing proc',i)
    p=Process(target=parallelization_parse, args=the_argv)
    p.start()
    proc.append(p)

  for p in proc:
    p.join()

  #merge the results
  real_path=os.path.realpath(path_to_corpus_to_be_parsed)
  prefix='/'+'/'.join(real_path.split('/')[:-1])
  suffix='/'+real_path.split('/')[-1]+'.psd'
  target=prefix+suffix

  print('\nMerging parsing result to file', target )
  os.system("cat "+" ".join([path_input_corpus+'.subpsd' for path_input_corpus in list_subcorpus_names])+" > " +target)

  print('And removing temp splitted files...')
  os.system("rm "+" ".join([path_input_corpus+'.subpsd' for path_input_corpus in list_subcorpus_names])+"  "+"  ".join(list_subcorpus_names))
  
  elapsed=time.mktime(time.localtime())-start
  print('\n>>>All the jobs are done!')
  print('time elapsed:', elapsed, 'seconds')
