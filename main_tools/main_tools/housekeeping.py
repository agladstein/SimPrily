from main_tools import global_vars
from main_tools.my_random import MY_RANDOM as random


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
            'sim option':arguments[3],
            'job':arguments[4],
            'SNP file':arguments[5],
            'germline':arguments[6],
            'random discovery':arguments[7],
            'path':arguments[8]}
    return args

def set_seed(seed_option):
    seed_option = int(seed_option)
    print seed_option
    if seed_option == 0:
        random.seed()
    if seed_option > int(0):
        random.seed(seed_option)