#
# ctb6_division_huang.py
#
'''
divide the CTB6 corpus into training, developing and testing data set according to

Huang, Z., Eidelman, V., & Harper, M. (2009).
Improving A Simple Bigram HMM Part-of-Speech Tagger by Latent Annotation and Self-Training.
NAACL (pp. 213–216).

for the purpose of result comparsion

Specifically:

 divide them (CTB6 files) into blocks of 10 files in sorted order
 and for each block use the 1st file for development,
 the 2nd for test, and the re- maining for training. "

'''

import os
import sys
import re
import codecs

print('===Warning:run this script at the PoS_Zhu/scr directory, it is path-sensitive..')
#project_path='/Users/jma/Dropbox/Code/PoS_Zhu'
project_path='../'
ctb_path=project_path+'/ctb6_tagged'

non_sent=re.compile('<.*>') # non-xml-format lines


# 1. split the original files into train/dev/test set,
#each of which becomes a unified file

list_of_dev=[]
list_of_test=[]
list_of_train=[]

os.chdir(ctb_path)
list_of_files=os.listdir()
sorted_list_of_files=sorted(list_of_files)

print('(sorted) list of data files...')
for i in range(len(sorted_list_of_files)):
  print(sorted_list_of_files[i])
  #print(sorted_list_of_files[i], end=' ==>')
  #if list_of_files[i] == sorted_list_of_files[i]:
    #print('YES!')
  

for i in range(len(sorted_list_of_files)):

  name=sorted_list_of_files[i]
  
  if i%10==1:
    list_of_dev.append(name)
  elif i%10==2:
    list_of_test.append(name)

  else:
    list_of_train.append(name)
  
# note that the sent numbers do not match with Huang et al., paper, we suspect that they
# append the last six file to train (originally: 1 to test, 1 to dev, 4 to train)
#
#list_of_train.append(list_of_dev.pop())
#list_of_train.append(list_of_test.pop())


print('\n>>Num of dev/test/train/total files are:')
print(len(list_of_dev), len(list_of_test), len(list_of_train), len(list_of_files), end='\n\n')
    

#
# merging train,test, dev data into 3 single files
#
working_data_path=project_path+'/working_data/'

train='ctb6.huang.train'
test='ctb6.huang.test'
dev='ctb6.huang.dev'

f_w=open(working_data_path+train, 'w')


def read_files_write_to_single_file(reading_list, target_file):

  f_w=open(target_file, 'w')
  
  for i in reading_list:
    f_r=open(i,'r')
    file=f_r.read()
    f_w.write(file)
    f_r.close()

  f_w.close()

    
print ('\n>>Mergeing training/testing/developeing files to 3 single files...')
read_files_write_to_single_file(list_of_test, working_data_path+test)
read_files_write_to_single_file(list_of_dev, working_data_path+dev)
read_files_write_to_single_file(list_of_train, working_data_path+train)
print('done!')

print('\n>>Removing xml tags and convert train/test/dev files to txt format...')

def clean(source, target):
  Sent=[]
  f=open(source,'rU')
  lines=f.readlines()
  for i in lines:
    new_line=i.strip()
    if not non_sent.match(new_line):
      Sent.append(i)

  f.close()
  f=open(target,'w')
  for i in Sent:
    f.write(i)
  f.close()


new_train='train.txt'
new_test='test.txt'
new_dev='dev.txt'

clean(working_data_path+test, working_data_path+new_test)
clean(working_data_path+dev, working_data_path+new_dev)
clean(working_data_path+train, working_data_path+new_train)
  
      
    


