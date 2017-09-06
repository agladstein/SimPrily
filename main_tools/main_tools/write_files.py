import os

def create_sim_directories(path_name):
    sim_data_dir     = str(path_name)+'/sim_data'
    germline_out_dir = str(path_name)+'/germline_out'
    sim_values_dir   = str(path_name)+'/sim_values'
    results_sims_dir = str(path_name)+'/results_sims'

    ### Check if necessary directories exist.
    dir_list = [sim_data_dir, germline_out_dir, sim_values_dir, results_sims_dir]
    for d in dir_list:
        try:
            os.makedirs(d)
        except OSError:
            if not os.path.isdir(d):
                raise
    return dir_list

def write_sim_file(sim_dir, job, param_dict):
    param_file = '{}/sim_{}_values.txt'.format(sim_dir, job)
    out_file = open(param_file,'w')

    params = []
    vals = []
    for param, val in param_dict.items():
        params.append(param)
        vals.append(str(val))

    out_file.write('\t'.join(params) + '\n')
    out_file.write('\t'.join(vals) + '\n')

    out_file.close()

def write_results_file(res_dir, job, res_list, header):
    header = '\t'.join(header)+'\n'
    file_dir_name = '{0}/ms_output_{1}.summary'.format(res_dir, job)
    out_file  = open(file_dir_name, 'w')
    out_file.write(header)

    out = '\t'.join([str(r) for r in res_list]) + '\n'
    out_file.write(out)
    out_file.close()