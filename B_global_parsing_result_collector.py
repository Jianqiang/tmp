#
# B_global_parsing_result_collector.py
#

'''
Collect the parsing results from the global constituent parsing model

'''

import codecs
import sys
import pickle



def parse_result_collector_gcp(parsing_result, result_pickle):

  print('Collecting parsing result from ', parsing_result)

  ParsedCorpus=[]
  top_k_parse=[]
  parsed_sent=[]

  
  f=codecs.open(parsing_result, 'rU','utf-8')
  lines=f.readlines()
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

  f.close()

  print ('\nWriting  collected parsing result to pickel file ', result_pickle)
  f=open( result_pickle , 'wb')
  pickle.dump(ParsedCorpus, f)
  

print('\nRunning global_parsing_result_collector')
print('@Arg: 1. path_to_parser_output,  2. path_to_collector_result_pickle')

parse_result_collector_gcp(sys.argv[1], sys.argv[2])
      






  
  
