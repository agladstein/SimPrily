import subprocess
import os
from main_tools.housekeeping import debugPrint


def run_macs(macs_args, sequences):
    """
    :param macs_args:     ['./bin/macs', '166.0', '1000000', '-I', '2', '26', '140',
     '-t', '0.00444997180488', '-s', '1231', '-r', '0.00177998872195', 
     '-h', '1e5', '-n', '1', '1.0', '-n', '2', '0.899072251249', '-en',
    '0.0118708617304', '1', '0.224720524949', '-ej', '0.0143090794261',
     '2', '1', '-R', 'genetic_map_b37/genetic_map_GRCh37_chr1.txt.macshs']
    :param sequences: [A, B], which is a sequence type
    :return: sequences, which is a list of two instance types stored as 
    [A, B]
    position: list of floats cast as strings, length: 10752
    the floaty strings increase from '0.000178136752' to '     0.99995896'
    """

    debugPrint(2,"running macs simulation:")
    position = []
    null = open(os.devnull, 'w')
    proc = subprocess.Popen(macs_args,stdout=subprocess.PIPE,stderr=null)
    #debugPrint(3,"macs command: {}".format(" ".join(macs_args)))
    while True:
        line = proc.stdout.readline()
        line = line.rstrip()
        # line = line.decode("utf-8") 
        if line != b'':
            if line.startswith(b"SITE:"):
                columns = line.split(b'\t')
                site_alleles = columns[4].strip()
                position.append(columns[2])
                seq_loc = 0
                for seq in sequences:
                    seq.bits.extend(site_alleles[seq_loc:seq_loc + seq.tot])
                    seq_loc += seq.tot
            # elif not line.isnum():
            #     debugPrint(3,line)
        else:
            break
 #   debugPrint(2,"Finished macs simulation")
    return [sequences,position]