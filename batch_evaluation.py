#
# batch_evaluation.py
#

import os
import sys
from multiprocessing import Process
#import codecs


def evaluate(path_to_score, path_to_dict, path_to_gold, path_to_segment_result):
    os.system("perl "+path_to_score+" "+path_to_dict+" "+path_to_gold+" "+path_to_segment_result+"  >"+path_to_segment_result[:-4]+".eval")


def parse_evaluation_result(path_to_evaluation_result):
    #f=codecs.open(path_to_evaluation_result, 'rU','utf-8')
    f=open(path_to_evaluation_result, 'r')
    lines=f.readlines()
    d_str=lines[-1]
    last_line_tokens=d_str.split()
    #last_line_tokens=f.readlines()[-1].split()
    if last_line_tokens[0]=='###' and len(last_line_tokens)==14:
        recall, precision,f_score,oov_rate,oov_recall,iv_recall=[float(i) for i in last_line_tokens[-6:]]
        return recall, precision,f_score,oov_rate,oov_recall,iv_recall
    else:
        print('error! Format of the EVALUATION RESULT does not match the standard!')

    

    

if __name__=='__main__':

    print('\nRunning batch_evaluation... \nCollect all the call "score" utility to evaluate all the *.seg file'+
          '\n& generating *.eval files to keep the result; and then finally to gen a *.summary to figure out the best result'+
          '\n\n@Arg: 1.directory/path_to_.seg_files  2. path_to_score_function, 3.path_to_dictionary, 4_path_to_goldstandard'+
          '\note: ./score is in the same dir of this script by default')


    #step1
    print('>>collect all *.seg files...')
    d_dir=os.path.realpath(sys.argv[1])
    path_to_score=sys.argv[2]
    path_to_dict=sys.argv[3]
    path_to_gold=sys.argv[4]

    files=[f for f in os.listdir(d_dir) if os.path.isfile(f) and f[-4:]=='.seg']


    #step2
    print('>>run evaluation (in parallel) for each segmentation result')
    proc=[]
    list_eval_result=[]
    for seg_result_file in files:
        p=Process(target=evaluate, args=(path_to_score, path_to_dict, path_to_gold, d_dir+'/'+seg_result_file))
        p.start()
        proc.append(p)

    for p in proc:
        p.join()

    print('>> writing the filename+f-score to summary.txt', 'in',d_dir) #python3 seems to have problems decode *.eval file, we use shell instead
    os.system("cd "+d_dir)
    os.system(" tail -1 *.eval |  grep '###' | sort -k11n | awk '{print  $2 "+ ' "\tF-score=" '+" $11}' > tmp.txt ")
    os.system("tail -r tmp.txt >summary.txt")

'''
    #step3
    print('>>generating .summary file to report the result')
    files=[f for f in os.listdir(d_dir) if os.path.isfile(f) and f[-5:]=='.eval']
    results=[]
    for eval_result in files:
        #print((eval_result, parse_evaluation_result(eval_result)))
        tmp_list=[eval_result]
        tmp_list.extend([i for i in parse_evaluation_result(eval_result)])
        results.append(tuple(tmp_list) )

    results.sort(key=lambda x:x[3], reverse=True)


    path_summary=d_dir+'/'+'eval.summary'
    f=open(path_summary, 'w')

    print('\n=======Results summary========\nalso saved in ', path_summary)
    print('format: name, recall, precision,f_score,oov_rate,oov_recall,iv_recall')

    for result in results:
        for entry in result:
            f.write("%10s" % entry+' | ')
            print ("%10s" % entry+' | ', end='')
        print('\n')
        f.write('\n')            

'''    
    
    

