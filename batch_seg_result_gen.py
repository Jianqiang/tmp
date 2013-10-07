#
# batch_seg_result_gen.py
#


'''
generate segmetnation result form *.psd file generate from the parser

note:need #1."python" cmd on the system should be python 3.1 or above; consider set alias temporarily
          2. B_collect_parsing_result_n_convert2_segmentation.py or other script that collects and converts
             *.psd (parsing results) to *.seg (segmentation results)
          3. If B_collect_parsing_result_n_convert2_segmentation.py is used, it depends on psd_sent_2_seg.py  
'''

import os
import sys
from multiprocessing import Process
import codecs



def run_parse2seg(script_path, psd_file):
    os.system("python3 "+script_path+"  "+psd_file)



if __name__=='__main__':

    print('\nArg: 1. directory_of_psd_files, 2.path_to_scirpt_collect_parsing_result_n_convert2_segmentation.py'+
          '(by default: ./B_collect_parsing_result_n_convert2_segmentation.py)')

    #step1
    print('>>collect all *.psd files...')
    d_dir=os.path.realpath(sys.argv[1])
    files=[f for f in os.listdir(d_dir) if os.path.isfile(f) and f[-4:]=='.psd']

    #step2
    parse2seg_script='./B_collect_parsing_result_n_convert2_segmentation.py'
    if len(sys.argv)>2:
        parse2seg_script=os.path.realpath(sys.argv[2])
    print('>>running collect_parsing_result_n_convert2_segmentation.py for all *.psd files in parallel')
    proc=[]
    for psd_result in files:
        p=Process(target=run_parse2seg, args=(parse2seg_script, psd_result))
        p.start()
        proc.append(p)

    for p in proc:
        p.join()

    print('done!')
    


    
    
