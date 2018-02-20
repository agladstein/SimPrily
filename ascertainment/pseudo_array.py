import sys
from bisect import bisect_right

from main_tools.my_random import MY_RANDOM as random
from main_tools.housekeeping import debugPrint

def find2(a, x):
    """This function receives the array with available sites (sites that passed the frequency cut-off)"""
    '''
    Takes two parameters: a and x. A is a list with the
    length of 2680 that contains integers in ascending order. 
    X is an integer that is 8 digits long and between 15929526
    and 49365777. 

    Returns: example 1 only returns from the len(a) -1 condition, 
    which returns the integer 2679

    Errors: 
    - breaks when x is a string
    '''
    if x <= a[0]: #x is smaller than first value in a
        return 0
    elif x >= a[len(a)-1]: #x is larger than last value in a
        return len(a)-1
    #Find leftmost item greater than or equal to x
    else:
        i = bisect_right(a, x)
        j = i-1
        d1=abs(a[i]-x)
        d2=abs(a[j]-x)
        if d2<d1:
            return j
        elif d1<d2:
            return i
        elif d1==d2:
            return i

def add_snps(avail_sites, nb_avail_sites, pos_asc, nbss_asc):
    ''''
    This function is called 199 times when the program is 
    ran. 
    It five parameters: avail_sites, 
    nb_avail_sites, pos_asc, nbss_asc, nb_array_snps. 
    -avail_sites has a list of floats. Length: 2860
    -nb_avail_sites: 2680
    -pos_asc: list of ints (2481-2679). Increases by one every time the 
        program is ran (lengths increase from 1 to 199).
    -nbss_acs is an int (198)
    -nb_array_snps: 200
    
    Returns: list of ints is ascending order from 2481 to 2679. Length: 9

    Errors: 
    -negative numbers in pos_asc

    Need to figure out how to get it to not return only the pos_asc
    '''   

    first_index=pos_asc[0]
    last_index=pos_asc[-1]
    if(nb_avail_sites>nbss_asc): ###this should happen all the time
        if (last_index<nb_avail_sites-1):
            try:
                avail_sites[last_index+1]
            except:
                print( "well, it WASN'T defined after all!")
                try:
                    avail_sites[first_index-1]
                except:
                    print( "well, it WASN'T defined after all!")
                else:
                    for i in range(len(pos_asc)):
                        pos_asc[i]=pos_asc[i]-1
            else:
                print( "sure, it was defined")
                pos_asc.append(last_index+1)
        elif (last_index==nb_avail_sites-1):
            if(first_index-1)>=0:
                pos_asc.insert(0,first_index-1)
    return pos_asc

