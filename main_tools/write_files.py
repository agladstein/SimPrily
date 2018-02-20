import os

def create_sim_directories(path_name):
    """
    
    :param path_name: which is currently output_dir
    :return: dir_list (['output_dir/sim_data', 'output_dir/germline_out', 'output_dir/results'])
    """
    sim_data_dir     = str(path_name)+'/sim_data'
    germline_out_dir = str(path_name)+'/germline_out'
    sim_results_dir  = str(path_name)+'/results'

    ### Check if necessary directories exist.
    dir_list = [sim_data_dir, germline_out_dir, sim_results_dir]
    for d in dir_list:
        try:
            os.makedirs(d)
        except OSError:
            if not os.path.isdir(d):
                raise
    return dir_list


def write_sim_results_file(dir, job, param_dict, res_list, header):
    """
    
    :param dir: output_dir/results
    :param job: 1
    :param param_dict: {'A': '44499.7180488', 'daf': '0.0264139586625', 'B': '40008.4616861', 'AB_t': '2546.95287896', 'AN': '10000.0', 'AN_t': '2113.43905612'}

    :param res_list: [4372, 1724, 590, -0.40890634648504526, 165, 27, 11, 57.40526315789474, 0.970678370998841, 158, 4, 1, 49.15632065775952, 2.3175661604382545, 0.03793034448167276] 
    :param header: ['SegS_D1_CGI', 'Sing_D1_CGI', 'Dupl_D1_CGI', 'TajD_D1_CGI', 'SegS_D1_ASC', 'Sing_D1_ASC', 'Dupl_D1_ASC', 'Pi_D1_ASC', 'TajD_D1_ASC', 'SegS_S1_ASC', 'Sing_S1_ASC', 'Dupl_S1_ASC', 'Pi_S1_ASC', 'TajD_S1_ASC', 'FST_D1_S1_ASC']
    :return: 
    """

    result = '{}/results_{}.txt'.format(dir, job)
    out_file = open(result, 'w')

    params = []
    vals = []
    for param, val in param_dict.items():
        params.append(param)
        vals.append(str(val))
    header = '\t'.join(header)+'\n'
    out = '\t'.join([str(r) for r in res_list]) + '\n'

    out_file.write('\t'.join(params) + '\t' + header)
    out_file.write('\t'.join(vals) + '\t' + out)


def write_stats_file(res_dir, job, res_list, header):
    header = '\t'.join(header)+'\n'
    file_dir_name = '{0}/{1}.summary'.format(res_dir, job)
    out_file  = open(file_dir_name, 'w')
    out_file.write(header)

    out = '\t'.join([str(r) for r in res_list]) + '\n'
    out_file.write(out)
    out_file.close()