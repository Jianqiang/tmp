#
# ctb5_split_4_joint_seg_tag.py
#

'''
split Chinese Treebank 5 into train,dev,test set, according to popular ways of splitting
in joint segmentation and pos-taggging literature such as

Sun Weiwei 2011 Jiang Wenbin et al. 2008; Zhang and Clark 2010

'''

import os
import sys
import re
import codecs


d_pattern=re.compile('([a-z]*)_(\d*)\.[nm][wz]\.pos') #pattern for file name in CTB

non_sent=re.compile('<.*>') # non-sentence (pure xml tags) pattern for content of the corpus

print('\n\n>>> Runing ctb5_split_4_joint_seg_tag.py...')
print('split Chinese Treebank 5 into train,dev,test set, according to popular configurations in joint segmentation and pos-taggging literature \nsuch as Sun Weiwei 2011 Jiang Wenbin et al. 2008; Zhang and Clark 2010')

print('\nWarning:run this script at the PoS_Zhu/scr directory, it is path-sensitive..')
#project_path='/Users/jma/Dropbox/Code/PoS_Zhu'
project_path='../'
ctb_path=project_path+'/ctb5'

list_of_dev=[]
list_of_test=[]
list_of_train=[]

print('spliting the corpus...')

os.chdir(ctb_path)
list_of_files=os.listdir(ctb_path)
sorted_list_of_files=sorted(list_of_files)
for file in sorted_list_of_files:
  match=d_pattern.match(file)
  file_id=int(match.group(2))

  if file_id>300 and file_id<326:
    list_of_dev.append(file)

  elif file_id>270 and file_id<301:
    list_of_test.append(file)

  else:
    list_of_train.append(file)

def write_to_file(path, data):
  file=codecs.open(path, 'w','utf-8')
  for line in data:
    if not non_sent.match(line):  #removal of pure xml tag lines (reserve plain text lines)
      file.write(line)
  file.close()

print('\nSpliting done! Writing to files...')

working_path=project_path+'/working_data/'
      
train=[line for file in list_of_train for line in codecs.open(file,'rU','utf-8').readlines() ]
p_train=working_path+'train.ctb5.pos'
write_to_file(p_train, train)

test=[line for file in list_of_test for line in codecs.open(file,'rU','utf-8').readlines() ]
p_test=working_path+'test.ctb5.pos'
write_to_file(p_test, test)

dev=[line for file in list_of_dev for line in codecs.open(file,'rU','utf-8').readlines() ]
p_dev=working_path+'dev.ctb5.pos'
write_to_file(p_dev, dev)


the_all=[line for file in sorted_list_of_files for line in codecs.open(file,'rU','utf-8').readlines() ]
p_all=working_path+'all.ctb5.pos'
write_to_file(p_all, the_all)
print('finished writing!')

#corpus statistics...
print('\ncorpus statistics')
token_count=0
line_count=0
for line in the_all:
  if not non_sent.match(line):
    line_count += 1
    tokens=re.findall('\S+', line, re.U)
    token_count += len(tokens)
print('token count:',token_count)
print('sent count:',line_count)


#pattern_wd=re.compile('\S+_[A-Z]+')
sent=[]
for line in the_all:
  tokens=re.findall('\S+_[A-Z]+', line,re.U)
  sent.extend(tokens)

print('token count (d. method):',len(sent))

