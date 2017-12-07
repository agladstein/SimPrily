import sys
if (sys.version_info > (3, 0)):
    import summary_statistics.afs_stats_bitarray as afs_stats_bitarray
else:
    import afs_stats_bitarray


def store_segregating_site_stats(seq_list, results, head_list):
    for seq in seq_list:
        if seq.type == 'discovery':
            current_res = afs_stats_bitarray.base_S_ss( seq.CGI_bits, seq.genotyped )
            seq.pi_CGIs = afs_stats_bitarray.Pi2( current_res.pop(3), seq.genotyped )
            current_res.append( afs_stats_bitarray.Tajimas( seq.pi_CGIs, current_res[0], seq.genotyped ) )

            results.extend(current_res)
            head_list.extend([c+str(seq.name)+'_CGI' for c in ['SegS_', 'Sing_', 'Dupl_', 'TajD_']])

def store_pairwise_FSTs(seq_list, n, results, head_list):
    for i in range(n-1):
        for j in range(i+1, n):
            seq1 = seq_list[i]
            seq2 = seq_list[j]

            size1 = seq1.genotyped if seq1.type == 'discovery' else seq1.tot
            size2 = seq2.genotyped if seq2.type == 'discovery' else seq2.tot

            results.append(afs_stats_bitarray.FST2( seq1.CGI_bits, seq1.pi_CGIs, size1, seq2.CGI_bits, seq2.pi_CGIs, size2 ))
            head_list.append('FST_' + str(seq1.name) + str(seq2.name) + '_CGI')

def store_IBD_stats(stat_dict, pair_list, pair_dict, results, head_list, min_val=0):
    """Stores IBD statistics specifically for IBD exceeding min_val Mb"""
    for choice in stat_dict:
        stat_func = stat_dict[choice]
        for pair in pair_list:
            data = [d for d in pair_dict[pair] if d >= min_val]
            if choice != 'num' and len(data) < 1:
                data = [0]

            results.append( stat_func(data) )
            if min_val == 0:
                head_list.append('IBD_{}_{}'.format(choice,pair))
            else:
                head_list.append('IBD{}_{}_{}'.format(min_val, choice, pair))

def store_array_segregating_site_stats(seq_list, results, head_list):
    for seq in seq_list:

        asc_bits = seq.asc_bits
        n = seq.genotyped if seq.type == 'discovery' else seq.tot

        code_asc = []
        ss_code_asc = afs_stats_bitarray.base_S_ss(asc_bits, n)
        if (ss_code_asc[0] == 0):
            for i in xrange(5):
                code_asc.append(0)
            pi_code_asc = 0
        else:
            code_asc.extend( afs_stats_bitarray.base_S_ss(asc_bits, n) )
            pi_code_asc = afs_stats_bitarray.Pi2(code_asc[3], n)
            code_asc.append(pi_code_asc)
            code_asc.append(afs_stats_bitarray.Tajimas(pi_code_asc, code_asc[0], n))
            del (code_asc[3])
        seq.pi_asc = pi_code_asc

        results.extend( code_asc )

        head_list.extend(['{0}_{1}_ASC'.format(code, seq.name) for code in ['SegS', 'Sing', 'Dupl', 'Pi', 'TajD']]) 

def store_array_FSTs(seq_list, results, head_list):
    for seq1 in seq_list:
        for seq2 in seq_list:
            if seq_list.index(seq2) > seq_list.index(seq1):
                size1 = seq1.genotyped if seq1.type == 'discovery' else seq1.tot
                size2 = seq2.genotyped if seq2.type == 'discovery' else seq2.tot

                results.append( afs_stats_bitarray.FST2( seq1.asc_bits, seq1.pi_asc, size1, seq2.asc_bits, seq2.pi_asc, size2) )
                head_list.append('FST_{}_{}_ASC'.format(seq1.name, seq2.name))