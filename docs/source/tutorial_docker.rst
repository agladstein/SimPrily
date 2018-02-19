####################
Tutorial with Docker
####################

1. What do you want to simulate? How many simulations?
2. Create your model.csv and param.txt input files.
3. Perform a small test simulation.

*************************
1. Define your simulation
*************************
a. Draw your model.
b. Estimate the required resources.
c. Decide where to run your simulations.

*********************
2. Create input files
*********************

**************************
3. Perform test simulation
**************************

a. Pull Docker image
====================

**Pull the latest SimPrily Docker image:**
::

    docker pull agladstein/simprily

Once you have successfully pulled the image you will see something like this:
::

    Using default tag: latest
    latest: Pulling from agladstein/simprily
    f49cf87b52c1: Pull complete
    7b491c575b06: Pull complete
    b313b08bab3b: Pull complete
    51d6678c3f0e: Pull complete
    09f35bd58db2: Pull complete
    f7e0c30e74c6: Pull complete
    c308c099d654: Pull complete
    339478b61728: Pull complete
    d16221c2883e: Pull complete
    df211aed0ee8: Pull complete
    94afb574a896: Pull complete
    b253919783b5: Pull complete
    45cb233ca3a5: Pull complete
    Digest: sha256:1de7a99a23264caa22143db2a63794fa34541ccaf9155b9fb50488b5949a9d7d
    Status: Downloaded newer image for agladstein/simprily:latest

**Next, double check the images you've pulled:**
::

    docker image ls

You should see something like this:
::

    REPOSITORY                      TAG                 IMAGE ID            CREATED             SIZE
    agladstein/simprily             latest              1d3fbe956b00        5 hours ago         938MB

b. Run SimPrily
===============

Run one small example with the Docker container
::

    docker run -t -i --mount type=bind,src=/home/agladstein/src/SimPrily,dst=/app agladstein/simprily python /app/simprily.py -p examples/eg1/param_file_eg1.txt -m examples/eg1/model_file_eg1.csv -g genetic_map_b37/genetic_map_GRCh37_chr1.txt.macshs -a array_template/ill_650_test.bed -i 1 -o output_dir -v

You should see something like this:
::

    debug-1: Debug on: Level 1
    JOB 1
    debug-1: name   total   panel   genotyped
    debug-1: A      140     0       140
    debug-1: B      20      0       20
    debug-1: total samples: 160
    debug-1: Perform simulation and get sequences
    debug-1: Number of sites in simulation: 10309
    debug-1: Calculating summary statistics

    #########################
    ### PROGRAM COMPLETED ###
    #########################

Then, you should see a new directory created ``/home/agladstein/src/SimPrily/output_dir``.
In that directory, you should see the directories
::

    sim_data
    germline_out
    results

and the directory ``results`` should have the file ``results_1.txt``, which should look something like this:
::

    A       AN_t    B       AB_t    AN      SegS_A_CGI      Sing_A_CGI      Dupl_A_CGI      TajD_A_CGI      SegS_B_CGISing_B_CGI       Dupl_B_CGI      TajD_B_CGI      FST_AB_CGI
    29380.6397673   1615.50194862   42155.6351482   2546.95287896   10000.0 9795    3880    1283    -1.30415802172  4360       1690    674     -0.488311472745 0.00115531480069



**************************
4. Perform HTC simulations
**************************
