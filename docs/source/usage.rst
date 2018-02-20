#####
Usage
#####

For quick help:
::

    python simprily.py --help

e.g. One simulation (with pseudo array and genetic map):
::

    python simprily.py -p examples/eg1/param_file_eg1_asc.txt -m examples/eg1/model_file_eg1_asc.csv -g genetic_map_b37/genetic_map_GRCh37_chr1.txt.macshs -a array_template/ill_650_test.bed -i 1 -o output_dir -v


e.g. One simulation (genetic map, no pseudo array):
::

    python simprily.py -p examples/eg1/param_file_eg1.txt -m examples/eg1/model_file_eg1.csv -g genetic_map_b37/genetic_map_GRCh37_chr1.txt.macshs -i 1 -o output_dir -v


______________________________________

``simprily.py`` takes 4 required arguments and 2 optional arguments, and help, verbose, and profile options.

Run as
::

    python simprily.py [-h] -p PARAM -m MODEL -i ID -o OUT [-g MAP] [-a ARRAY] [-v] [--profile]

**************
Required Input
**************

-p PARAM  The location of the parameter file
-m MODEL  The location of the model file
-i ID     The unique identifier of the job
-o OUT    The location of the output directory

or

--param PARAM  The location of the parameter file
--model MODEL  The location of the model file
--id ID        The unique identifier of the job
--out OUT      The location of the output directory

**************
Optional Input
**************
-h            Shows a help message and exists
-v            Increase output verbosity. This includes 3 levels, ``-v``, ``-vv``, and ``-vvv``
--profile     Print a log file containing the time in seconds and memory use in Mb for main functions
-g MAP        The location of the genetic map file
-a ARRAY      The location of the array template file, in `bed format <http://bedtools.readthedocs.io/en/latest/content/general-usage.html>`_. The third column is used as the physical positions of the SNP for the pseudo array.

or

--help         Shows a help message and exists
-v             Increase output verbosity. This includes 3 levels, ``-v``, ``-vv``, and ``-vvv``
--profile      Print a log file containing the time in seconds and memory use in Mb for main functions
--map MAP      The location of the genetic map file
--array ARRAY  The location of the array template file, in `bed format <http://bedtools.readthedocs.io/en/latest/content/general-usage.html>`_. The third column is used as the physical positions of the SNP for the pseudo array.

*****************************************
Additional information on input arguments
*****************************************

ID
--
This is a unique identifier for the job. It is used in the names of the output files.
For example, the output file with parameter values and summary statistics is named ``results_{IDid}.txt``.

output_dir
----------
This is where all the output goes.
Within the output_dir the directory ``results`` will always be created. The ``results`` directory contains the results file ``results_{jobid}.txt`` with the parameter values and summary statistics.
Additionally, the directories ``germline_out`` and ``sim_data`` are also created, but will be empty if the ``germline`` or ``pedmap`` arguments in the model file are not included.

*Be careful when running large numbers of jobs (>2000). It is bad practice to run large numbers of jobs and direct all the output to the same directory, because listing the contents of the directory becomes very slow. Instead, we recommend creating directory "buckets". See section Recommendations for other HTC workflows*.

param_file.txt
--------------
Examples of param_file.txt can be found in examples.
The param_file.txt must define the parameters of the demographic model and the minimum derived allele frequency to be used to create the pseudo array, if a pseudo array is to be created.

All time parameters must end in ``_t``.

All parameter values should be given in pre-coalescent scaled units.
That is, Ne should be given in units of chromosomes, and time should be given in units of generations.
The code will scale to the appropriate coalescent units for the simulation.

The definition can be hard-coded parameter values, such as:
::

    A = 1000
    B = 1000
    T1_t = 100


The definition can be a prior, such as:
::

    A = (1e3.0:1e4.0)
    B = (1e3.0:1e4.0)
    T1_t = (10:500)

Log base 10 can be used for the parameter definitions by using ``1eX`` or ``1Ex``.
This is recommended when using a prior with a very large range (See ABCtoolbox manual).

