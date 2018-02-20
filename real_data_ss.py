from collections import OrderedDict
from sys import argv
import numpy as np
import os
import argparse

from alleles_generator.bit_structure import set_real_genome_bits, set_real_array_bits
from alleles_generator.real_file import AllelesReal
from main_tools.write_files import write_stats_file
from alleles_generator.seqInfo import create_sequences
from main_tools.write_files import create_sim_directories
from processInput import process_input_files
from summary_statistics import stat_tools
from summary_statistics.germline_tools import run_germline, process_germline_file
from main_tools import global_vars
from main_tools.housekeeping import debugPrint

verbos = 0

def processArgs(arguments):
    parser = argparse.ArgumentParser()
    parser.add_argument("-p","--param",help="REQUIRED!: The location of the parameter file",required=True)
    parser.add_argument("-m","--model",help="REQUIRED!: The location of the model file",required=True)
    parser.add_argument("-o","--out", help="REQUIRED!: The location of the output dir",required=True)
    parser.add_argument("-g","--genome", help="The location of the genome file",required=True)
    parser.add_argument("-a","--array", help="The location of the array file",required=True)
    parser.add_argument("-v", help="increase output verbosity", action="count",default=0)
    tmpArgs = parser.parse_args()

    args = {
            'param file':tmpArgs.param,
            'model file':tmpArgs.model,
            'genome file':tmpArgs.genome,
            'array file':tmpArgs.array,
            'output':tmpArgs.out
        }

    global_vars.init()
    global_vars.verbos = tmpArgs.v
    debugPrint(1,"Debug on: Level " + str(global_vars.verbos))

    return args


def main(args):
    args = processArgs(args)

    model_file = args['model file']
    param_file = args['param file']
    path = args['output']

    [sim_data_dir, germline_out_dir, sim_results_dir] = create_sim_directories(path)

    processedData =  process_input_files(param_file, model_file, args)
    debugPrint(3, "Finished processing input\nprocessedData: ", processedData)

    using_pseudo_array = True
    if not processedData.get('discovery') and not processedData.get('sample') and not processedData.get('daf'):
        using_pseudo_array = False

    ### Create a list of Sequence class instances. These will contain the bulk of all sequence-based data
    sequences = create_sequences(processedData)
    names = [seq.name for seq in sequences]

    n_d = sum([1 for seq in sequences if seq.type == 'discovery'])

    debugPrint(1,'name\ttotal\tpanel\tgenotyped')
    for seq in sequences:
        debugPrint(1,'{}\t{}\t{}\t{}'.format(seq.name, seq.tot, seq.panel, seq.genotyped))

    total = sum([seq.tot for seq in sequences])
    debugPrint(1, 'total samples: {}'.format(sum([seq.genotyped for seq in sequences if seq.type=='discovery'] + [seq.tot for seq in sequences if seq.type=='sample'])))


    ##########################################################################
    ####################### Read Data from tped files ########################
    ##########################################################################

    genome_file = args['genome file']
    job = os.path.basename(genome_file)
    seq_alleles_genome = AllelesReal(str(genome_file)+'.tped')
    set_real_genome_bits(sequences, seq_alleles_genome)
    if using_pseudo_array == True:
        array_file = args['array file']
        job = str(job) + '_' + str(os.path.basename(array_file))
        seq_alleles_array = AllelesReal(str(array_file) + '.tped')
        set_real_array_bits(sequences, seq_alleles_array)

    ##########################################################################
    ###################### Calculate summary statistics ######################
    ##########################################################################
    res, head  = [], []

    ### Calculate summary stats from genomes
    stat_tools.store_segregating_site_stats(sequences, res, head)
    stat_tools.store_pairwise_FSTs(sequences, n_d, res, head)

    ### Calculate summary stats from the ascertained SNPs
    if using_pseudo_array:
        stat_tools.store_array_segregating_site_stats(sequences, res, head)
        stat_tools.store_array_FSTs(sequences, res, head)

        debugPrint(1,'Make ped and map files')
        ped_file_name = '{0}/{1}.ped'.format(sim_data_dir, job)
        map_file_name = '{0}/{1}.map'.format(sim_data_dir, job)
        out_file_name = '{0}/{1}'.format(germline_out_dir, job)

        ### Use Germline to find IBD on pseduo array ped and map files
        do_i_run_germline = 1 #fix this later

        debugPrint(1,'run germline? ' + str(do_i_run_germline))
        if (do_i_run_germline == 0):
            ########################### <CHANGE THIS LATER> ###########################
            ### Germline seems to be outputting in the wrong unit - so I am putting the min at 3000000 so that it is 3Mb, but should be the default.
            # germline = run_germline(ped_file_name, map_file_name, out_file_name, min_m = 3000000)
            germline = run_germline(ped_file_name, map_file_name, out_file_name, min_m=300)
            ########################### </CHANGE THIS LATER> ##########################

        ### Get IBD stats from Germline output
        if os.path.isfile(out_file_name + '.match'):
            debugPrint(1,'Reading Germline IBD output')
            [IBD_pairs, IBD_dict] = process_germline_file(out_file_name, names)

            debugPrint(1,'Calculating summary stats')
            stats = OrderedDict([('num', len), ('mean', np.mean), ('med', np.median), ('var', np.var)])
            stat_tools.store_IBD_stats(stats, IBD_pairs, IBD_dict, res, head)
            stat_tools.store_IBD_stats(stats, IBD_pairs, IBD_dict, res, head, min_val=30)

        # print 'finished calculating ss'

    write_stats_file(sim_results_dir, job, res, head)
    

    print('')
    print('##########################')
    print('### PROGRAM COMPLETED  ###')
    print('##########################')
    print('')


if __name__ == '__main__':
    main(argv)
