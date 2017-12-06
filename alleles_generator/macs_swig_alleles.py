from bitarray import bitarray

class AllelesMacsSwig(object):
    """Make list of lists containing alleles from macsSwig."""

    def __init__(self, nbss, sim, total):
        """

        :param nbss: Number of simulated sites
        :param sim: Result of macsSwig simulation
        :param total: Total number of haploid simulated individuals
        """
        self.nbss = nbss
        self.sim = sim
        self.total = total

    def make_lists(self):
        alleles = []
        for x in xrange(0, self.nbss):
            loc = []
            for m in xrange(0, self.total):
                loc.append(self.sim.getSite(x, m))
            alleles.append(loc)
        return alleles

    def make_bitarray_seq(self, n_0, n_m):
        """Make bitarray containing alleles from macsswig sim output for one population (equivalent of seq lists)."""
        seq_bits = bitarray()
        for site in xrange(0, self.nbss):
            for indiv in xrange(n_0, n_m):
                seq_bits.extend(self.sim.getSite(site,indiv))
        return seq_bits