If pseudo arrays are to be created, the derived allele frequency must be defined. For example,
::

    A = (1e3.0:1e4.0)
    B = (1e3.0:1e4.0)
    T1_t = (10:500)
    daf = (0.01:0.1)


*currently only a range of values is supported for daf. Therefore if you want to hard code a value, use the same value as the min and max of the prior.*

model_file.csv
--------------
Examples of model_file.csv can be found in examples.

The demographic model, SNP ascertainment model, and additional options are defined in the model_file.csv.
The demographic model defines events in populations' history, including population divergence, instantanious effective population size changes, exponential growth, gene flow and admixture. We use a coalescent simulation, so models must be defined backwards in time, starting from the present, with each event going back in the past. The SNP ascertainment model defines how to create a pseudo SNP array using a template SNP array, a set of discovery populations and a minor allele frequency cutoff. The SNP ascertainment model should be used when comparing to real SNP array data.

All instances of any argument must start with a dash followed by the corresponding argument parameters,
and value(s).
Each new argument must be a new line.
All variables and values must be separated by commas (white space will be ignored, so it is okay to include spaces).
The model arguments can appear in any order.

All parameters must be called with a name corresponding to its definition in the param file.
This is how parameter values are assigned to the simulation model.
For example,
::

    -macs,./bin/macs,
    -length,5000000,
    -s,1231414,
    -t,2.5e-8,
    -r,1e-8,
    -h,1e5,
    # define a sample size of 50 haploid individuals for populations 1 and 2
    -I, 2, 50, 50
    # define the effective population size at present for population 1
    -n, 1, A
    # define the effective population size at present for population 2
    -n, 2, B
    # define a divergence event (join backwards in time) between populations 1 and 2
    -ej, T1, 1, 2


**Setup simulation arguments**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
One of the following two flags must be included:

``-macs``
    use the original simulator `MaCS <https://github.com/gchen98/macs>`_. This option will stream the MaCS simulation output directly to be read into a python bitarray.

``-macs_file``
    read in static output from MaCS. This should only be used for rigorous testing.

Following the ``-macs`` and ``-macs_file`` flags there should be a path to either the executable or static file in relation to the working directory. For example:

    If you are using a virtual environment the path to macs should be
    ::

        -macs, ./bin/macs


    If you are using Docker or Singularity the path to macs should be
    ::

        -macs, /app/macs

    or if you want to use a static file,

    ::

        -macs_file, tests/test_data/sites1000000.txt


``-length``
    The number base pairs you want to simulate. Must be included.

``-s``
    random seed.
    Must be an integer.
    If no input is given, no seed will be used, and everything will be random.
    If a seed is provided, reproducible parameters will be picked from the priors.
    Using a seed will also cause reproducible simulations with macs.

**Demographic simulation arguments**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
All argument flags are based on macs arguments (see macs and ms manual for more detail).

``-t``: mutation rate per site per 4N generations

``-d``: enable debugging messages. No entry will default to allowing debugging messages. This will not work when using macsswig

``-h``: history. Refers to the number of previous base pairs to retain

``-r [r]``:  recombination rate per site per 4N generations

``-c [f lambda]``: f = ratio of gene conversion rate to crossover rate. track len(lambda) is mean length of tract in base pairs.
*This has not been tested.*

``-T``: Print each local tree in Newick format to standard out. *This has not been tested.*

``-G [alpha]``: Assign growth rate alpha across populations where alpha=-log(Np/Nr).

``-I [n n_n]``: Assign all elements of the migration matrix for n populations.
Values in matrix set to mig_rate/(n-1).
The length of n_n should be equal to n

``-m [i,j m]``: i, j is associated with a location in the migration matrix
m is assigned to the value at (i, j)

``-ma [m_nn]``: Assign values to all elements of migration matrix for n populations

``-n [i size]``: Population i set to size

``-g [i alpha]``: assigns alpha value as explained in -G to population i

``-eG [t alpha]``: t is a time value.
alpha behaves the same as in -G

