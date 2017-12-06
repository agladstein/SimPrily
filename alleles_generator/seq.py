
def create_seq(alleles,n_0,n_m):
    Talleles = zip(*alleles)
    seq = Talleles[n_0:n_m]
    return seq
