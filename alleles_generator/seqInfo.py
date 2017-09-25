from bitarray import bitarray

from main_tools.my_random import MY_RANDOM as random


class SeqInfo():
    def __init__(self, name, total, seq_type):
        self.name = name
        self.tot  = total
        self.type = seq_type   # Either 'discovery', 'sample' or 'split sample'
        self.bits = bitarray()
        self.asc_bits = bitarray()
        ## Discovery-specific variables:
        self.panel    = 0   # panel is the number of discovery individuals used to make the pseudoarray, but which do not appear in the pseudoarray
        self.ignore   = 0   # ignore is the number of discovery individuals in the pseudoarray not used in the panel
        self.CGI_bits = bitarray() if seq_type == 'discovery' else None
        self.pi_CGI   = []         if seq_type == 'discovery' else None
        self.pi_asc   = None

    def __repr__(self):
        return self.name

def create_sequences(processedData, args):
    
    sequences = []
    ### Initialize all discovery type sequence data
    
    for i, ind in enumerate(processedData.get('discovery')):
        # commented out, probably a debug print
        # print("ind: " + str(type(ind)))
        tot = processedData['I'][ind-1]
        name = 'D' + str(i+1)
        seq = SeqInfo(name, tot, seq_type = 'discovery')

        if args['random discovery'] == 'True':
            seq.ignore = random.randint(4, seq.tot-1) # number of ignored cannot be less than 4 in order for Tajima's D to iterate
        else:
            assert seq.tot%2 == 0 # population total must be even in this case
            seq.ignore = seq.tot//2
        seq.panel  = seq.tot - seq.ignore
        sequences.append(seq)

    ### Initialize all sample type sequence data
    for i, ind in enumerate(processedData.get('sample')):
        tot = processedData['I'][ind-1]
        name = 'S' + str(i+1)
        seq = SeqInfo(name, tot, seq_type = 'sample')

        seq.panel = seq.tot
        sequences.append(seq)

    return sequences


def create_real_sequences(processedData, args):
    sequences = []
    ### Initialize all discovery type sequence data

    for i, ind in enumerate(processedData.get('discovery')):
        tot = processedData['I'][ind - 1]
        name = 'D' + str(i + 1)
        seq = SeqInfo(name, tot, seq_type='discovery')

        seq.ignore = random.randint(4,seq.tot - 1)  # number of ignored cannot be less than 4 in order for Tajima's D to iterate

        seq.panel = seq.tot - seq.ignore
        sequences.append(seq)

    ### Initialize all sample type sequence data
    for i, ind in enumerate(processedData.get('sample')):
        tot = processedData['I'][ind - 1]
        name = 'S' + str(i + 1)
        seq = SeqInfo(name, tot, seq_type='sample')

        seq.panel = seq.tot
        sequences.append(seq)

    return sequences