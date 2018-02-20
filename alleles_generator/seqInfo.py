from bitarray import bitarray

from main_tools.housekeeping import debugPrint


class SeqInfo():
    def __init__(self, name, total, seq_type):
        self.name = name
        self.tot = total
        self.type = seq_type  # Either 'discovery' or 'sample'
        self.bits = bitarray()
        self.asc_bits = bitarray()

        ## Discovery-specific variables:
        self.panel = 0  # panel is the number of discovery individuals used to make the pseudoarray, but which do not appear in the pseudoarray
        self.genotyped = 0  # genotyped is the number of discovery individuals in the pseudoarray not used in the panel
        self.CGI_bits = bitarray() if seq_type == 'discovery' else None
        self.pi_CGI = [] if seq_type == 'discovery' else None
        self.pi_asc = None

    def __repr__(self):
        return self.name


def create_sequences(processedData):
    '''
    Parameters: args is a dictionary that maps the SNP file to 
    array_template
    args: a dictionary (seen below in the args parameter)
    processedData: a dictionary (seen below in the args parameter)

    Returns: instance types named [d1, s1]
    '''

    debugPrint(2, "Running create_sequences:")
    sequences = []
    if 'discovery' in processedData and 'sample' in processedData and 'daf' in processedData:
        ### Initialize all discovery type sequence data
        for i, ind in enumerate(processedData.get('discovery')):
            tot_index = processedData['macs_args'].index("-I") + 1 + ind
            tot = int(processedData['macs_args'][tot_index])  # total number of individuals used in simulation
            name = processedData.get('name').pop(0)
            seq = SeqInfo(name, tot, seq_type='discovery')

            seq.genotyped = processedData['I'][ind]
            seq.panel = seq.tot - seq.genotyped
            sequences.append(seq)

        ### Initialize all sample type sequence data
        for i, ind in enumerate(processedData.get('sample')):
            tot = processedData['I'][ind]
            name = processedData.get('name').pop(0)
            seq = SeqInfo(name, tot, seq_type='sample')

            seq.panel = seq.tot
            seq.genotyped = seq.tot
            sequences.append(seq)
    else:
        for tot in processedData["I"][1:]:
            name = processedData.get('name').pop(0)
            seq = SeqInfo(name, tot, seq_type='discovery')

            #  seq.panel = seq.tot #pretty sure it can be deleted
            seq.genotyped = seq.tot
            sequences.append(seq)
    return sequences