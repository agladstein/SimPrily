import subprocess
import os
from main_tools.housekeeping import debugPrint


def run_macs(macs_args, sequences):
    debugPrint(2,"running macs simulation:")
    position = []
    null = open(os.devnull, 'w')
    proc = subprocess.Popen(macs_args,stdout=subprocess.PIPE,stderr=null)
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
    debugPrint(2,"Finished macs simulation")
    return [sequences,position]