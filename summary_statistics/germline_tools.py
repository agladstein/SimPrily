from subprocess import Popen

def run_germline(ped_name, map_name, out_name, min_m):
    print( 'Running Germline on ' + ped_name + ' ' + map_name)

    bash_command = 'bash ./bin/phasing_pipeline/gline.sh ./bin/germline-1-5-1/germline  {0} {1} {2} "-bits 10 -min_m {3}"'.format(
        ped_name, map_name, out_name, str(min_m))
    print( bash_command)

    germ_flag = Popen.wait(Popen(bash_command, shell=True))
    print( 'finished running germline')
    return germ_flag

def process_germline_file(germfile_name, name_list):
    """
    Creates a list of all IBD pair options, and a dictionary of the pair options pointing 
    to lists of corresponding segments from the germfile.
    """
    germline_file = open(str(germfile_name) + '.match', 'r')
    ## Create a list of all UNIQUE possible pairs from name_list (A_B and B_A are considered the same, A_A is also allowed)
    pair_list = ['{0}{1}'.format(name_list[i], name_list[j]) for i in range(len(name_list)) for j in range(len(name_list)) if j>=i]
    pair_dict  = {pair:[] for pair in pair_list}

    for line in germline_file:
        process_germline_line(line, pair_list, pair_dict)

    germline_file.close()
    return [pair_list, pair_dict]

def process_germline_line(line, pair_list, pair_dict):
    line = line.split()
    ## Read names from germline
    pop1 = str(line[0])
    pop2 = str(line[2])
    # pop1 = str( line[1].split('_')[1] )
    # pop2 = str( line[3].split('_')[1] )

    segment = float(line[10]) / 1000000
    ## Ensure that pair is a key in pair_dict   
    pair = (pop1+pop2) if (pop1+pop2) in pair_list else (pop2+pop1)
    pair_dict[pair].append(segment)