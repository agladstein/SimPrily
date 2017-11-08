from main_tools import global_vars
from main_tools.my_random import MY_RANDOM as random
import sys


def prettyPrintDict(dic):
    out = ""
    for x in dic:
        out += x+'-->' + dic[x] + "\n"
    return out

def debugPrint(verbosLevel, string):
    if global_vars.verbos >= verbosLevel: 
        for line in string.split("\n"):
            print("  "*(verbosLevel-1) + "debug-" + str(verbosLevel) +": "+ line)

def process_args(arguments):
    '''
    Parameters: ['simprily.py', 'examples/eg1/param_file_eg1.txt',
     'examples/eg1/model_file_eg1.csv', '1', 'output_dir']

    Returns:  {'SNP file': 'array_template/ill_650_test.bed', 
    'sim option': 'macs', 'germline': 1, 'model file': 
    'examples/eg1/model_file_eg1.csv', 'job': '1', 'command': 
    'simprily.py', 'param file': 'examples/eg1/param_file_eg1.txt', 
    'random discovery': True, 'path': 'output_dir'}
    '''
    debugPrint(3, "PROCESS ARGS PARAMETERS: " + str(arguments))
    args = {'command':arguments[0],
            'param file':arguments[1],
            'model file':arguments[2],
            'job':arguments[3],
            'path':arguments[4]}
    model_args = argsFromModelCSV(args['model file'])
    args['sim option'] = model_args['sim option']
    args['SNP file'] = model_args['SNP file']
    args['germline'] = model_args['germline']
    args['random discovery'] = model_args['random discovery']
    debugPrint(3, "PROCESS ARGS RETURNS: " + str(args))
    return args

def set_seed(seed_option):
    seed_option = int(seed_option)
    print(seed_option)
    if seed_option == 0:
        random.seed()
    if seed_option > int(0):
        random.seed(seed_option)

def argsFromModelCSV(filename):
    '''
    This function returns a dictionary for the arguments of the 
    program
    Reads arguments from model_file.csv

    Parameters: filename, which is a csv file that has: 
     [['-macs', './bin/macs', ''],
     ['-length', '1000000', ''], ['-t', '2.5e-8', ''], ['-s', 
     '1231', ''], ['-r', '1e-8', ''], ['-h', '1e5', ''], ['-R', 
     'genetic_map_b37/genetic_map_GRCh37_chr1.txt.macshs', ''], 
     ['-I', '2', '20', '140', ''], ['-n', '1', 'A', ''], ['-n', 
     '2', 'B', ''], ['-ej_1', 'AB_t', '2', '1', ''], ['-en', 
     'AN_t', '1', 'AN'], ['-discovery', '1'], ['-sample', '2'], 
     ['-daf', 'daf'], ['-array', ' array_template/ill_650_test.bed'], 
     ['-random_discovery', ' True']] 


    Returns:  a dictionary, which has: 
    {'SNP file': 'array_template/ill_650_test.bed', 'random discovery':
     True, 'sim option': 'macs', 'germline': 1}
    '''
    
    f=open(filename, 'r')
    model_args=dict()
    for line in f:
        if line.startswith("-macs") or line.startswith("-macs_file"):
            x = line.strip().split(",")
            model_args['sim option']= x[0][1:]
        if line.startswith("-macsswig"):
            x = line.strip().split(",")
            model_args['sim option']= x[0][1:]
        if line.startswith("-array"):
            x = line.strip().split(",")
            if x[1].startswith(" "):
                model_args['SNP file']= x[1][1:]
            else:
                model_args['SNP file']= x[1]
        if line.startswith("-germline"):
            model_args['germline']= 0
        if line.startswith("-nonrandom_discovery"):
            model_args['random discovery'] = False
        
    if 'sim option' not in model_args:
        print("Sim option not provided in model_file.csv")
        sys.exit(1)
    if 'germline' not in model_args:
        model_args['germline'] = 1
    if 'random discovery' not in model_args:
        model_args['random discovery'] = True
    if 'SNP file' not in model_args:
        print("No SNP file provided in model_file.csv")
        sys.exit(1)
    debugPrint(3, "MODELS ARGS RETURNS:  " + str(model_args))
    return model_args
        
