####################
Tutorial with Docker
####################

1. What do you want to simulate? How many simulations?
2. Create your model.csv and param.txt input files.
3. Perform a small test simulation.
4. Perform high-throughput simulations.

*************************
1. Define your simulation
*************************
**What do you want to simulate? How many simulations?**
    Suppose we want to simulate a full chromosome with a locus size of 200Mb,
    with a two population split model, with one population size change,
    where there first population has a sample size of 10 diploid individuals
    and the second population has a sample size of 70 diploid individuals.
    And we want to use priors on all of parameters.
    Suppose we want a total of 50,000 simulations.

**Draw your model.**
    Do this on paper first.
::

        ____
        |   |
        | 1 |
        |_ _|-en
         | |____
         | ___ |-ej
         | | | |
         | | | |
          1   2

*********************
2. Create input files
*********************

Create the model_file_tutorial.csv and param_file_tutorial.txt files.

**model_file_tutorial.csv**
::

    # Use the simulator MaCS
    -macs,./bin/macs,
    # Simulate a locus size of 10kb. Start with 10kb, then increase to 200Mb
    -length,10000,
    # Use a mutation rate of 2.5e-8
    -t,2.5e-8,
    # Use a recombination rate of 1e-8
    -r,1e-8,
    # Tell MaCS to retain 1e5 previous base pairs
    -h,1e5,
    # Two populations, first with sample size 10 diploid individuals and 2nd with sample size 70 diploid individuals
    -I,2,20,140,
    # Effective population size of population 1 defined as A
    -n,1,A,
    # Effective population size of population 2 defined as B
    -n,2,B,
    # Divergence event from 1 to 2
    -ej,AB_t,2,1,
    # Population size change in population 1 to size AN
    -en,AN_t,1,AN

**param_file_tutorial.txt**
::

    A = (1e3:1e4.0)
    B = (1e3:1e4.0)
    AB_t = (1000:4000)
    AN_t = (0:4000)
    AN = (1e4:1e5.0)


**************************
3. Perform test simulation
**************************

*Docker requires sudo privileges. If you do not have sudo, use Singularity.*

Check that Docker is installed:
::

    sudo docker run hello-world

Quick and easy install script provided by Docker:
::

    curl -sSL https://get.docker.com/ | sh

See `Developer <http://simprily.readthedocs.io/en/latest/develop.html#docker/>`_
documentation for more information on Docker.

a. Pull Docker image
====================

**Pull the latest SimPrily Docker image:**
::

    sudo docker pull agladstein/simprily

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

    sudo docker image ls

You should see something like this:
::

    REPOSITORY                      TAG                 IMAGE ID            CREATED             SIZE
    agladstein/simprily             latest              1d3fbe956b00        5 hours ago         938MB

b. Run SimPrily
===============

Run one small example with the Docker container
::

    sudo docker run -t -i --mount type=bind,source="$(pwd)",target=/app/tutorial agladstein/simprily python /app/simprily.py -p /app/tutorial/param_file_tutorial.txt -m /app/tutorial/model_file_tutorial.csv -i tutorial_1 -o /app/tutorial/output_dir -v

You should see something like this:
::

    debug-1: Debug on: Level 1
    JOB tutorial_1
    Current Seed: 19924
    debug-1: name   total   panel   genotyped
    debug-1: A      20      0       20
    debug-1: B      140     0       140
    debug-1: total samples: 160
    debug-1: Perform simulation and get sequences
    debug-1: Number of sites in simulation: 3071
    debug-1: Calculating summary statistics

    #########################
    ### PROGRAM COMPLETED ###
    #########################

Then, you should see a new directory created ``"$(pwd)"/output_dir``.
In that directory, you should see the directories
::

    sim_data
    germline_out
    results

and the directory ``results`` should have the file ``results_tutorial_1.txt``, which should look something like this:
::

    A       B       AN      AB_t    AN_t    SegS_A_CGI      Sing_A_CGI      Dupl_A_CGI      TajD_A_CGI      SegS_B_CGI      Sing_B_CGI     Dupl_B_CGI      TajD_B_CGI      FST_AB_CGI
    6803.19290799   5631.76173775   907706.772716   2253.4362688    1707.92117592   2490    500     193     0.648468498628  2210  37       2       2.26242085379   0.146122749866


**************************
4. Perform HTC simulations
**************************

a. Estimate the required resources
==================================

**Compare to provided benchmarking**
    First we should compare our model to the `benchmark <http://simprily.readthedocs.io/en/latest/tutorial_docker.html#benchmark/>`_.
    Our model is "simple", like Model 1, we have 160 diploid samples, and want to simulate 200Mb.
    So according to the benchmarking, we can expect our model to use approximately 1GB of memory and take about 5 min to run.

    1Gb is a reasonable amount of memory for most CPUs.

    50,000 simulations X 5 min / 60 per simulation = 4,167 hrs for all simulations.

