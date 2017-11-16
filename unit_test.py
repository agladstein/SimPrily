
import unittest
from main_tools.housekeeping import process_args
from summary_statistics.afs_stats_bitarray import Pi2, Tajimas, FST2, count_bit_differences, base_S_ss
from alleles_generator.seqInfo import create_sequences, SeqInfo
from ascertainment.pseudo_array import find2, add_snps, pseudo_array_bits
from main_tools.write_files import create_sim_directories
from simulation.run_sim import run_macs
from alleles_generator.macs_file import AllelesMacsFile
from alleles_generator import seq
from bitarray import bitarray
import random


class TestFns(unittest.TestCase):


    def test_run_macs(self):
        '''
        length of return position list: 10752

        '''
        macs_args = ['./bin/macs', '166.0', '1000000', '-I', '2', '26', '140', '-t', '0.00444997180488', '-s', '1231', '-r', '0.00177998872195', '-h', '1e5', '-R', 'genetic_map_b37/genetic_map_GRCh37_chr1.txt.macshs', '-n', '1', '1.0', '-n', '2', '0.899072251249', '-en', '0.0118708617304', '1', '0.224720524949', '-ej', '0.0143090794261', '2', '1', '-R', 'genetic_map_b37/genetic_map_GRCh37_chr1.txt.macshs']
        d1 = {'pi_CGI': [], 'name': 'D1', 'asc_bits': bitarray(), 'type': 'discovery', 'genotyped': 20, 'tot': 26, 'CGI_bits': bitarray(), 'pi_asc': None, 'bits': bitarray(), 'panel': 6}
        s1 = {'pi_CGI': None, 'name': 'S1', 'asc_bits': bitarray(), 'type': 'sample', 'genotyped': 140, 'tot': 140, 'CGI_bits': None, 'pi_asc': None, 'bits': bitarray(), 'panel': 140}
        sequences = [d1, s1]
        d1_return = {'pi_CGI': None, 'name': 'S1', 'asc_bits': bitarray(), 'type': 'sample', 'genotyped': 140, 'tot': 140, 'CGI_bits': None, 'pi_asc': None, 'bits': bitarray('00110001100'), 'panel': 6}
        s1_return = {'pi_CGI': None, 'name': 'S1', 'asc_bits': bitarray(), 'type': 'sample', 'genotyped': 140, 'tot': 140, 'CGI_bits': None, 'pi_asc': None, 'bits': bitarray('00110001100'), 'panel': 140}
        return_sequences = [d1_return, s1_return]
        return_position = ['0.01', '5.023']
        check = run_macs(macs_args, sequences)
       # self.assertEquals(check[0][0], d1_return)
       # self.assertEquals(check, [return_sequences, return_position])


    def test_create_sim_directories(self):
        pathname = 'output_dir'
        theta = create_sim_directories(pathname)
        check =  ['output_dir/sim_data', 'output_dir/germline_out', 'output_dir/results']
        self.assertEquals(theta, check)

    def test___init__seqInfo(self):
        '''
        Reference class test
        '''
        name = "string"
        total = 12
        seq_type = "sample"
        a = SeqInfo(name, total, seq_type)
        self.assertEquals(a.tot, total)

        name = []
        total = 12
        seq_type = "sample"
        a = SeqInfo(name, total, seq_type)
        self.assertEquals(a.name, name)

        name = "string"
        total = 12.0
        seq_type = bitarray()
        a = SeqInfo(name, total, seq_type)
        self.assertEquals(a.tot, total)
        
    def test_create_sequences(self):
        '''
        Parameters: args is a dictionary that maps the SNP file to 
        array_template
        args: a dictionary (seen below in the args parameter)
        processedData: a dictionary (seen below in the args parameter)
        
        Returns: instance types named [d1, s1] 
        '''
        args = {'SNP file': 'array_template/ill_650_test.bed', 
        'sim option': 'macs', 'germline': 1, 'model file': 
        'examples/eg1/model_file_eg1.csv', 'job': '1', 
        'command': 'simprily.py', 'param file': 
        'examples/eg1/param_file_eg1.txt', 'random discovery': 
        True, 'path': 'output_dir'}
        processed_data = {'param_dict': {'A': '44499.7180488', 
        'daf': '0.0264139586625', 'B': '40008.4616861', 'AB_t': 
        '(1600:4100)', 'AN': '10000.0', 'AN_t': '2113.43905612'}, 
        'daf': 0.0264139586625, 'macs': './bin/macs', 'macs_args': 
        ['./bin/macs', '166.0', '1000000', '-I', '2', '26', '140', '-t', 
        '0.00444997180488', '-s', '1231', '-r', '0.00177998872195', '-h',
         '1e5', '-R', 'genetic_map_b37/genetic_map_GRCh37_chr1.txt.macshs',
          '-n', '1', '1.0', '-n', '2', '0.899072251249', '-en', 
          '0.0118708617304', '1', '0.224720524949', '-ej', '0.0143090794261',
           '2', '1'], 'I': [20, 140], 'sample': [2], 'length': '1000000', 
           'seed': '1231', 'discovery': [1]}        
        check = create_sequences(processed_data, args)
        values1 = {'pi_CGI': [], 'name': 'D1', 'asc_bits': bitarray(), 
        'type': 'discovery', 'genotyped': 20, 'tot': 26, 'CGI_bits': 
        bitarray(), 'pi_asc': None, 'bits': bitarray(), 'panel': 6}
        values2 = {'pi_CGI': None, 'name': 'S1', 'asc_bits': 
        bitarray(), 'type': 'sample', 'genotyped': 140, 'tot':
         140, 'CGI_bits': None, 'pi_asc': None, 'bits': 
         bitarray(), 'panel': 140}
        self.assertEquals(check[0].__dict__, values1)
        self.assertEquals(check[1].__dict__, values2)


    def test_base_S_ss(self):
        '''
        This function is called upon 

        Parameters: seq_bits has a bitarray that is 28000 characters long,
        n is an integer (changes every time it is called,
        it is typically two digits but occasionally is 3)

        Returns: a list that contains ints as the first 3 indices
        and a list of ints at the fourth index. 

        Errors: 
        - floats, strings, and lists for n
        - nonbinary characters, strings, lists, and ints in bitarray
        due to line 12 (.length() attribute)

        Negative ints for n, odd numbers in seq_bits pass
        A LARGE NUMBER (20+) WILL RESULT IN A MASSIVE LIST OF 
        LISTS THAT IS TOO LARGE TO TEST FOR. THE PROGRAM
        WILL NOT CRASH
        '''
        bits1 = bitarray('1101010100101001')
        n = -12
        check = base_S_ss(bits1, n)
        self.assertEquals(check, [0, 0, 0, []])


        bits1 = bitarray('1101010100101001111')
        n = 3
        check = base_S_ss(bits1, n)
        self.assertEquals(check, [5, 5, 5, [3, 2]])

        bits1 = bitarray('1')
        n = 3
        check = base_S_ss(bits1, n)
        self.assertEquals(check, [0, 0, 0, [0, 0]])

        bits1 = bitarray('11111')
        n = 16
        check = base_S_ss(bits1, n)
        self.assertEquals(check, [0, 0, 0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])


    def test_Pi2(self):
        spec = [3,2,1]
        n = len(spec) + 1
        theta = Pi2(spec, n)
        self.assertEquals(theta, round(3.3333333333333333, 15))
      
        spec = [4,3,2,1]
        n = len(spec) + 1
        theta = Pi2(spec, n)
        self.assertEquals(theta, 5.000000000000001)

        spec = []
        n = len(spec) + 1
        theta = Pi2(spec, n)
        self.assertEquals(theta, 0.0)


    def test_Tajimas(self):
        '''
        Tajimas is a function that is called three times with
        three different parameter sets. 

        Parameters: p, S, and n are all floats. they are passed in that 
        order. 
        Here are the parameters expected
        when the program is ran correctly with float, int, int
        
        N and S cannot be a floats because of lines 39 and 50. They 
        also cannot go below 4. 

        Returns: floats 0.408906346485, 0.970678370999, 2.31756616044
        '''
        check = Tajimas(4, 4, 4)
        self.assertEquals(check, 7.801229937910614)

        check2 = Tajimas(555, 555, 555)
        self.assertEquals(check2, 17.73840973343963)

        check3 = Tajimas(3, 4, 5)
        self.assertEquals(check3, 3.6915718471543735)

        #testing integers: positive, zero, and negative
     
    def test_FST2(self):
        '''
        Parameters for example 1: 
        seq1_bits: 4000 binary characters 
        pi1: 57.4052631579
        n1: 20
        seq2_bits: 28000 binary characters
        pi2: 49.1563206578
        n2: 140
        
        Returns: fst, which is a float.  when ran using example 1 as of 10/11/17
        fst from example 1 is 0.0379303444817. 

        Errors:
        -length of seq2_bits and seq1_bits needs to be divisible by n1 and n2
        -length of the seq_bit lengths and n1 or n2 are the same
        -negative numbers and zeroes are input as n1, n2, seq1_bits, and seq2_bits.
        -if the two seq_bits lengths are different, there will be an error. This 
        should not throw an error
        '''
        bits1 = bitarray('1101010100101001')
        bits2 = bitarray('1101010100101001')
        check = FST2(bits1, 57.4052631579, 4, bits1, 49.1563206578, 4)
        self.assertEquals(check, -29.446166804485717)

        bits1 = bitarray('1111111111111111')
        bits2 = bitarray('1000111100000000')
        check = FST2(bits1, 0, 4, bits2, 0, 4)
        self.assertEquals(check, 1.0)
        # this indicates that 0 is an acceptable parameter for pi1 and pi2

        bits1 = bitarray('1000111100000000')
        bits2 = bitarray('0000000000000000')
        check = FST2(bits1, 200000, 4, bits2, 400001, 4)
        self.assertEquals(check, -239999.0)
        
        
    def test_count_bit_differences(self):
        '''
        This function takes two binary sequences and compares the 
        lengths between the two. If they are not equal, it returns false
        Parameters: s1 and s2 are both binary sequences

        Returns: 

        Errors:
        - with strings, ints, and lists
        '''
        bits = bitarray('0000000000000000')
        bits2 = bitarray('0000000000000000')
        check = count_bit_differences(bits, bits2)
        self.assertEquals(check, 0.0)

    def test_find2(self):
        '''
        Takes two parameters: a and x. A is a list with the
        length of 2680 that contains integers in ascending order. 
        X is an integer that is 8 digits long and between 15929526
        and 49365777. 

        Returns: example 1 only returns from the len(a) -1 condition, 
        which returns the integer 2679

        Errors: 
        - breaks when x is a string
        '''
        a = [1,2,3,4]
        x = 213
        check = find2(a, x)
        self.assertEquals(check, 3)

        a = [-1,-2,-3]
        x =213
        check = find2(a, x)
        self.assertEquals(check, 2)

        a = [0]
        x = 2
        check = find2(a, x)
        self.assertEquals(check, 0)

        a = [-1212121212]
        x = -1
        check = find2(a, x)
        self.assertEquals(check, 0)

        a = [-1212121212]
        x = -1212121212
        check = find2(a, x)
        self.assertEquals(check, 0)

        a = ["-1212121212", "312423"]
        x = -1212121212
        check = find2(a, x)
        self.assertEquals(check, 0)

        a = ["hey", "312423"]
        x = [22]
        check = find2(a, x)
        self.assertEquals(check, 0)

    def test_add_snps(self):
        ''''
        This function is called 199 times when the program is 
        ran. 
        It five parameters: avail_sites, 
        nb_avail_sites, pos_asc, nbss_asc, nb_array_snps. 
        -avail_sites has a list of floats. Length: 2860
        -nb_avail_sites: 2680
        -pos_asc: list of ints (2481-2679). Increases by one every time the 
            program is ran (lengths increase from 1 to 199).
        -nbss_acs is an int (198)
        -nb_array_snps: 200
        
        Returns: list of ints is ascending order from 2481 to 2679. Length: 9

        Errors: 
        -negative numbers in pos_asc

        Need to figure out how to get it to not return only the pos_asc
        '''
        avail_sites = [21313211242134.0, 234234.0]
        nb_avail_sites = 2680
        pos_asc = [3000, 3000, 3000]
        nbss_acs  = 198
        nb_array_snps = 200
        check = add_snps(avail_sites, nb_avail_sites, pos_asc, nbss_acs, nb_array_snps)
        self.assertEquals(check, [3000, 3000, 3000])

        avail_sites = [1.0, 2.0]
        nb_avail_sites = 1000
        pos_asc = [12, 12, 12]
        nbss_acs = 23
        nb_array_snps = 200
        check = add_snps(avail_sites, nb_avail_sites, pos_asc, nbss_acs, nb_array_snps)
        self.assertEquals(check, [12, 12 ,12])

        avail_sites = [21313211242134]
        nb_avail_sites = 3000
        pos_asc = [-1, -1, 3000]
        nbss_acs  = 23
        nb_array_snps = 200
        check = add_snps(avail_sites, nb_avail_sites, pos_asc, nbss_acs, nb_array_snps)
        self.assertEquals(check, [-1, -1, 3000])

        # this one is defined
        avail_sites = [1.0, 1.0, 2.0, 3.0, 4.0, 5.0]
        nb_avail_sites = 24
        pos_asc = [12, -1, 2]
        nbss_acs  = 23
        nb_array_snps = 200
        check = add_snps(avail_sites, nb_avail_sites, pos_asc, nbss_acs, nb_array_snps)
        self.assertEquals(check, [12, -1, 2, 3])

        # defined, even though nbss_acs is negative and a float
        avail_sites = [1,  3, 4, 5]
        nb_avail_sites = 5
        pos_asc = [12, -1, 2]
        nbss_acs  = -1
        nb_array_snps = 200
        check = add_snps(avail_sites, nb_avail_sites, pos_asc, nbss_acs, nb_array_snps)
        self.assertEquals(check, [12, -1, 2, 3])

        # not defined
        avail_sites = [1, 9000, 5]
        nb_avail_sites = 5
        pos_asc = [12, 8000001, 2]
        nbss_acs  = -1
        nb_array_snps = 200
        check = add_snps(avail_sites, nb_avail_sites, pos_asc, nbss_acs, nb_array_snps)
        self.assertEquals(check, [12, 8000001, 2])

        '''
        def test_pseudo_array(self):
        Parameters: asc_panel, daf, pos, snps 

        This function does
        not appear to be called by any of the examples (verified by 
        print statements and commenting out the function)
        '''     
       
    def test_pseudo_array_bits(self):
        '''
        Parameters: 
        asc_panel_bits: bitarray
        daf: float (0.0264139586625)
        pos: list of floats in acsending order
        snps: list of ints

        Returns: pos_asc: list of ints (2481-2679)
        nbss_asc: 200
        index_avail_sites: 
        avail_sites: list of floats

        Errors: 
        - the asc_panel_bits needs to be divisible by pos
        - daf cannot be negative or greater than 1
        '''
        asc_panel_bits = bitarray('1001100110011001')
        daf = .02
        pos = [1.02, 1.03, 1.04, 1.05]
        snps = [12, 13 ,15]
        check = pseudo_array_bits(asc_panel_bits, daf, pos, snps)
        self.assertEquals(check,  (([1, 2, 3], 3, [0, 1, 2, 3], [1.02, 1.03, 1.04, 1.05])))

        #tests negative numbers in pos parameter
        asc_panel_bits = bitarray('1001100110011001')
        daf = .02
        pos = [-1.02, -1.03, -1.04, -1.05]
        snps = [12, 13 ,15]
        check = pseudo_array_bits(asc_panel_bits, daf, pos, snps)
        self.assertEquals(check, ([1, 2, 3], 3, [0, 1, 2, 3], [-1.02, -1.03, -1.04, -1.05]))

        # even number in snps
        asc_panel_bits = bitarray('1001100110011001')
        daf = .02
        pos = [-1.02, -1.03, -1.04, -1.05]
        snps = [12, 13]
        check = pseudo_array_bits(asc_panel_bits, daf, pos, snps)
        self.assertEquals(check, ([2, 3], 2, [0, 1, 2, 3], [-1.02, -1.03, -1.04, -1.05]))

        # odd number of asc_panel_bits and pos  
        asc_panel_bits = bitarray('10011001100')
        daf = .02
        pos = [-1.02, -.00000000000103, 12000000000]
        snps = [12, 13, .02]
        check = pseudo_array_bits(asc_panel_bits, daf, pos, snps)
        self.assertEquals(check, ([0, 1, 2], 3, [0, 1, 2], [-1.02, -1.03e-12, 12000000000]))


        # one value for pos and snps 
        asc_panel_bits = bitarray('10011001100')
        daf = .01
        pos = [-1.02]
        snps = [12]
        check = pseudo_array_bits(asc_panel_bits, daf, pos, snps)
        self.assertEquals(check, ([0], 1, [0], [-1.02]))

        # one value for pos and snps 
        asc_panel_bits = bitarray('10011001100')
        daf = .01
        pos = [4290345925890245902345092]
        snps = [12]
        check = pseudo_array_bits(asc_panel_bits, daf, pos, snps)
        self.assertEquals(check, ([0], 1, [0], [4290345925890245902345092L]))


    def test_alleles(self):
            alleles_macs_file = AllelesMacsFile('tests/test_data/sites.txt')
            alleles = alleles_macs_file.make_lists()[0]
            self.maxDiff = None
            expected_alleles = [
                ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0'],
                ['0', '0', '1', '0', '0', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
                ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '1'],
                ['0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '1', '0', '0', '0'],
                ['0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
                ['0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0'],
                ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0'],
                ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0'],
                ['1', '1', '0', '0', '0', '0', '1', '1', '1', '1', '0', '1', '1', '1', '1', '0', '1', '1', '1', '1'],
                ['0', '0', '1', '1', '1', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0', '1', '0', '0', '1', '1'],
                ['1', '1', '0', '0', '0', '0', '1', '1', '1', '1', '0', '1', '1', '1', '1', '0', '1', '1', '0', '0'],
                ['0', '0', '1', '1', '1', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0', '1', '0', '0', '1', '1'],
                ['0', '0', '0', '0', '0', '0', '1', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
                ['0', '0', '1', '1', '1', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0'],
                ['0', '0', '1', '1', '1', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0'],
                ['1', '1', '0', '0', '0', '0', '1', '1', '1', '1', '0', '1', '1', '1', '1', '0', '1', '1', '1', '1'],
                ['1', '1', '0', '0', '0', '0', '1', '1', '1', '1', '0', '1', '1', '1', '1', '0', '1', '1', '1', '1'],
                ['1', '1', '0', '0', '0', '0', '1', '1', '1', '1', '0', '1', '1', '1', '1', '0', '1', '1', '1', '1'],
                ['0', '0', '1', '1', '1', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0'],
                ['0', '0', '1', '1', '1', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0'],
                ['1', '1', '0', '0', '0', '0', '1', '1', '1', '1', '0', '1', '1', '1', '1', '0', '1', '1', '1', '1'],
                ['0', '0', '1', '1', '1', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0'],
                ['1', '1', '0', '0', '0', '0', '1', '1', '1', '1', '0', '1', '1', '1', '1', '0', '1', '1', '1', '1'],
                ['0', '0', '1', '1', '1', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0'],
                ['0', '0', '1', '1', '1', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0'],
                ['1', '1', '0', '0', '0', '0', '1', '1', '1', '1', '0', '1', '1', '1', '1', '0', '1', '1', '1', '1'],
                ['0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
                ['0', '0', '1', '1', '1', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0'],
                ['1', '1', '0', '0', '0', '0', '1', '1', '1', '1', '0', '1', '1', '1', '1', '0', '1', '1', '1', '1'],
                ['0', '1', '0', '0', '0', '0', '1', '1', '0', '1', '0', '1', '0', '0', '1', '0', '1', '0', '0', '0'],
                ['0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
                ['0', '0', '1', '1', '1', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0', '1', '0', '0', '0', '0'],
                ['1', '1', '0', '0', '0', '0', '1', '1', '1', '1', '0', '1', '1', '1', '1', '0', '1', '1', '1', '1'],
                ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0'],
                ['1', '1', '0', '0', '0', '0', '1', '1', '1', '1', '0', '1', '1', '1', '1', '0', '1', '1', '1', '1'],
                ['0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0'],
                ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0'],
                ['1', '1', '0', '0', '0', '0', '1', '1', '0', '1', '0', '1', '1', '1', '1', '0', '1', '1', '0', '0']]
            self.assertListEqual(alleles, expected_alleles)

'''
        def test_seq(self):
            seqA = seq.create_seq(self.test_alleles(),0,10)
            seqB = seq.create_seq(self.test_alleles(),10,20)
            self.maxDiff = None
            expected_seqA = [('0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '0', '0', '0', '1', '1', '1', '0', '0',
                        '1', '0', '1', '0', '0', '1', '0', '0', '1', '0', '0', '0', '1', '0', '1', '0', '0', '1'), (
                       '0', '0', '0', '1', '0', '0', '0', '0', '1', '0', '1', '0', '0', '0', '0', '1', '1', '1', '0', '0',
                       '1', '0', '1', '0', '0', '1', '0', '0', '1', '1', '0', '0', '1', '0', '1', '1', '0', '1'), (
                       '0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '1', '1', '0', '0', '0', '1', '1',
                       '0', '1', '0', '1', '1', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0'), (
                       '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '1', '1', '0', '0', '0', '1', '1',
                       '0', '1', '0', '1', '1', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0'), (
                       '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '1', '1', '0', '0', '0', '1', '1',
                       '0', '1', '0', '1', '1', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0'), (
                       '0', '1', '0', '0', '1', '0', '0', '0', '0', '1', '0', '1', '0', '1', '1', '0', '0', '0', '1', '1',
                       '0', '1', '0', '1', '1', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0'), (
                       '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '1', '0', '0', '1', '1', '1', '0', '0',
                       '1', '0', '1', '0', '0', '1', '0', '0', '1', '1', '0', '0', '1', '0', '1', '0', '0', '1'), (
                       '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '0', '0', '0', '1', '1', '1', '0', '0',
                       '1', '0', '1', '0', '0', '1', '0', '0', '1', '1', '1', '0', '1', '0', '1', '0', '0', '1'), (
                       '0', '0', '0', '0', '0', '1', '0', '0', '1', '0', '1', '0', '0', '0', '0', '1', '1', '1', '0', '0',
                       '1', '0', '1', '0', '0', '1', '1', '0', '1', '0', '0', '0', '1', '0', '1', '0', '0', '0'), (
                       '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '1', '0', '0', '1', '1', '1', '0', '0',
                       '1', '0', '1', '0', '0', '1', '0', '0', '1', '1', '0', '0', '1', '0', '1', '0', '0', '1')]
            expected_seqB = [('0', '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '1', '1', '0', '0', '0', '1', '1', '0',
                  '1', '0', '1', '1', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0'), (
                 '0', '0', '0', '1', '0', '0', '0', '1', '1', '0', '1', '0', '0', '0', '0', '1', '1', '1', '0', '0', '1',
                 '0', '1', '0', '0', '1', '0', '0', '1', '1', '0', '0', '1', '0', '1', '0', '0', '1'), (
                 '0', '0', '0', '0', '0', '1', '0', '0', '1', '0', '1', '0', '0', '0', '0', '1', '1', '1', '0', '0', '1',
                 '0', '1', '0', '0', '1', '0', '0', '1', '0', '0', '0', '1', '0', '1', '0', '1', '1'), (
                 '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '0', '0', '0', '1', '1', '1', '0', '0', '1',
                 '0', '1', '0', '0', '1', '0', '0', '1', '0', '0', '0', '1', '1', '1', '0', '0', '1'), (
                 '1', '0', '0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '0', '0', '0', '1', '1', '1', '0', '0', '1',
                 '0', '1', '0', '0', '1', '0', '0', '1', '1', '0', '0', '1', '0', '1', '0', '0', '1'), (
                 '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '1', '1', '0', '0', '0', '1', '1', '0',
                 '1', '0', '1', '1', '0', '0', '1', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0'), (
                 '0', '0', '0', '1', '0', '0', '0', '0', '1', '0', '1', '0', '0', '0', '0', '1', '1', '1', '0', '0', '1',
                 '0', '1', '0', '0', '1', '0', '0', '1', '1', '0', '0', '1', '0', '1', '1', '0', '1'), (
                 '0', '0', '0', '0', '0', '0', '1', '0', '1', '0', '1', '0', '0', '0', '0', '1', '1', '1', '0', '0', '1',
                 '0', '1', '0', '0', '1', '0', '0', '1', '0', '0', '0', '1', '0', '1', '0', '0', '1'), (
                 '0', '0', '1', '0', '0', '0', '0', '0', '1', '1', '0', '1', '0', '0', '0', '1', '1', '1', '0', '0', '1',
                 '0', '1', '0', '0', '1', '0', '0', '1', '0', '0', '0', '1', '0', '1', '0', '0', '0'), (
                 '0', '0', '1', '0', '0', '0', '0', '0', '1', '1', '0', '1', '0', '0', '0', '1', '1', '1', '0', '0', '1',
                 '0', '1', '0', '0', '1', '0', '0', '1', '0', '0', '0', '1', '0', '1', '0', '0', '0')]
            self.assertListEqual(seqA,expected_seqA)
            self.assertListEqual(seqB,expected_seqB)

        def test_alleles_bitarray(self):
            alleles_macs_file = AllelesMacsFile('tests/test_data/sites.txt')
            alleles_bits = alleles_macs_file.make_bitarray()[0]
            self.maxDiff = None
            expected_alleles_bits = bitarray('0000000000000010000000100100001000000000000000000000000000110100000000010000100000000100000000000000000000001000100000000000000000000000010000000000000100000000110000111101111011110011110000100001001111000011110111101100001111000010000100110000001001000000000000111100001000010000001111000010000100001100001111011110111111000011110111101111110000111101111011110011110000100001000000111100001000010000110000111101111011110011110000100001000011000011110111101111001111000010000100000011110000100001000011000011110111101111000000001000000000000011110000100001000011000011110111101111010000110101001010000000000100000000000000111100001000010000110000111101111011110000000000000100000011000011110111101111010000000000000010000000000000001000000011000011010111101100')
            self.assertEqual(alleles_bits, expected_alleles_bits)

        def test_seq_bitarray(self):
            seq_macs_file = AllelesMacsFile('tests/test_data/sites.txt')
            seqA_bits = seq_macs_file.make_bitarray_seq(0, 10)
            seqB_bits = seq_macs_file.make_bitarray_seq(10, 20)
            self.maxDiff = None
            expceted_seqA_bits = bitarray('00000000000010010000000000000001000000000000010000000000001000000000000000000000110000111100111100001100001111001111000000000010010011110000001111000011000011111100001111110000111100111100000011110000110000111100111100001100001111001111000000111100001100001111000000001000111100001100001111010000110100000001000011110000110000111100000000001100001111010000000000000000001100001101')
            expceted_seqB_bits = bitarray('00001000001000000000000000001101000010000000000000001000000000000001000100000000011110111110000100110111101100100001001100000000001000010000100001000001111011110111101111011110111110000100001000010000011110111110000100000111101111100001000010000100000111101111000000000010000100000111101111010010100000000000001000010000011110111100010000000111101111000000100000100000000111101100')
            self.assertEqual(seqA_bits,expceted_seqA_bits)
            self.assertEqual(seqB_bits,expceted_seqB_bits)

'''


def main():
    test = unittest.defaultTestLoader.loadTestsFromTestCase(TestFns)
    results = unittest.TextTestRunner().run(test)
    print('Correctness score = ', str((results.testsRun - len(results.errors) - len(results.failures)) / results.testsRun * 100) + ' / 100')
    
if __name__ == "__main__":
    main()

