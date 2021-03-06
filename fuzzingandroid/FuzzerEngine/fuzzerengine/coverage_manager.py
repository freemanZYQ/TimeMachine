
import os
import subprocess
import os.path
import time
import threading
import re
from config_fuzzer import RunParameters 

def get_emma_coverage(restore_count):
    # adb shell am broadcast -a edu.gatech.m3.emma.COLLECT_COVERAGE
    cov_file_name = 'coverage' + str(restore_count)

    cmd = subprocess.Popen(['../../scripts/pull_coverage.sh', cov_file_name],stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    output, err = cmd.communicate()
    print 'get_emma_coverage- return code: ' + ' output: ' + str(output) + ' ' + str(err) +' '

def get_ella_coverage(restore_count):
    cov_file_name = 'coverage' + str(restore_count)
    
        
    cmd = subprocess.Popen (['../../scripts/pull_coverage_ella.sh', cov_file_name],stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    output, err = cmd.communicate()
    print 'get_ella_coverage: return msg: error: ' + str(output) + ' ' + str(err) 

def compute_coverage():
    #using compute_coverage to compute
    cmd = subprocess.Popen ('../../scripts/compute_coverage.sh',stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    output, err=cmd.communicate()
    print 'compute_coverage-return code: ' + ' output: '+str(output) + '  ' + str(err) +' '

def compute_coverage_ella():
    #using compute_coverage to compute
    
    cmd = subprocess.Popen ('../../scripts/compute_coverage_ella.sh',stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    output, err=cmd.communicate()
    print 'compute_coverage-return code: ' + ' output: '+str(output) + '  ' + str(err) +' '

def read_coverage_ella():
    if not os.path.isfile ('../../output/ella_files/cov'):
        return 0
    f= open ('../../output/ella_files/cov', 'r')
    lines = f.readlines()
    f.close()

    return int(lines[0])

def read_current_coverage():
    if RunParameters.OPEN_SOURCE:
        return read_coverage()
    else:
        return read_coverage_ella()
def compute_current_coverage():
    if RunParameters.OPEN_SOURCE:
        compute_coverage()
    else:
        compute_coverage_ella()
def pull_coverage_files(restore_count):
    if RunParameters.OPEN_SOURCE:
        get_emma_coverage(restore_count)
    else:
        get_ella_coverage(restore_count)

def read_coverage():
    if not os.path.isfile('../../output/coverage.txt'):
        return 0

    f= open('../../output/coverage.txt', 'r')
    lines = f.readlines()
    f.close()

    if len(lines) < 6:
        return 0

    #see the format of code coverage summary generated by EMMA

    s=re.sub('\t',' ',lines[5])
    s=re.sub(' +',' ',s)
    s=s.split(' ')[6]
    print lines[5] + "current line coverage: " + s


    return int(s.replace("%", ""))

def record_coverage():
    start_time = time.time()
    file_path='../../output/coverage_time.csv'

    #clear the old data
    open(file_path,'w').close()

    while True:
        with open(file_path, 'a') as coverage_file:
            t = time.time() - start_time
            
            compute_coverage()
            coverage = read_coverage()
            
            line = str(round(t,1)) + "," + str(coverage) + "\n"
            coverage_file.writelines(line)
            coverage_file.flush()
            coverage_file.close()

        time.sleep(120)



if __name__=='__main__':
    # compute_coverage()
    #read_coverage()

    #coverage_writer=threading.Thread(target=record_coverage)
    #coverage_writer.start()
    compute_coverage_ella()
    tp=read_coverage_ella()
    print str(tp)