def pseudo_array(asc_panel, daf, pos, snps):
    Tasc_panel = zip(*asc_panel)
    print( 'number of sites in Tasc_panel:', len(Tasc_panel))
    print( 'number of chromosomes in Tasc_panel:', len(Tasc_panel[0]))

    #######Array with the available sites given the frequency cut off
    ##array with the frequency of all the simulated snps
    sites_freq = []
    ##array with the available sites, that pass the frequency cut-off
    avail_sites = []  ##this one has the positions of the snps
    index_avail_sites = []  ##this one has the indexes of the snps
    for n in range(len(Tasc_panel)):
        freq_site = float(Tasc_panel[n][0:len(asc_panel)].count('1')) / float(len(asc_panel))
        if freq_site >= daf and freq_site <= 1 - daf:
            sites_freq.append(freq_site)
            avail_sites.append(pos[n])
            index_avail_sites.append(n)
    nb_avail_sites = len(avail_sites)
    if (len(avail_sites) == len(snps)):
        debugPrint(3,"number of avail_sites is equal to the number of Array snps")
        pos_asc = []
        pos_asc = index_avail_sites
        nbss_asc = len(pos_asc)
        flag_nb_asc_snps = 1
    elif (len(avail_sites) > len(snps)):
        debugPrint(3,"number of avail_sites greater than number of Array snps")
        pos_asc = [None] * int(len(snps))  ##indexes of the SNPs that pass the frequency cut-off and position
        for i in range(len(snps)):  # each snp on the snp array on a chromosome
            ## y is the position of the SNPs in the array
            y = snps[i]
            ##find the closest SNP in the array
            closestleft = find2(avail_sites, y)
            if (i > 0 and pos_asc[i - 1] == closestleft and closestleft + 1 < len(avail_sites)):  ##avoid duplicates
                closestleft = closestleft + 1  ##move one position to the right
                pos_asc[i] = closestleft
            elif (i > 0 and pos_asc[i - 1] > closestleft and pos_asc[i - 1] + 1 < len(avail_sites)):
                closestleft = pos_asc[i - 1] + 1
                pos_asc[i] = closestleft
            else:
                pos_asc[i] = closestleft
                ###if I have duplicates at this point, it means that there were not anyt more snps to choose from
                ###closestleft+1 or pos_asc[i-1]+1 == len(avail_sites)
        #####smoothing
        ##last index of the pos_asc
        i = len(pos_asc) - 1
        ##check if there is another position that might work better
        for j in range(0, i):
            if (j == i - 1 and pos_asc[j] + 1 < pos_asc[j + 1] and pos_asc[j] < (len(avail_sites) - 1) and (
                        j + 1) < len(avail_sites)):
                d1 = abs(snps[j] - avail_sites[pos_asc[j]])
                d2 = abs(snps[j] - avail_sites[pos_asc[j] + 1])
                if (d2 < d1):
                    pos_asc[j] = pos_asc[j] + 1

        ##removes duplicates
        pos_asc = (list(set(pos_asc)))
        pos_asc.sort()

        nbss_asc = len(pos_asc)

        if (len(snps) == nbss_asc):
            flag_nb_asc_snps = 1
            debugPrint(3,'Number of asc snps equal to nb array snps')

        if (len(snps) != len(pos_asc)):
            flag_nb_asc_snps = 0
            debugPrint(3,'Number of asc snps not equal to nb array snps')
            diff = int(len(snps) - len(pos_asc))
            for m in range(1, diff + 1):
                pos_asc2 = []
                pos_asc2 = add_snps(avail_sites, nb_avail_sites, pos_asc, nbss_asc)
                pos_asc = pos_asc2
                nbss_asc = len(pos_asc)
                if nbss_asc == len(snps):
                    flag_nb_asc_snps = 1
                    break
                else:
                    flag_nb_asc_snps = 0

        if (flag_nb_asc_snps == 0):  ##it means that the 1st index in pos_asc is 0; and the last is len(avail_sites)-1
            diff = int(len(snps) - len(pos_asc))
            while (len(pos_asc) != len(snps)):
                rand_numb = random.randint(0, len(avail_sites) - 1)
                # print( 'random',rand_numb)
                if rand_numb not in pos_asc:
                    pos_asc.append(rand_numb)
            pos_asc.sort()
            nbss_asc = len(pos_asc)
    print( 'finished making pseudo array')
    return pos_asc, nbss_asc, index_avail_sites, avail_sites


