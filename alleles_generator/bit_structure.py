from bitarray import bitarray

def set_seq_bits(sequences, alleles):
    """Set seq.bits for each sequence in sequences list"""
    seq_loc = 0
    for seq in sequences:
        seq.bits = alleles.make_bitarray_seq(seq_loc, seq_loc + seq.tot)
        seq_loc += seq.tot

def set_discovery_bits(seq_list):
    for seq in seq_list:
        if seq.type == 'discovery':
            for ind in xrange(0, len(seq.bits), seq.tot):
                seq.CGI_bits.extend(seq.bits[ind : ind+seq.ignore])

def set_panel_bits(n, seq_list):
    panel_bits = bitarray()
    for site in xrange(n):
        for seq in seq_list:
            if seq.type == 'discovery':
                panel_bits.extend( seq.bits[ site*seq.tot + seq.ignore : site*seq.tot + seq.tot ] )
    return panel_bits