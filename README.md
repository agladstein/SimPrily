# SimPrily

Created by Ariella Gladstein, based on code from Consuelo Quinto Cortes and Krishna Veeramah.
Also worked on by David Christy, Logan Gantner, and Mack Skodiak.  
agladstein@email.arizona.edu

## About
SimPrily runs genome simulations with user defined parameters or parameters randomly generated by priors and computes genomic statistics on the simulation output.  
Version 1

1. Run genome simulation with model defined by prior distributions of parameters and demographic model structure.
2. Take into account SNP array ascertainment bias by creating pseudo array based on priors of number of samples of discovery populations and allele frequency cut-off.
3. Calculate genomic summary statistics on simulated genomes and pseudo arrays. 

This is ideal for use with Approximate Bayesian Computation on whole genome or SNP array data.

Uses c++ programs macs and GERMLINE. For more information on these programs, see:  
https://github.com/gchen98/macs  
https://github.com/sgusev/GERMLINE  

## Install

cd to the directory you want to work in,
```bash
git clone https://github.com/agladstein/SimPrily.git
```

#### Environment Set up
If using Vagrant (this is recommended if running on non-Linux OS):

```bash
vagrant up
vagrant ssh
``` 

```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python-virtualenv git python-dev
sudo easy_install -U distribute
cd ~
virtualenv simprily_env
source ~/simprily_env/bin/activate
pip install --upgrade pip
pip install pip-tools
cd /vagrant
pip-sync
~/simprily_env/bin/python simprily.py examples/eg1/param_file_eg1.txt examples/eg1/model_file_eg1.csv macs 1 array_template/ill_650_test.bed 1 False out_dir
```

If not using Vagrant:
```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python-virtualenv git python-dev
sudo easy_install -U distribute
virtualenv simprily_env
pip install --upgrade pip
pip install pip-tools
pip-sync
simprily_env/bin/python simprily.py examples/eg1/param_file_eg1.txt examples/eg1/model_file_eg1.csv macs 1 array_template/ill_650_test.bed 0 True output_dir
```


## Usage

e.g. One Test simulation:  
```
python simprily.py examples/eg1/param_file_eg1.txt examples/eg1/model_file_eg1.csv macs 1 array_template/ill_650_test.bed 1 False out_dir
```

#### Input  
`simprily.py` takes 8 arguments.   

Run as  
```
python simprily.py param_file.txt model_file.csv sim_option jobID array_template germline output_dir
```
1. `param_file.txt` = full path to file containing parameter values or priors
2. `model_file.csv` = full path to file containing model commands
3. `sim_option` = macs or macsswig
4. `jobID` = can be any unique value to identify the output  
5. `array_template` = bed file with physical position of SNPs on array to use as template for simulated pseudo array.  
6. `germline` = 0 to run GERMLINE, 1 to not run GERMLINE. ##Change this flag  
7. `random_discovery` = True to randomly pick number of individuals for SNP discovery, or False to use half of the discovery individuals.
8. `output_dir` = path to the directory to output to. No argument will use the default of current dir `.` 


#### Output
Four subdirectories are created in the directory specified in the `output_dir` argument.  
```
output_dir/sim_values
output_dir/results_sims
output_dir/sim_data
output_dir/germline_out
```

##### Intermediate files
Intermediate files go to `output_dir/sim_data` and `output_dir/germline_out`.    
`output_dir/sim_data` contains PLINK formated .ped and .map files created from the pseudo array, which are necessary to run GERMLINE.  
`output_dir/germline_out` contains the GERMLINE .match output and .log. The .match contains all of the identified IBD segments.  
These files are NOT automatically removed in python script, but are unnecessary once the job is complete.  

##### Results files
Output files go to `output_dir/sim_values` and `output_dir/results_sims`.  
`output_dir/sim_values` contains the parameter values used in the simulation.
The first line is a header with the parameter names.
The second line is the parameter values.  
`output_dir/results_sims` contains the summary statistics calculated from the simulation.
The first line is a header with the summary statistics names.
The second line is the summary statistics values.

-------------------------

## Open Science Grid

Run interactively with the Singularity container on the OSG  
```bash
[agladstein@login02 SimPrily]$ singularity shell --home $PWD:/srv --pwd /srv /cvmfs/singularity.opensciencegrid.org/agladstein/simprily\:latest
Singularity: Invoking an interactive shell within container...

$ python simprily.py examples/eg1/param_file_eg1.txt examples/eg1/model_file_eg1.csv macs 1 array_template/ill_650_test.bed 1 False out_dir
```

-------------------------


## Known Issues
* Seed with macsswig is unstable. 
* If exponential growth is large, macs simulation will not finish. (This is a macs bug).
* If the same id is used with the same output dir as a previous run, the .map file will be appended to.