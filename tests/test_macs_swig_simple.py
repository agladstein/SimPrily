import unittest

from alleles_generator.macs_swig_alleles import AllelesMacsSwig
from simulation import macsSwig


class TestAllelesMacsSwig(unittest.TestCase):
    def test_basic(self):

        mu = 2.5e-8
        rho = 1e-8
        na = 10
        nb = 10
        total = na + nb
        NA = float(10000)
        T = 50
        macs_theta = float(mu * 4 * NA)
        macs_rho = float(rho * 4 * NA)
        scaled_T = float(T / (4 * NA))
        length = 1000

        macs_args = ['macs', str(na + nb), str(length), '-s', '3239188', '-t', str(macs_theta), '-r', str(macs_rho), '-h',
                     '1e5', '-R', 'genetic_map_b37/genetic_map_GRCh37_chr1.txt.macshs', '-I', '2',
                     str(na), str(nb), '-ej', str(scaled_T), '1', '2']

        sim = macsSwig.swigMain(len(macs_args), macs_args)

        nbss = sim.getNumSites()

        pos = []
        for i in xrange(nbss):
            position = round(sim.getPosition(i) * (length))
            pos.append(position)

        alleles_macsswig = AllelesMacsSwig(nbss,sim,total)
        alleles = alleles_macsswig.make_lists()
        del sim

        self.maxDiff = None
        expected_alleles = [['1', '1', '1', '1', '0', '1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1'],
         ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
         ['0', '0', '0', '1', '0', '1', '1', '1', '0', '1', '0', '0', '1', '0', '0', '0', '0', '0', '0', '1'],
         ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1'],
         ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1', '0', '0']]
        #self.assertListEqual(alleles, expected_alleles)

if __name__ == '__main__':
    unittest.main()