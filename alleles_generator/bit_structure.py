from bitarray import bitarray

def set_seq_bits(sequences, alleles):
    """Set seq.bits for each sequence in sequences list"""
    seq_loc = 0
    for seq in sequences:
        seq.bits = alleles.make_bitarray_seq(seq_loc, seq_loc + seq.tot)
        seq_loc += seq.tot

def set_discovery_bits(sequences):
    for seq in sequences:
        if seq.type == 'discovery':
            for ind in range(0, len(seq.bits), seq.tot):
                seq.CGI_bits.extend(seq.bits[ind : ind+seq.genotyped])

def set_panel_bits(n, sequences):
    panel_bits = bitarray()
    for site in range(int(n)):
        for seq in sequences:
            if seq.type == 'discovery':
                panel_bits.extend( seq.bits[ site*seq.tot + seq.genotyped : site*seq.tot + seq.tot ] )
    return panel_bits

def set_real_genome_bits(sequences, alleles):
    seq_loc = 0
    for seq in sequences:
        if seq.type == 'discovery':
            seq.CGI_bits = alleles.make_bitarray_seq(seq_loc, seq_loc + seq.genotyped)
            seq_loc += seq.genotyped

def set_real_array_bits(sequences, alleles):
    """Set seq.bits for each sequence in sequences list"""
    seq_loc = 0
    for seq in sequences:
        seq.asc_bits = alleles.make_bitarray_seq(seq_loc, seq_loc + seq.genotyped)
        seq_loc += seq.genotyped
