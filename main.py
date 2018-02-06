import sys
import os
from datetime import datetime
import subprocess
from termcolor import colored, cprint

DEFAULT_OUPUT = 'file name: {}\nInput:\n{}\nExpected Ouput:\n{}\nActual Ouput:\n{}\nVerdict: {} (time: {})\n'
ONELINE_OUTPUT = 'file name: {:6} {} (time: {:4})'

class TimeLimitExceeded (Exception):
    def __init__ (self, msg=None):
        if msg is None:
            msg = colored("Time limit Exceeded",'blue')
        super(TimeLimitExceeded, self).__init__(msg)

def run_program (program_path, input_file_path):
    cmd = ''.join([program_path, '<', input_file_path])
    start = datetime.now()
    output = subprocess.getoutput(cmd)
    end = datetime.now()
    final_time = end - start
    return (round(final_time.total_seconds(), 3), output)

def get_output_file_name (name, output_folder):
    for output_file_name in os.listdir(output_folder):
        basename = os.path.splitext(output_file_name)[0]
        if basename == name:
            return output_file_name
    raise Exception('No corresponding output file for file {}'.format(name))

def check_output (actual_output, expected_output, time, info):
    if time > float(info['TIMELIMIT']):
        raise TimeLimitExceeded()
    if actual_output.splitlines() == expected_output.splitlines():
        return True
    else:
        return False
        

if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit ("Needs a folder path.")
    
    fullpath = os.path.abspath(sys.argv[-1])
    oneline = len(sys.argv) > 2
    
    input_folder = os.path.join(fullpath, 'input/')
    output_folder = os.path.join(fullpath, 'output/')
    program_path = os.path.join(fullpath, 'sol')
    info_path = os.path.join(fullpath, 'info.txt')

    if not os.path.isfile(program_path):
        program_path = os.path.join(fullpath, 'sol.exe')
    if not os.path.isfile(program_path):
        exit ("Needs running program named sol.")

    info = {}

    with open(info_path, 'r') as f_info:
        for line in f_info:
            var, value = line.split('=')
            info[var] = value[:-1]

    input_files = os.listdir(input_folder)
    input_files.sort()

    for input_file_path in input_files:
        name = os.path.splitext(input_file_path)[0]
        output_file = get_output_file_name(name, output_folder)

        time, actual_output = run_program(program_path, os.path.join(input_folder, input_file_path))

        with open(os.path.join(input_folder, input_file_path), 'r') as f_in:
            input_data = f_in.read()

        with open(os.path.join(output_folder, output_file), 'r') as f_out:
            expected_output = f_out.read()
        
        try:
            accepted = check_output(actual_output, expected_output, time, info)
            if accepted:
                verdict = colored('Accepted!', 'green')
            else:
                verdict = colored('Wrong answer', 'red')
        except TimeLimitExceeded as e:
            verdict = e

        if oneline:
            print(ONELINE_OUTPUT.format(name, verdict, time))
        else:
            print(DEFAULT_OUPUT.format(name, input_data, expected_output, actual_output, verdict, time))
    
    exit(1)
