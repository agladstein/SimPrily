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
    args = {'command':arguments[0],
            'param file':arguments[1],
            'model file':arguments[2],
            'job':arguments[3],
            'path':arguments[4]}
    model_args = argsFromModelCSV(args['model file'])
    args['sim option'] = model_args['sim option']
    args['SNP file'] = model_args['SNP file']
    args['germline'] = model_args['germline']
    args['pedmap'] = model_args['pedmap']
    args['random discovery'] = model_args['random discovery']
    return args

def set_seed(seed_option):
    seed_option = int(seed_option)
    print seed_option
    if seed_option == 0:
        random.seed()
    if seed_option > int(0):
        random.seed(seed_option)

def argsFromModelCSV(filename):
    #Reads arguments from model_file.csv
    #returns model_args dictionary
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
        if line.startswith("-pedmap"):
            model_args['pedmap'] = True
        
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
    return model_args
        
