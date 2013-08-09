#
# pre_processing_tree_annotation.py
#

# -*- coding: utf8 -*-

'''
Script to make all the tags in the form of X_subscript,
to comply with NLTK Tree format.


Three rules:

X c --> X_c     
Xl/r --> X_l/r
X b/i --> X_b/i

to summarize, b, i and c subscript are separated with whitespace from the main tag, while l and r subscript directly follow the main tag.


X can be represented as (1) [A-Z]+  

or (2) a closed list of all the tags 
{'AD', 'AS', 'BA', 'CC', 'CD', 'CS', 'DEC','DEG', 'DER', 'DEV', 'DT', 'ETC', 'FW', 'IJ', 'JJ', 'LB', 'LC', 'M', 'MSP', 'NN', 'NR', 'NT', 'OD', 'ON', 'P', 'PN', 'PU', 'SB', 'SP', 'VA', 'VC', 'VE', 'VV' }

  

should be verified by both expression to check any inconsistency

'''

import sys
import codecs
import re

POS={'AD', 'AS', 'BA', 'CC', 'CD', 'CS', 'DEC','DEG', 'DER', 'DEV', 'DT', 'ETC', 'FW', 'IJ', 'JJ', 'LB', 'LC', 'M', 'MSP', 'NN', 'NR', 'NT', 'OD', 'ON', 'P', 'PN', 'PU', 'SB', 'SP', 'VA', 'VC', 'VE', 'VV' }
#valid POS in CTB

is_x=re.compile('[A-Z]+')
is_x_lr=re.compile('([A-Z]+)([lr])')

BI={'b','i'}



def pre_proc(tokens):
  target=[]
  char_seq=[]
  check_stack=[]

  #print('\n\nline to be proc=', tokens, len(tokens))


  d_current=tokens[0]  #special treatment of the first position of the seq

  if d_current=='(':
    target.append(d_current)
    check_stack.append(d_current)

  else:
    print ('Error! A line shall start with "("')
    return -1              
      

  i=1

  while i<len(tokens)-1:
    d_last=tokens[i-1]
    d_next=tokens[i+1]
    d_current=tokens[i]


    #case '('
    if d_current=='(':
      target.append(d_current)
      check_stack.append(d_current)
      i=i+1
                
                
    #case  X b/i --> X_b/i
    elif d_last=='(' and is_x.match(d_current) and d_next in BI: 
      target.append(d_current+'_'+d_next)
      target.append(tokens[i+2])
      char_seq.append(tokens[i+2])
      i=i+3

    #case X c --> X_c
    elif d_last=='(' and  is_x.match(d_current) and d_next=='c':
      target.append(d_current+'_'+d_next)
      i=i+2

    #case Xl/r -->X_l/r
    elif d_last=='(' and is_x_lr.match(d_current) and d_next=='(':
      m=is_x_lr.match(d_current)
      tag=m.group(1)
      subscript=m.group(2)
      symbol=tag+'_'+subscript
                
      target.append(symbol)
      i=i+1

    # case ')'
    elif  d_current==')':
      if check_stack[-1]=='(':
        check_stack.pop()
        target.append(d_current)
        i=i+1
      else:
        print('Error! "(" and ")" does not match!!!')
        return -1

    else:
      print ('Error! Unknown configuration  last/current/next is:', d_last, d_current, d_next)


  # proc last item in the tokens list
  if tokens[i]==')' and check_stack[-1]=='(' and len(check_stack)==1:

    check_stack.pop()
    target.append(tokens[i])

  else:
                
    print('Error! Check-stack is not emplty in the end!')

  #print('char_seq=', ''.join(char_seq))
  #print('new_line=', target, len(target))

  return target
                
             

      
    
    


print ('\n>>> Pre-processing of the tree/word-structure annotation','to make all the tags in the form of X_subscript,to comply with NLTK Tree format')
print ('@@@requirs two arguments 1:path_to_annotation; 2: path_to_result')

path=sys.argv[1]
path2=sys.argv[2]


f=codecs.open(path, 'rU', 'utf-8')

print('\nreading the original annotation from ',path,'...')
lines=f.readlines()
new_lines=[]

print('\npre-processing...')
for line in lines:
  tokens=re.findall('\S+', line, re.U)
  target=pre_proc(tokens)  #target is a list of strings
  new_lines.append(target)  #call the pre-processing sub-routine

f.close()


print('\nwriting results to ',path2, '...')
f=codecs.open(path2, 'w', 'utf-8')
for line in new_lines:
  #print(type(line))
  d_str='  '.join(line)
  
  f.write(d_str+'\n')

print('\n>>>Completed!')

  
  
  