def pseudo_array_bits(asc_panel_bits, daf, pos, snps):
    '''
    Parameters: 
    asc_panel_bits: bitarray
    daf: float (0.0264139586625)
    pos: list of floats in acsending order
    snps: list of ints

    Returns: pos_asc: list of ints (2481-2679)
    nbss_asc: 200
    index_avail_sites: 
    avail_sites: list of floats

    Errors: 
    - the asc_panel_bits needs to be divisible by pos
    - daf cannot be negative or greater than 1
    '''
    n = asc_panel_bits.length()/len(pos)
    n = int(n)
    #######Array with the available sites given the frequency cut off
    ##array with the frequency of all the simulated snps
    sites_freq = []
    ##array with the available sites, that pass the frequency cut-off
    avail_sites = []  ##this one has the positions of the snps
    index_avail_sites = []  ##this one has the indexes of the snps

    i = 0
    for site in range(0, asc_panel_bits.length(), int(n)):
        freq_site = float(asc_panel_bits[site:site + n].count(1) / float(n))
        if freq_site >= daf and freq_site <= 1 - daf:
            sites_freq.append(freq_site)
            avail_sites.append(pos[i])
            index_avail_sites.append(i)
        i=i+1
    nb_avail_sites = len(avail_sites)
    if (len(avail_sites) < len(snps)):
        print( "Error: There are not enough simulated sites in the discovery panel with allele frequency >=",daf,"and <=",1 - daf)
        sys.exit()

    if (len(avail_sites) == len(snps)):
        #debugPrint(3,"Number of avail_sites is equal to the number of Array snps")
        pos_asc = []
        pos_asc = index_avail_sites
        nbss_asc = len(pos_asc)
        flag_nb_asc_snps = 1

    elif (len(avail_sites) > len(snps)):
        #debugPrint(3,"Number of avail_sites greater than number of Array snps")
        pos_asc = [None] * int(len(snps))  ##indexes of the SNPs that pass the frequency cut-off and position
        for i in range(len(snps)):  # each snp on the snp array on a chromosome
            ## y is the position of the SNPs in the array
            y = snps[i]
            ##find the closest SNP in the array
            closestleft = find2(avail_sites, y)
            if (i > 0 and pos_asc[i - 1] == closestleft and closestleft + 1 < len(avail_sites)):  ##avoid duplicates
                closestleft = closestleft + 1  ##move one position to the right
                pos_asc[i] = closestleft
            elif (i > 0 and pos_asc[i - 1] > closestleft and pos_asc[i - 1] + 1 < len(avail_sites)):
                closestleft = pos_asc[i - 1] + 1
                pos_asc[i] = closestleft
            else:
                pos_asc[i] = closestleft
                ###if I have duplicates at this point, it means that there were not anyt more snps to choose from
                ###closestleft+1 or pos_asc[i-1]+1 == len(avail_sites)

        #####smoothing
        ##last index of the pos_asc
        i = len(pos_asc) - 1

        ##check if there is another position that might work better
        for j in range(0, i):
            if (j == i - 1 and pos_asc[j] + 1 < pos_asc[j + 1] and pos_asc[j] < (len(avail_sites) - 1) and (
                        j + 1) < len(avail_sites)):
                d1 = abs(snps[j] - avail_sites[pos_asc[j]])
                d2 = abs(snps[j] - avail_sites[pos_asc[j] + 1])
                if (d2 < d1):
                    pos_asc[j] = pos_asc[j] + 1

        ##removes duplicates
        pos_asc = (list(set(pos_asc)))
        pos_asc.sort()

        nbss_asc = len(pos_asc)
        nb_array_snps = len(snps)

        if (len(snps) == nbss_asc):
            flag_nb_asc_snps = 1
            debugPrint(3,'nb of asc snps equal to nb array snps')

        if (len(snps) != len(pos_asc)):
            flag_nb_asc_snps = 0
           #debugPrint(3,'nb of asc snps not equal to nb array snps')
            diff = int(len(snps) - len(pos_asc))
            for m in range(1, diff + 1):
                pos_asc2 = []
                pos_asc2 = add_snps(avail_sites, nb_avail_sites, pos_asc, nbss_asc)
                pos_asc = pos_asc2
                nbss_asc = len(pos_asc)
                if nbss_asc == len(snps):
                    flag_nb_asc_snps = 1
                    break
                else:
                    flag_nb_asc_snps = 0

        if (flag_nb_asc_snps == 0):  ##it means that the 1st index in pos_asc is 0; and the last is len(avail_sites)-1
            diff = int(len(snps) - len(pos_asc))
            while (len(pos_asc) != len(snps)):
                rand_numb = random.randint(0, len(avail_sites) - 1)
                # print( 'random',rand_numb)
                if rand_numb not in pos_asc:
                    pos_asc.append(rand_numb)
            pos_asc.sort()
            nbss_asc = len(pos_asc)
    #debugPrint(2,'finished making pseudo array')
    return pos_asc, nbss_asc, index_avail_sites, avail_sites