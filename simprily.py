import sys
from collections import OrderedDict
from sys import argv

import numpy as np
import os

from alleles_generator.bit_structure import set_seq_bits, set_discovery_bits, set_panel_bits
from alleles_generator.macs_file import AllelesMacsFile
from alleles_generator.macs_swig_alleles import AllelesMacsSwig
from alleles_generator.seqInfo import create_sequences
from ascertainment.asc_tools import set_asc_bits, make_ped_file, make_map_file, get_SNP_sites
from ascertainment.pseudo_array import pseudo_array_bits
from main_tools import global_vars
from main_tools.housekeeping import process_args, debugPrint, prettyPrintDict
from main_tools.write_files import create_sim_directories, write_sim_results_file
from processInput import processInputFiles
from simulation import macsSwig
from simulation.run_sim import run_macs
from simulation.sim_tools import get_sim_positions, get_sim_positions_old
from summary_statistics import stat_tools
from summary_statistics.germline_tools import run_germline, process_germline_file

verbos = 0


def main(args):
    print ''

    # Enable David's debugging thing
    global_vars.init()
    if(len(sys.argv)>1):
        for arg in sys.argv:
            if arg.startswith("-v"):
                global_vars.verbos = arg.count("v")
    debugPrint(1,"Debug on: Level " + str(global_vars.verbos))


    chr_number = 1
    # Use dictionary keys instead of index keys for args
    args = process_args(args)
    job = str(args['job'])  # must be a number
    print 'JOB', job

    sim_option = args['sim option']

    path = args['path']
    [sim_data_dir, germline_out_dir, sim_results_dir] = create_sim_directories(path)


    processedData =  processInputFiles(args['param file'], args['model file'])

    using_pseudo_array = True
    if not processedData.get('discovery') and not processedData.get('sample') and not processedData.get('daf'):
        using_pseudo_array = False

    debugPrint(3,"#"*22+"param_dict:\n{}".format(prettyPrintDict(processedData['param_dict']))+"#"*22)


    ### Create a list of Sequence class instances. These will contain the bulk of all sequence-based data
    sequences = create_sequences(processedData, args)
    names = [seq.name for seq in sequences]

    n_d = sum([1 for seq in sequences if seq.type == 'discovery'])

    print 'name\ttotal\tpanel\tgenotyped'
    for seq in sequences:
        print '{}\t{}\t{}\t{}'.format(seq.name, seq.tot, seq.panel, seq.genotyped)


    total = sum([seq.tot for seq in sequences])
    print 'total samples:', sum([seq.genotyped for seq in sequences if seq.type=='discovery'] + [seq.tot for seq in sequences if seq.type=='sample'])


    debugPrint(1,"\n-".join(" ".join(processedData['macs_args']).split(" -")))

    ### Define simulation size
    length = processedData['length']

    ##########################################################################
    ################## Perform simulation and get sequences ##################
    ##########################################################################

    ### Flag to check if the simulation works
    SNPs_exceed_available_sites = True
    while SNPs_exceed_available_sites:

        if sim_option == 'macsswig':
            print 'Run macsswig simulation'
            sim = macsSwig.swigMain(len(processedData['macs_args']), processedData['macs_args'])
            print 'Finished macsswig simulation'
            nbss = sim.getNumSites()

            ### Get data from the simulations
            seq_alleles = AllelesMacsSwig(nbss, sim, total) 
            set_seq_bits(sequences, seq_alleles)

            if using_pseudo_array:
                ## get position of the simulated sites and scale it to the "real" position in the SNP chip
                sim_positions = []
                for i in xrange(nbss):
                    position = round(sim.getPosition(i) * float(length))
                    sim_positions.append(position)

            del sim

        elif sim_option == 'macs':
            ### Run macs and make bitarray
            [sequences,position] = run_macs(processedData['macs_args'], sequences)
            nbss = len(sequences[0].bits) / (sequences[0].tot)

            if using_pseudo_array:
                ## get position of the simulated sites and scale it to the "real" position in the SNP chip
                sim_positions = get_sim_positions(position, nbss, length)


        elif sim_option == 'macs_file':
            ### Using a static sim output rather than generating from seed
            seq_alleles = AllelesMacsFile('tests/test_data/sites1000000.txt')
            set_seq_bits(sequences, seq_alleles)
            nbss = len(sequences[0].bits) / (sequences[0].tot)

            if using_pseudo_array:
                ## get position of the simulated sites and scale it to the "real" position in the SNP chip
                sim_positions = get_sim_positions_old(seq_alleles, nbss, length)

        set_discovery_bits(sequences)

        print 'number sites in simulation:', nbss

        ##########################################################################
        ### Create pseudo array according to ascertainment scheme and template ###
        ##########################################################################

        if using_pseudo_array:
            SNPs = get_SNP_sites(args['SNP file'])
            print 'nb Array SNPs:', len(SNPs)

            asc_panel_bits = set_panel_bits(nbss, sequences)
            print 'number of chromosomes in asc_panel:', asc_panel_bits.length()/nbss

            ### Get pseudo array sites
            print 'Make pseudo array'
            [pos_asc, nbss_asc, avail_site_indices, avail_sites] = pseudo_array_bits(asc_panel_bits, processedData['daf'], sim_positions, SNPs)
            nb_avail_sites = len(avail_sites)
        else:
            SNPs = []

        SNPs_exceed_available_sites = ( len(SNPs) >= nb_avail_sites )

    if using_pseudo_array:
        set_asc_bits(sequences, nbss_asc, pos_asc, avail_site_indices)


    ##########################################################################
    ###################### Calculate summary statistics ######################
    ##########################################################################
    res, head  = [], []

    ### Calculate summary stats from genomes
    if nbss > 0:   # Simulations must contain at least one segregating site
        stat_tools.store_segregating_site_stats(sequences, res, head)
        stat_tools.store_pairwise_FSTs(sequences, n_d, res, head)

    ### Calculate summary stats from the ascertained SNPs
    if using_pseudo_array:
        if nbss_asc > 0:
            stat_tools.store_array_segregating_site_stats(sequences, res, head)   
            stat_tools.store_array_FSTs(sequences, res, head)

        print 'Make ped and map files'
        ped_file_name = '{0}/macs_asc_{1}_chr{2}.ped'.format(sim_data_dir, job, str(chr_number))
        map_file_name = '{0}/macs_asc_{1}_chr{2}.map'.format(sim_data_dir, job, str(chr_number))
        out_file_name = '{0}/macs_asc_{1}_chr{2}'.format(germline_out_dir, job, str(chr_number))

        if os.path.isfile(out_file_name + '.match'):  # Maybe remove if statement
            os.remove(ped_file_name)
            os.remove(map_file_name)

        if using_pseudo_array and processedData.get('germline') or processedData.get('pedmap'):
            make_ped_file(ped_file_name, sequences)
            make_map_file(map_file_name, pos_asc, chr_number, avail_sites)

        ### Use Germline to find IBD on pseduo array ped and map files
        do_i_run_germline = int(args['germline'])

        print 'run germline? ' + str(do_i_run_germline)
        if (do_i_run_germline == 0):
            ########################### <CHANGE THIS LATER> ###########################
            ### Germline seems to be outputting in the wrong unit - so I am putting the min at 3000000 so that it is 3Mb, but should be the default.
            # germline = run_germline(ped_file_name, map_file_name, out_file_name, min_m = 3000000)
            germline = run_germline(ped_file_name, map_file_name, out_file_name, min_m=300)
            ########################### </CHANGE THIS LATER> ##########################

        ### Get IBD stats from Germline output
        if os.path.isfile(out_file_name + '.match'):
            print 'Reading Germline IBD output'
            [IBD_pairs, IBD_dict] = process_germline_file(out_file_name, names)

            print 'Calculating summary stats'
            stats = OrderedDict([('num', len), ('mean', np.mean), ('med', np.median), ('var', np.var)])
            stat_tools.store_IBD_stats(stats, IBD_pairs, IBD_dict, res, head)
            stat_tools.store_IBD_stats(stats, IBD_pairs, IBD_dict, res, head, min_val=30)

        print 'finished calculating ss'


    print processedData['param_dict']

    #Previously used for separate files
    '''
    write_results_file(results_sims_dir, job, res, head)
    write_sim_file(sim_values_dir, job, processedData['param_dict'])
    '''
    #Combined file
    write_sim_results_file(sim_results_dir, job, processedData['param_dict'], res, head)
    

    print ''
    print '######################################'
    print '### PROGRAM COMPLETED SUCCESSFULLY ###'
    print '######################################'
    print ''


if __name__ == '__main__':
    main(argv)
