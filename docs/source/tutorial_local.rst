e.g. One simulation (with pseudo array and genetic map):
::

    python simprily.py -p examples/eg1/param_file_eg1_asc.txt -m examples/eg1/model_file_eg1_asc.csv -g genetic_map_b37/genetic_map_GRCh37_chr1.txt.macshs -a array_template/ill_650_test.bed -i 1 -o output_dir -v


e.g. One simulation (genetic map, no pseudo array):
::

    python simprily.py -p examples/eg1/param_file_eg1.txt -m examples/eg1/model_file_eg1.csv -g genetic_map_b37/genetic_map_GRCh37_chr1.txt.macshs -i 1 -o output_dir -v
