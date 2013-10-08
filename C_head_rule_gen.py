#
# head_rule_gen.py
#

'''
generate (head) rule file for Zpar.
using word-structure annotation for Zpar (e.g. word_str_annotation1.zpar) to collect or non-terminals, and generate a rule
according to its subscripts

'''

import codecs
import sys
import string

from utility_proj import decompose_tag
#import re

print('\n\nRunning head_rule_gen for Zpar')
print('\n@Arg: 1.path_to_word_structure_annotaiton_4zpar (default:../working_data/word_str_annotation1.zpar )'+
      '\n2. (optional) path_to_rule_file' )


path_to_annotation='../working_data/word_str_annotation1.zpar'
path_to_rule='../working_data/rules.zpar'
if len(sys.argv)>1:
    path_to_annotaiton=sys.argv[1]
    if len(sys.argv)>2:
        path_to_rule=sys.argv[2]
    else:
        path_to_rule='/'+'/'.join(os.path.realpath(path_to_annotation).split('/')[:-1])+'/'+'rules.zpar'

def remove_p(d_str):
    return '  ' if d_str in {'(',')'} else d_str
    
l_set={'l','c'}
r_set={'r'}
rules={}#dictionary to keep rules

print('\ncollecting non-termianls...')
lines=codecs.open(path_to_annotation, 'rU','utf-8').readlines()
non_terminals={d_string for line in lines for d_string in ''.join([remove_p(char) for char in line]).split() if len(d_string)>2 and d_string[-2]=='_' and d_string[-1] in string.ascii_letters  }

print('\nconstructing rules...')
for full_tag in non_terminals:
    main_tag, subscript = decompose_tag(full_tag)
    #only dealing with l/r/c tag, not b/i tag
    if subscript in {'l','c','r'}:
        rules[full_tag]='l' if subscript in l_set  else 'r'

print('\nwriting rules to file', path_to_rule)
f=codecs.open(path_to_rule,'w','utf-8')
for tag in rules:
    f.write(tag+'	:'+rules[tag]+'\n')
f.close()    
