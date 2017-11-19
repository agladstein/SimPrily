
import re
from bitarray import bitarray


class AllelesMacsFile(object):
    def __init__(self, macs_file_name):
        self.macs_file_name = macs_file_name

    def make_lists(self):
        """Make list of lists containing alleles from macs sites output file.
        macs sites output file is made by
        macs 20 1000 -t 0.001 -r 0.0004 -s 100000 -h 1e5 -I 2 10 10 -ej 0.0025 1 2 >trees.txt 1> sites.txt"""

        alleles = []
        position = []
        macs_file = open(self.macs_file_name, 'r')
        for line in macs_file:
            if re.match('SITE', line):
                columns = line.split('\t')
                site_alleles = list(columns[4].strip())
                alleles.append(site_alleles)
                position.append(columns[2])
        macs_file.close()
        return [alleles,position]

    def make_bitarray(self):
        """Make bitarray containing alleles from macs sites output file.
        macs sites output file is made by
        macs 20 1000 -t 0.001 -r 0.0004 -s 100000 -h 1e5 -I 2 10 10 -ej 0.0025 1 2 >trees.txt 1> sites.txt"""
        macs_file = open(self.macs_file_name, 'r')
        alleles_bits = bitarray()
        position = []
        for line in macs_file:
            if re.match('SITE', line):
                columns = line.split('\t')
                site_alleles = columns[4].strip()
                alleles_bits.extend(site_alleles)
                position.append(columns[2])
        macs_file.close()
        return [alleles_bits,position]

    def make_bitarray_seq(self, n_0, n_m):
        """Make bitarray containing alleles from macs sites output file for one population (equivalent of seq lists).
        macs sites output file is made by
        macs 20 1000 -t 0.001 -r 0.0004 -s 100000 -h 1e5 -I 2 10 10 -ej 0.0025 1 2 >trees.txt 1> sites.txt"""
        macs_file = open(self.macs_file_name, 'r')
        seq_bits = bitarray()
        for line in macs_file:
            if re.match('SITE', line):
                columns = line.split('\t')
                site_alleles = columns[4].strip()
                for i in xrange(n_0, n_m):
                    seq_bits.extend(site_alleles[i])
        macs_file.close()
        return seq_bits
