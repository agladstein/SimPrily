#########################
High Throughput Computing
#########################

*****************
Open Science Grid
*****************

1. Create an OSG Connect account. https://osgconnect.net/signup
2. Join the project SimPrily
3. Create an `ssh key pair <https://support.opensciencegrid.org/support/solutions/articles/12000027675-generate-ssh-key-pair-and-add-the-public-key-to-your-account>`_

Log onto Open Science Grid Connect
::

    ssh user-name@login01.osgconnect.net

Clone the entire repository. *We only need the pegasus_workflow directory*
::

 git clone https://github.com/agladstein/SimPrily.git



Test with interactive Singularity container
===========================================
Start the Singularity container and run a small test.
::

    [agladstein@login02 ~]$ singularity shell --home $PWD:/srv --pwd /srv /cvmfs/singularity.opensciencegrid.org/agladstein/simprily\:latest
    Singularity: Invoking an interactive shell within container...

    $ bash
    agladstein@login02:~$ export PATH=/usr/local/bin:/usr/bin:/bin
    agladstein@login02:~$ python /app/simprily.py examples/eg2/Param_file_eg2.txt examples/eg2/model_file_eg2.csv 2 out_dir


Submit a Pegasus workflow
=========================

All components of the Pegasus workflow are located in the directory
``pegasus_workflow``.

Start the workfow by running ``submit`` on the command line from the ``pegasus_workflow`` directory.
There are 3 required arguments and 2 optional arguments
::

    ./submit -p PARAM -m MODEL -j NUM [-g MAP] [-a ARRAY]


**Required**

-p PARAM  The location of the parameter file
-m MODEL  The location of the model file
-j NUM    The number of jobs to run. The ``ID`` will go from 1 to ``NUM``.

**Optional**

-g MAP    The location of the genetic map file
-a ARRAY  The location of the array template file, in bed form

*We recommend that all testing be done before submiting workflows to OSG. Therefore we do not include the verbose options. Pegasus provides run information, so we do not include the profile option with the OSG workflow.*

Example workflow submissions
----------------------------
e.g. (No pseudo array and no recombination map)
::

    ./submit -p ../examples/eg2/param_file_eg2.txt -m ../examples/eg2/model_file_eg2.csv -j 10

e.g. (include pseudo array, but no recombination map)
::

    ./submit -p ../examples/eg2/param_file_eg2_asc.txt -m ../examples/eg2/model_file_eg2_asc.csv -j 10 -a ../array_template/ill_650_test.bed

e.g. (recombination map, but no pseudo array)
::

    ./submit -p ../examples/eg2/param_file_eg2.txt -m ../examples/eg2/model_file_eg2.csv -j 10 -g ../genetic_map_b37/genetic_map_GRCh37_chr1.txt.macshs

e.g. (include pseudo array, and recombination map)
::

    ./submit -p ../examples/eg2/param_file_eg2_asc.txt -m ../examples/eg2/model_file_eg2_asc.csv -j 10 -a ../array_template/ill_650_test.bed -g ../genetic_map_b37/genetic_map_GRCh37_chr1.txt.macshs


Monitoring and Debugging
========================

To find the run times of the executable:
::

    pegasus-statistics -s all

Then, look at ``Transformation statistics``.


How the Pegasus workflow works
==============================

``submit`` -> ``tools/dax-generator`` -> ``wrappers/run-sim.sh``

``submit`` will run ``tools/dax-generator``, which constructs the workflow. The ``dax-generator`` is the main Pegasus file.
The ``dax-generator`` creates the HTCondor dag file.
It also tells Pegasus where the local files are and transfers files (from submit host to compute node) so they are available for the job.
It also defines how to handle output files.

``wrappers/run-sim.sh`` is the wrapper that runs in the container. It modifies the environment, and runs SimPrily.


***************************************
Recommendations for other HTC workflows
***************************************

*coming soon*