**Profile the Simulation**
    After performing the test simulation and before starting high-throughput simulations,
    the memory use and run time of this model should be assessed.

- Edit model_file_tutorial.csv so it has the desired length of 200Mb. Change it to:

::

    -length,200000000,

- Run the simulation and time it with ``time``:

::

    time sudo docker run -t -i --mount type=bind,source="$(pwd)",target=/app/tutorial agladstein/simprily python /app/simprily.py -p /app/tutorial/param_file_tutorial.txt -m /app/tutorial/model_file_tutorial.csv -i tutorial_1 -o /app/tutorial/output_dir -v

We expect the simulation to take about 5 minutes, but the time depends on the parameters randomly chosen from the priors, so it could take less or more time.

- While that is running check ``top`` to see how much memory is being used.

::

    top


You should see something like this:
::

    top - 18:29:42 up  1:59,  3 users,  load average: 1.00, 0.63, 0.28
    Tasks: 142 total,   2 running, 140 sleeping,   0 stopped,   0 zombie
    %Cpu(s): 98.7 us,  1.3 sy,  0.0 ni,  0.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
    KiB Mem :  8175420 total,  5298016 free,   237632 used,  2639772 buff/cache
    KiB Swap:        0 total,        0 free,        0 used.  7599724 avail Mem

      PID USER      PR  NI    VIRT    RES    SHR S %CPU %MEM     TIME+ COMMAND
    20053 root      20   0   26492  16596   2988 R 97.3  0.2   4:35.89 macs
    20022 root      20   0  172476  34128  11044 S  2.3  0.4   0:07.51 python
    11488 root      20   0  442116  27524  13588 S  0.3  0.3   0:12.62 docker-containe
        1 root      20   0   37952   6128   4104 S  0.0  0.1   0:08.21 systemd
        2 root      20   0       0      0      0 S  0.0  0.0   0:00.00 kthreadd

In this case we see that Python is using about 170Mb of virtual memory.

b. Decide where to run your simulations
=======================================
Depending on how fast we want all the runs to finish, we pick the number of cores we want to run on.
In this case, since we expect it to only take about 4,000 hrs we could run this on the Open Science Grid or a smaller HPC, server, or cloud.

c. Run in parallel on large server
==================================
If we have a server with at least 100 cores, we could run the simulations in about 2 days with ``parallel``:
::

    seq 1 50000 | parallel -j 100 sudo docker run -t -i --mount type=bind,source="$(pwd)",target=/app/tutorial agladstein/simprily python /app/simprily.py -p /app/tutorial/param_file_tutorial.txt -m /app/tutorial/model_file_tutorial.csv -i tutorial_{} -o /app/tutorial/output_dir


d. Run as workflow on Open Science Grid
=======================================
Or we can use the `Pegasus workflow on the Open Science Grid <http://simprily.readthedocs.io/en/latest/htc.html#open-science-grid/>`_.

- Log onto Open Science Grid Connect

::

    ssh user-name@login01.osgconnect.net


- Clone the entire repository. *We only need the pegasus_workflow directory*

::

    git clone https://github.com/agladstein/SimPrily.git


- Go into the ``pegasus_workflow`` directory:

::

    cd SimPrily/pegasus_workfow

- Copy or create the model_file_tutorial.csv and param_file_tutorial.txt from above.

- Submit a small test workflow:

::

    ./submit -p param_file_tutorial.txt -m model_file_tutorial.csv -j 10

We should see something like:
::

    2018.06.25 11:02:08.849 CDT:   -----------------------------------------------------------------------
    2018.06.25 11:02:08.855 CDT:   File for submitting this DAG to HTCondor           : simprily-0.dag.condor.sub
    2018.06.25 11:02:08.860 CDT:   Log of DAGMan debugging messages                 : simprily-0.dag.dagman.out
    2018.06.25 11:02:08.865 CDT:   Log of HTCondor library output                     : simprily-0.dag.lib.out
    2018.06.25 11:02:08.870 CDT:   Log of HTCondor library error messages             : simprily-0.dag.lib.err
    2018.06.25 11:02:08.876 CDT:   Log of the life of condor_dagman itself          : simprily-0.dag.dagman.log
    2018.06.25 11:02:08.881 CDT:
    2018.06.25 11:02:08.886 CDT:   -no_submit given, not submitting DAG to HTCondor.  You can do this with:
    2018.06.25 11:02:08.897 CDT:   -----------------------------------------------------------------------
    2018.06.25 11:02:11.948 CDT:   Your database is compatible with Pegasus version: 4.8.0
    2018.06.25 11:02:12.078 CDT:   Submitting to condor simprily-0.dag.condor.sub
    2018.06.25 11:02:12.174 CDT:   Submitting job(s).
    2018.06.25 11:02:12.180 CDT:   1 job(s) submitted to cluster 19334.
    2018.06.25 11:02:12.185 CDT:
    2018.06.25 11:02:12.190 CDT:   Your workflow has been started and is running in the base directory:
    2018.06.25 11:02:12.196 CDT:
    2018.06.25 11:02:12.201 CDT:     /local-scratch/agladstein/workflows/simprily_1529942525/workflow/simprily_1529942525
    2018.06.25 11:02:12.206 CDT:
    2018.06.25 11:02:12.212 CDT:   *** To monitor the workflow you can run ***
    2018.06.25 11:02:12.217 CDT:
    2018.06.25 11:02:12.222 CDT:     pegasus-status -l /local-scratch/agladstein/workflows/simprily_1529942525/workflow/simprily_1529942525
    2018.06.25 11:02:12.227 CDT:
    2018.06.25 11:02:12.233 CDT:   *** To remove your workflow run ***
    2018.06.25 11:02:12.238 CDT:
    2018.06.25 11:02:12.243 CDT:     pegasus-remove /local-scratch/agladstein/workflows/simprily_1529942525/workflow/simprily_1529942525
    2018.06.25 11:02:12.248 CDT:
    2018.06.25 11:02:12.760 CDT:   Time taken to execute is 5.657 seconds

