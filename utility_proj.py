#
# utility_proj.py
#
'''
project utility, some subroutines shared by modules. Extracted to keep consistency
'''

import re

pattern=re.compile('([A-Z]+)_([a-z]+)') # the pattern of tree nodes (tags), compiled, as will be called repeatedly


# convert a set of item to a single str representation
# ----->!!! warning: this peace of code makes assumptions about tagset(no 'Z' occurs in a tag name)
def set2str(d_set):
  new_list=list(d_set)
  #new_list.extend(d_set)
  new_list.sort()

  return 'Z'.join(new_list)



#pattern_str2set=re.compile(('[A-Y]'))
def str2set(d_str):
  d_set=set()
  S=''
  for item in d_str:
    if item=='Z':
      d_set.add(S)
      S=''

    else:
      S=S+item

  if S:
    d_set.add(str(S))

  return d_set




#decompose tags in the form  "tag_subscript"
def decompose_tag(complex_tag):

  #pattern=re.compile('([A-Z]+)_([a-z]+)') # the pattern of tree nodes (tags), compiled, as will be called repeatedly

  match=pattern.match(complex_tag)

  try:
    match=pattern.match(complex_tag)
    
    tag=match.group(1)
    subscript=match.group(2)

    return tag, subscript

  except:
    print ('Error in tag format! The tag format is unrecognizable! e.g.',complex_tag)
    return False
