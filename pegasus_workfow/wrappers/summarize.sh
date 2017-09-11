#!/bin/bash

set -e

TARBALL=$1
OUT_RESULTS_SIMS=results_sims.txt
OUT_SIM_VALUES=sim_values.txt

tar xzf $TARBALL

echo "sim" >tmp1
head -1 `ls results_sims_*/*.summary | head -n 1` >tmp2
paste tmp1 tmp2 >$OUT_RESULTS_SIMS
rm tmp1; rm tmp2

for f in results_sims_*/*; do
  tail -1 $f >>stats
done

for f in results_sims_*/*; do
  echo $f >>name
done

paste name stats >>$OUT_RESULTS_SIMS
rm stats; rm name



echo "sim" >tmp1
head -1 `ls sim_values_*/*_values.txt | head -n 1` >tmp2
paste tmp1 tmp2 >$OUT_SIM_VALUES
rm tmp1; rm tmp2

for f in sim_values_*/*; do
    tail -1 $f >>stats
done

for f in sim_values_*/*; do
    echo $f >>name
done

paste name stats >>$OUT_SIM_VALUES
rm stats; rm name
