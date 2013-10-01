#
# B_parsing_result_2_segmentation.py
#

'''
Collect the parsing results from the global constituent parsing model,
and convert them to segmentation result

'''

import codecs
import sys
import os
import pickle


from psd_sent_2_seg import convert_psd_sent_2_segmentation, convert_psd_sent_2_segmentation_2


def parse_result_collector_gcp(parsing_result):

  print('Collecting parsing result from ', parsing_result)

  ParsedCorpus=[]
  top_k_parse=[]
  parsed_sent=[]

  
  f=codecs.open(parsing_result, 'rU','utf-8')
  lines=f.readlines()
  f.close()
  counter=0
  max_count=len(lines)
  
  for line in lines:
    counter += 1
    if counter%int(max_count/5)==0:
      print (int(counter/max_count*100), '% finished...')
    
    tokens=line.split()
    
    if tokens:  #current line is not empty
      parsed_sent.extend(tokens)
      

    else:
      #print('\n#####Emptry Line')
      #print(parsed_sent)

      if parsed_sent[0]=='(ROOT':
        
        if top_k_parse:  
          ParsedCorpus.append(top_k_parse)

        parsed_sent=[]
        top_k_parse=[]
        
        

      elif parsed_sent[:2]==['#','Parse']:        
        score=float(parsed_sent[5])
        top_k_parse.append((score, ' '.join(parsed_sent[6:])))
        parsed_sent=[]
        
        

      else:
        print('Parsing Result FORMAT ERROR!')
        break

  if top_k_parse:
    ParsedCorpus.append(top_k_parse)

  return ParsedCorpus


  
#### Running the script ####

print('\nRunning global_parsing_result_collector')
print('@Arg: 1. path_to_parser_output')

path_to_parser_output='../working_data/test.a1.10best.psd'
path_to_collector_result_pickle='../working_data/pc.pickle'

if len(sys.argv)>1:
  path_to_parser_output=sys.argv[1]


parsed_corpus=parse_result_collector_gcp(path_to_parser_output)

SegCorpus=convert_psd_sent_2_segmentation(parsed_corpus)

path_output='/'.join(os.path.realpath(path_to_parser_output).split('/')[:-1])+'/'+path_to_parser_output.split('/')[-1][:-3]+'seg'
print('\nWriting segmentation result to', path_output)
f=codecs.open(path_output,'w','utf-8')
for seg in SegCorpus:
  f.write(' '.join(seg)+'\n')






  
  
