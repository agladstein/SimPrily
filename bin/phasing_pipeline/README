INTRODUCTION
------------

This is a Bash script pipeline for phasing PLINK format genotype data and processing it through GERMLINE to detect IBD matches.

INSTALLATION
------------

The pipeline requires you to have the BEAGLE phasing and GERMLINE IBD software installed. You can download each here:

BEAGLE:		http://www.stat.auckland.ac.nz/~bbrowning/beagle/beagle.html
GERMLINE:	http://www1.cs.columbia.edu/~gusev/germline/

To install, compile the utility scripts by entering the phasing_pipeline directory and running `make all`.
Then update the sotware sources in the run.sh script by setting the PIPE, GERMLINE, and BEAGLE variables to point to their respective locations.
Optionally, set the HEAP variable for Beagle heap-size used by the Java runtime.

This pipeline has been tested with BEAGLE 3.0.1 and may not work with subsequent versions that change output format (v3.2 does not work).
It does not take advantage of BEAGLE's trio phasing abilities.

USAGE
-----

The pipeline takes as input an input .ped and .map file in PLINK format ( http://pngu.mgh.harvard.edu/~purcell/plink/data.shtml#ped )
as well as an output name to prefix all of the generated output with. You can run the pipeline as follows:

bash run.sh file.ped file.map out

To generate out.phased.ped out.phased.map out.match out.log files for the phased data, IBD output, and IBD logs respectively.

---

Optionally, you can pass additional parameters to GERMLINE as follows:

bash run.sh file.ped file.map out "-map genetic.map -min_m 10"

Which would phase and call GERMLINE with the genetic map and minimum match flags.
You can also bypass the phasing completely and run germline only using:

bash gline.sh GERMLINE_PATH file.ped file.map out