We can monitor the workflow by using the command given in the printed statement. In this case:
::

    pegasus-status -l /local-scratch/agladstein/workflows/simprily_1529942525/workflow/simprily_1529942525

Which outputs:
::

    STAT  IN_STATE  JOB
    Run      02:11  simprily-0 ( /local-scratch/agladstein/workflows/simprily_1529942525/workflow/simprily_1529942525 )
    Run      00:58   ┗━run-sim.sh_ID0000009
    Summary: 2 Condor jobs total (R:2)

    UNRDY READY   PRE  IN_Q  POST  DONE  FAIL %DONE STATE   DAGNAME
        4     0     0     1     0    12     0  70.6 Running *simprily-0.dag
    Summary: 1 DAG total (Running:1)

This means that the ``simprily`` workflow is running (in the directory shown),
and currently one simulation is running (the 9th simulation).
We see that 12 processes have completed and the entire workflow is 70.6% done.

The email that was used to create the OSG Connect account will receive an email when the workflow is complete.

In this case the results will be written to
``/local-scratch/agladstein/workflows/simprily_1529942525/outputs/``
::

    [agladstein@login01 pegasus_workfow]$ ls /local-scratch/agladstein/workflows/simprily_1529942525/outputs/
    final_results.txt

``final_results.txt`` contains the parameter values used to run the simulations and summary statistics calculated from the simulations
for all of the simulations from the workflow.
For example:
::

    [agladstein@login01 pegasus_workfow]$ head /local-scratch/agladstein/workflows/simprily_1529942525/outputs/final_results.txt
    A	B	AN	AB_t	AN_t	SegS_A_CGI	Sing_A_CGI	Dupl_A_CGI	TajD_A_CGI	SegS_B_CGI	Sing_B_CGI	Dupl_B_CGI	TajD_B_CGI	FST_AB_CGI
    5344.42290079	8823.11026958	23042.8392599	1621.37069753	3576.63582673	66	14	5	0.612131940133	76	11	2	2.36972132977	0.08462380112
    8626.21444024	4432.98604274	18027.9154874	3139.75475448	2737.45325718	69	24	9	-0.313129414676	41	22	2.80590304723	0.163579588626
    1204.0872668	2992.49797803	61262.9413354	2599.93721571	438.20762215	243	13	33	1.72441317331	201	00	3.24176945597	0.124526585551
    3696.12346086	5279.87024578	28842.820112	2699.2693586	3226.68324657	74	25	1	0.381684017383	95	63	1.33636580198	0.129678414366
    5456.92727156	4876.88978622	45379.0305936	1742.81453106	620.930047461	182	38	21	0.498313835616	196	25	6	0.762716222206	0.324577494188
    4506.50442054	7227.8502438	92238.4468821	2039.10543287	2451.45021427	208	31	2	1.43332513774	361	37	44	0.37981118879	0.294256698297
    6305.87444634	8167.64822508	96815.9966437	3923.83195464	2226.21980366	287	76	17	0.619786936616	284	72	2.60377068841	0.140691639063
    1559.12937959	4924.54508638	56393.1667057	2534.56840169	2250.6811166	55	2	1	3.13808514057	154	212	1.43704802413	0.107439420978
    3781.32638852	4356.79072056	33283.5573331	1325.91016803	531.570175129	95	18	18	0.21637274122	96	410	1.03611653739	0.0946289249489

- Once the previous test workflow completes, we can scale up incrementally.
Next run 100 jobs, then run 1000 jobs. If everything there are no errors,
we can run the full workflow of 50,000 jobs:

::

    ./submit -p param_file_tutorial.txt -m model_file_tutorial.csv -j 50000

Since we estimated it should take about 4000 CPU hrs to run,
we can expect the OSG to finish this full workflow in a day or less, depending on the OSG's current load.