#
# format_converter_4_crf_tagger.py
#
'''
convert the plain txt input, each line of which looks like:
外商_NN 投资_NN 企业_NN 成为_VV 中国_NR 外贸_NN 重要_JJ 增长点_NN

into CoNLL format which is readable for CRF++ package:

    Each token must be represented in one line, with the columns separated by white space
    (spaces or tabular characters). A sequence of token becomes a sentence.
    To identify the boundary between sentences, an empty line is put.


In order to support the use of morpholigical features,
 we need to represent the character features in the columns,
i.e. "character n-gram prefixes and suffixes for n up to 3",
which are 6 columns. 

'''

import re

#directory/file name configurations:

print('===Warning:run this script at the PoS_Zhu/scr directory, it is path-sensitive..')


#project_path='/Users/jma/Dropbox/Code/PoS_Zhu'
project_path='../'  #sppose we are at the src directory
working_data_path=project_path+'/working_data/'

train='train.txt'
test='test.txt'
dev='dev.txt'


train4crf='train.in'
test4crf='test.in'
dev4crf='dev.in'





#
# define of the format_converter_function:
#

word_tag_pair_pattern=re.compile('(.*)_([A-Z]+)')

def format_convert(source, target):
  f_r=open(source, 'rU')
  f_w=open(target,'w')

  for line in f_r:
    word_tag_token_seq=re.findall('\S+',line,re.U)
    #print(word_tag_token_seq)
    #line_conll=[]
  
    for word_tag_pair in word_tag_token_seq:
      m=word_tag_pair_pattern.match(word_tag_pair)
      if m:

        groups=m.groups()

        if len(groups)==2:

          word=m.group(1)
          tag=m.group(2)
          #print(m.group(1),end='  ')
          #print(m.group(2))

          word_len=len(word)
          p1=word[0]
          p2=''
          p3=''

          s1=word[-1]
          s2=''
          s3=''

          if word_len>1:
            p2=word[0:2]
            s2=word[-2:]

            if word_len>2:
              p3=word[0:3]
              s3=word[-3:]

            else:
              p3=p2+'_#_'
              s3='_#_'+s2

            
          else:
            p2=p1+'_#_'
            p3=p2+'_#_'
            s2='_#_'+s1
            s3='_#_'+s2


          #print(word,p1,p2,p3,s1,s2,s3,tag,sep=' // ')
          line_conll=[word,p1,p2,p3,s1,s2,s3,tag]
          for item in line_conll:
            f_w.write(item+'    ')
          f_w.write('\n')
          

        else:
          print('Error! each token shall be a word-tag pair!')
          break

      else:
        print('Error! The current token does not match "word_tag" format!')
        break


    f_w.write('\n')          
          
            
          

          

          
      
print('\n\n>>Converting the plain text corpus to CoNLL format, which is readable by CRF softwares')      

x=working_data_path
print('testing data...')
format_convert(x+test, x+test4crf)
print('developing data...')
format_convert(x+dev, x+dev4crf)
print('training data...')
format_convert(x+train, x+train4crf)
print('Done!')
  
