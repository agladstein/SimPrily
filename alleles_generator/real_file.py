import re
from bitarray import bitarray

class AllelesReal(object):

    def __init__(self, real_file_name):
        self.real_file_name = real_file_name

    def make_lists(self):
        """Make list of lists containing alleles from real data modified .tped file (from Consuelo's bash code)
        haploid individuals in rows, sites in columns
        no whitespace"""

        talleles = []
        real_file = open(self.real_file_name, 'r')
        for line in real_file:
            talleles.append(line.strip())
        real_file.close()
        alleles = zip(*talleles)
        return map(list,alleles)

    def make_list_seq(self, n_0, n_m):
        """Make list containing alleles from real data PLINK .tped file.
        sites in rows, individuals in columns (first 4 columns chr, rsnumber, site_begin, site_end).
        plink --bfile bfile --recode transpose 01 --output-missing-genotype N --out tfile01
        https://www.cog-genomics.org/plink2/formats#tped"""

        real_file = open(self.real_file_name, 'r')
        seq_bits = []
        for line in real_file:
            columns = line.split(' ')
            for i in range(n_0+4, n_m+4):
                seq_bits.extend(columns[i])
        real_file.close()
        return seq_bits

    def make_bitarray_seq(self, n_0, n_m):
        """Make bitarray containing alleles from real data PLINK .tped file.
        sites in rows, individuals in columns (first 4 columns chr, rsnumber, site_begin, site_end).
        plink --bfile bfile --recode transpose 01 --output-missing-genotype N --out tfile01
        https://www.cog-genomics.org/plink2/formats#tped

        Deal with missing data by changing all non 0's or 1's to 0.
        This is probably acceptable to data with very low frequency of missing data.
        Should improve by giving option to read PLINK .frq files for each population to change missing data to 0 or 1 with probability based on frequency of allele for each population."""

        real_file = open(self.real_file_name, 'r')
        seq_bits = bitarray()
        for line in real_file:
            columns = line.strip().split(' ')
            for i in range(n_0+4, n_m+4):
                if columns[i] not in ('0', '1'):
                    columns[i] = '0'
                seq_bits.extend(columns[i])
        real_file.close()
        return seq_bits
