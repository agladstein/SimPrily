from math import sqrt

def base_S_ss(seq,nbsites):
    """Finds the number of segregating sites, number of singletons, number of doubletons, and allele frequency spectrum"""
    spec_zero = []
    for g in range(len(seq) - 1):
        spec_zero.append(0)
    var_ss = 0  # Segregating sites
    alleles = zip(*seq)
    for g in range(nbsites):
        if 0 < list(alleles[g]).count('1') < (list(alleles[g]).count('1') + list(alleles[g]).count('0')):  ##this ignores sites that have all zeros, or all ones
            var_ss = var_ss + 1
            spec_zero[list(alleles[g]).count('1') - 1] = spec_zero[list(alleles[g]).count('1') - 1] + 1
    if var_ss > 0:
        Ns = spec_zero[0] + spec_zero[-1]  ##number of singletons
        Nd = spec_zero[1] + spec_zero[-2]  ##number of dupletons
    else:
        Ns = 0
        Nd = 0
    return [var_ss, Ns, Nd, spec_zero]

def Pi2(spec,n):
    """Standard pi, calculated from allele frequency spectrum
    n= sample size (in chromosomes)"""
    theta_pi=0.0
    for g in range(len(spec)):
        theta_pi=theta_pi+(2.0*float(spec[g])*(g+1.0)*(n-(g+1.0)))/(n*(n-1.0))
    return theta_pi

def Tajimas(p,S,n):
    """Calculates Tajima's D.
    Takes in pi, number of segregating sites, and number of chromosomes"""
    if (S==0):
        return 0
    else:
        a1=0.0
        for g in range(n-1):
            a1=a1+(1.0/(g+1.0))
        a2=0.0
        for g in range(n-1):
            a2=a2+(1.0/((g+1.0)**2))
        b1=(n+1.0)/(3.0*(n-1.0))
        b2=(2*((n**2.0)+n+3))/((9*n)*(n-1))
        c1=b1-(1.0/a1)
        c2=b2-((n+2.0)/(a1*n))+(a2/(a1**2.0))
        e1=c1/a1
        e2=c2/((a1**2.0)+a2)
        TajD=(p-(S/a1))/(sqrt((e1*S)+((e2*S)*(S-1.0))))
        return TajD

def FST2(seq1,pi1,nseq1,seq2,pi2,nseq2):
    """FST based on pi within populations and between populations"""
    k3=0
    #Pi within populations
    pw=(pi1+pi2)/2
    for i in xrange(len(seq1)):
        si = seq1[i]
        for j in xrange(len(seq2)):
            k3=k3+hamming_distance(seq1[i],seq2[j])
    pb=k3/(float(nseq1)*float(nseq2))
    if (pb==0):
        return '0'
    else:
        fst=float(1-(pw/pb))
        return fst

def hamming_distance(s1, s2):
    """Hamming distance between two strings of equal length is the number of positions at which the corresponding symbols are different"""
    assert len(s1) == len(s2)
    return sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))