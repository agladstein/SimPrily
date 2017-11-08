'''
def create_seq(alleles,n_0,n_m):
    print("THESE ARE THE PARAMTERS OF create_seq: " + str(alleles),
        str(n_0), str(n_m))
    Talleles = zip(*alleles)
    seq = Talleles[n_0:n_m]
    print("THIS IS SEQ THE RETURN OF CREATE SEQ : " + str(seq))
    return seq
    '''