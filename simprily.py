#!/usr/local/bin/python
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
from main_tools.housekeeping import process_args, debugPrint, profile
from main_tools.write_files import create_sim_directories, write_sim_results_file
from processInput import process_input_files
from simulation.run_sim import run_macs
from simulation.sim_tools import get_sim_positions, get_sim_positions_old
from summary_statistics import stat_tools
from summary_statistics.germline_tools import run_germline, process_germline_file

verbos = 0


def main(args):

    chr_number = 1
    # Use dictionary keys instead of index keys for args
    args = process_args(args)
    job = str(args['job'])  # must be a number
    print('JOB {}'.format(job))

    prof_option = args['profile']

    sim_option = args['sim option']

    path = args['path']
    [sim_data_dir, germline_out_dir, sim_results_dir] = create_sim_directories(path)

    processedData =  process_input_files(args['param file'], args['model file'], args)

    using_pseudo_array = True
    if not processedData.get('discovery') and not processedData.get('sample') and not processedData.get('daf'):
        using_pseudo_array = False

    debugPrint(3, "Finished processing input\nprocessedData: ", processedData)


    ### Create a list of Sequence class instances. These will contain the bulk of all sequence-based data
    sequences = create_sequences(processedData)
    names = [seq.name for seq in sequences]

    n_d = sum([1 for seq in sequences if seq.type == 'discovery'])

    debugPrint(1,'name\ttotal\tpanel\tgenotyped')
    for seq in sequences:
        debugPrint(1,'{}\t{}\t{}\t{}'.format(seq.name, seq.tot, seq.panel, seq.genotyped))

    total = sum([seq.tot for seq in sequences])
    debugPrint(1, 'total samples: {}'.format(sum([seq.genotyped for seq in sequences if seq.type=='discovery'] + [seq.tot for seq in sequences if seq.type=='sample'])))

    ### Define simulation size
    length = processedData['length']
    debugPrint(1, 'Perform simulation and get sequences')
    pedmap = args['pedmap']
    germline = args['germline']

    ##########################################################################
    ################## Perform simulation and get sequences ##################
    ##########################################################################

    ### Flag to check if the simulation works
    SNPs_exceed_available_sites = True
    while SNPs_exceed_available_sites:

        # add genetic map to macs_args list
        macs_args = []
        macs_args = processedData['macs_args']

        if sim_option == 'macsswig':
            print('Run macsswig simulation')
            profile(prof_option, path, job, "start_run_macsswig")
            sim = macsSwig.swigMain(len(macs_args), processedData['macs_args'])
            profile(prof_option, path, job, "end_run_macsswig")
            print('Finished macsswig simulation')
            nbss = sim.getNumSites()

            ### Get data from the simulations
            profile(prof_option, path, job, "start_set_seq_bits")
            seq_alleles = AllelesMacsSwig(nbss, sim, total) 
            set_seq_bits(sequences, seq_alleles)
            profile(prof_option, path, job, "end_set_seq_bits")

            if using_pseudo_array:
                ## get position of the simulated sites and scale it to the "real" position in the SNP chip
                sim_positions = []
                for i in xrange(nbss):
                    position = round(sim.getPosition(i) * float(length))
                    sim_positions.append(position)

            del sim

        elif sim_option == 'macs':
            ### Run macs and make bitarray
            profile(prof_option, path, job, "start_run_macs")
            [sequences,position] = run_macs(macs_args, sequences)
            profile(prof_option, path, job, "end_run_macs")
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

        profile(prof_option, path, job, "start_set_discovery_bits")
        set_discovery_bits(sequences)
        profile(prof_option, path, job, "end_set_discovery_bits")

        debugPrint(1, 'Number of sites in simulation: {}'.format(nbss))

        assert nbss > 10, "Number of sites is less than 10: {}".format(nbss)

        ##########################################################################
        ### Create pseudo array according to ascertainment scheme and template ###
        ##########################################################################

        if using_pseudo_array:
            SNPs = get_SNP_sites(args['SNP file'])
            debugPrint(1, 'Number of SNPs in Array: {}'.format(len(SNPs)))

            profile(prof_option, path, job, "start_set_panel_bits")
            asc_panel_bits = set_panel_bits(nbss, sequences)

            profile(prof_option, path, job, "end_set_panel_bits")
            debugPrint(1,'Number of chromosomes in asc_panel: {}'.format(asc_panel_bits.length()/nbss))


            ### Get pseudo array sites
            debugPrint(2,'Making pseudo array')
            profile(prof_option, path, job, "start_pseudo_array_bits")

            [pos_asc, nbss_asc, avail_site_indices, avail_sites] = pseudo_array_bits(asc_panel_bits, processedData['daf'], sim_positions, SNPs)
            profile(prof_option, path, job, "end_pseudo_array_bits")
            nb_avail_sites = len(avail_sites)
            SNPs_exceed_available_sites = ( len(SNPs) >= nb_avail_sites )
        else:
            SNPs = []
            SNPs_exceed_available_sites = False


    if using_pseudo_array:
        profile(prof_option, path, job, "start_set_asc_bits")
        set_asc_bits(sequences, nbss_asc, pos_asc, avail_site_indices)
        profile(prof_option, path, job, "end_set_asc_bits")


    debugPrint(1, 'Calculating summary statistics')
    ##########################################################################
    ###################### Calculate summary statistics ######################
    ##########################################################################
    res, head  = [], []

    ### Calculate summary stats from genomes
    if nbss > 0:   # Simulations must contain at least one segregating site
        profile(prof_option, path, job, "start_store_segregating_site_stats")
        stat_tools.store_segregating_site_stats(sequences, res, head)
        profile(prof_option, path, job, "end_store_segregating_site_stats")
        profile(prof_option, path, job, "start_store_pairwise_FSTs")
        stat_tools.store_pairwise_FSTs(sequences, n_d, res, head)
        profile(prof_option, path, job, "end_store_pairwise_FSTs")

    ### Calculate summary stats from the ascertained SNPs
    if using_pseudo_array:
        if nbss_asc > 0:
            profile(prof_option, path, job, "start_store_array_segregating_site_stats")
            stat_tools.store_array_segregating_site_stats(sequences, res, head)
            profile(prof_option, path, job, "end_store_array_segregating_site_stats")
            profile(prof_option, path, job, "start_store_array_FSTs")
            stat_tools.store_array_FSTs(sequences, res, head)
            profile(prof_option, path, job, "end_store_array_FSTs")

        debugPrint(2,'Making ped and map files')
        ped_file_name = '{0}/macs_asc_{1}_chr{2}.ped'.format(sim_data_dir, job, str(chr_number))
        map_file_name = '{0}/macs_asc_{1}_chr{2}.map'.format(sim_data_dir, job, str(chr_number))
        out_file_name = '{0}/macs_asc_{1}_chr{2}'.format(germline_out_dir, job, str(chr_number))

        if os.path.isfile(out_file_name + '.match'):  # Maybe remove if statement
            os.remove(ped_file_name)
            os.remove(map_file_name)

        if using_pseudo_array and pedmap or germline:
            profile(prof_option, path, job, "start_make_ped_file")
            make_ped_file(ped_file_name, sequences)
            profile(prof_option, path, job, "end_make_ped_file")
            profile(prof_option, path, job, "start_make_map_file")
            make_map_file(map_file_name, pos_asc, chr_number, avail_sites)
            profile(prof_option, path, job, "end_make_map_file")

        ### Use Germline to find IBD on pseduo array ped and map files
        do_i_run_germline = int(args['germline'])

        debugPrint(1,'run germline? {}'.format("True" if do_i_run_germline else "False"))

        if (do_i_run_germline == True):
            ########################### <CHANGE THIS LATER> ###########################
            ### Germline seems to be outputting in the wrong unit - so I am putting the min at 3000000 so that it is 3Mb, but should be the default.
            profile(prof_option, path, job, "start_run_germline")
            # germline = run_germline(ped_file_name, map_file_name, out_file_name, min_m = 3000000)
            profile(prof_option, path, job, "end_run_germline")
            germline = run_germline(ped_file_name, map_file_name, out_file_name, min_m=300)
            ########################### </CHANGE THIS LATER> ##########################

        ### Get IBD stats from Germline output
        if os.path.isfile(out_file_name + '.match'):
            print('Reading Germline IBD output')
            profile(prof_option, path, job, "start_process_germline_file")
            [IBD_pairs, IBD_dict] = process_germline_file(out_file_name, names)
            profile(prof_option, path, job, "end_process_germline_file")

            print('Calculating summary stats')
            stats = OrderedDict([('num', len), ('mean', np.mean), ('med', np.median), ('var', np.var)])
            profile(prof_option, path, job, "start_store_IBD_stats")
            stat_tools.store_IBD_stats(stats, IBD_pairs, IBD_dict, res, head)
            stat_tools.store_IBD_stats(stats, IBD_pairs, IBD_dict, res, head, min_val=30)
            profile(prof_option, path, job, "end_store_IBD_stats")

        debugPrint(1,'finished calculating ss')


    #Previously used for separate files
    '''
    write_results_file(results_sims_dir, job, res, head)
    write_sim_file(sim_values_dir, job, processedData['param_dict'])
    '''
    #Combined file
    write_sim_results_file(sim_results_dir, job, processedData['param_dict'], res, head)
    

    print('')
    print('#########################')
    print('### PROGRAM COMPLETED ###')
    print('#########################')
    print('')

    profile(prof_option, path, job, "COMPLETE")

if __name__ == '__main__':
    main(argv)