``-eg [t i alpha]``:
t is a time value.
alpha behaves the same as in -G.
i is a population that alpha is assigned to at time t.

``-eM [t m]``:
t is a time value.
Assign migration rate m to all elements in migration matrix at
time t

``-em [t i,j m_ij]``:
t is a time value.
i and j make up point in a population matrix.
assigns migration rate m_ij to the population at i, j at time t

``-ema [t n m_nn]``:
t is a time value.
Assign migration rates  within the migration matrix for n
populations at time t.

``-eN [t size]``:
t is a time value.
Assigns size to all populations at time t

``-en [t i size_i]``:
t is a time value.
assigns size_i to population i at time t

``-es [t i p]``:
t is a time value.
splits population i by p at time t

``-ej [t i j]``
t is a time value.
joins population i with population j at time t

**SNP array ascertainment arguments**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If the user would like to create a pseudo array from the simulation, the array template must be included in the command line argument with the flag ``-a``, and four additional arguments must be included in the model_file:

``-discovery``, followed by the populations (defined by their numbers from ``-n``) that should be used to discover the SNP (e.g. the HapMap populations).
These are the populations that will be used to create the pseudo array.
When calculating summary statistics, summary statistics based on whole genome simulation and pseudo array will be calculated for these populations.

``-sample``, followed by the populations (defined by their numbers from ``-n``) that are the samples of interest for demographic interest.

``-daf``, followed by the parameter name for daf.

``-random_discovery``, followed by ``True`` or ``False``.
True will add a random number of individuals to the discovery populations to use as the "panel" to create the pseudo array.
When this option is False, the total number of simulated discovery populations is equal to the number "genotyped" and in the "panel".


For example:
::

    -macs,./bin/macs,
    -length,5000000,
    -s,1231414,
    -t,2.5e-8,
    -r,1e-8,
    -h,1e5,
    -I, 2, 50, 50
    -n, 1, A
    -n, 2, B
    -ej, T1, 1, 2
    -discovery, 1
    -sample, 2
    -daf, daf
    -random_discovery, True



An example of an array template is:
::

    chr22	0	15929526
    chr22	0	15991515
    chr22	0	16288162
    chr22	0	16926611
    chr22	0	16990146
    chr22	0	17498992
    chr22	0	17540297
    chr22	0	17728199
    chr22	0	17760714
    chr22	0	18180154
    chr22	0	18217275
    chr22	0	18220413



**Ordering of time-specific events**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
When using priors, if some demographic events must happen in a certain order, the order can be specified by adding the order number to the argument.
For example say there are two demographic events, a population split and instantaneous growth, but the instantaneous growth must happen before the population split, we can indicate that in the model file:
::

    -en_1, Tgrowth, 1, A2
    -ej_2, Tsplit, 2, 1


Additionally, the same format can be used to indicate that multiple events should happen at the same time.
If there are multiple events that should happen at the same time, the word ``inst`` should be used instead of a time parameter after the first definition of the time.
*(this will actually cause the times to be just different enough that macs is happy.)*
For example, say we wanted growth to occur at the same time as the population split:
::

    -en_1, Tgrowth, 1, A2
    -ej_1, inst, 2, 1

In this case, the population split will technically be simulated slightly after the growth.

**germline**
^^^^^^^^^^^^
*currently has a bug*

The option ``-germline`` can be included in the model_file to use `GERMLINE <https://github.com/sgusev/GERMLINE>`_ to find shared IBD segments between all simulated individuals from pseudo array.
Does not use the genetic map to run GERMLINE.
Runs GERMLINE as:
::

    bash ./bin/phasing_pipeline/gline.sh ./bin/germline-1-5-1/germline  ped_name map_name out_name "-bits 10 -min_m min_m"


If GERMLINE does not run, try rebuilding it on the machine you are trying to run on:
::

    cd ./bin/germline-1-5-1
    make clean
    make


**pedmap**
^^^^^^^^^^
The option ``-pedmap`` can be included in the model_file to print a ped and map file of the pseudo array data.
