This directory contains the PBS scripts for the University of Arizona Ocelote HPC for profiling examples.

Submit pbs jobs from `/home/u15/agladstein/SimPrily`
```
qsub profiling_input/HPC_run/profile_parallel_ocelote_3_1.pbs
qsub profiling_input/HPC_run/profile_parallel_ocelote_3_2.pbs
qsub profiling_input/HPC_run/profile_parallel_ocelote_3_3.pbs
qsub profiling_input/HPC_run/profile_parallel_ocelote_3_4.pbs
qsub profiling_input/HPC_run/profile_parallel_ocelote_3_5.pbs
qsub profiling_input/HPC_run/profile_parallel_ocelote_3_6.pbs
qsub profiling_input/HPC_run/profile_parallel_ocelote_4_1.pbs
qsub profiling_input/HPC_run/profile_parallel_ocelote_4_2.pbs
qsub profiling_input/HPC_run/profile_parallel_ocelote_4_3.pbs
qsub profiling_input/HPC_run/profile_parallel_ocelote_4_4.pbs
qsub profiling_input/HPC_run/profile_parallel_ocelote_4_5.pbs
qsub profiling_input/HPC_run/profile_parallel_ocelote_4_6.pbs
```

output goes to `/rsgrps/mfh4/Ariella/SimPrily_profiling`

Check profiling job status
```
for i in {1..6}; do grep -l "COMPLETE" profile*_*_4_${i}_*.log | wc -l; done

./count_profile_jobs.sh /rsgrps/mfh4/Ariella/SimPrily_profiling
```

Combine profiling results
```
for i in {1..6}; do grep -l "COMPLETE" profile*_*_4_${i}_*.log | xargs cat >>profile_4_${i}.log;  done
for i in {1..6}; do rm profile*_*_4_${i}_*.log; done

grep -l "COMPLETE" profile*_*_3_1_*.log | xargs cat >>profile_3_1.log
grep -l "COMPLETE" profile*_*_3_2_*.log | xargs cat >>profile_3_2.log
grep -l "COMPLETE" profile*_*_3_3_*.log | xargs cat >>profile_3_3.log
grep -l "COMPLETE" profile*_*_3_4_*.log | xargs cat >>profile_3_4.log
grep -l "COMPLETE" profile*_*_3_5_*.log | xargs cat >>profile_3_5.log

for i in {1..6}; do cat profile_4_${i}.log >>profile_eg4.log; done
for i in {1..6}; do cat profile_3_${i}.log >>profile_eg3.log; done
```

