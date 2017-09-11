#!/bin/bash

set -e

JOB_ID=$1
PARAM_FILE=$2
MODEL_FILE=$3
ARRAY_FILE=$4
MAP_FILE=$5

export PYTHONPATH=/app

CMD="python /app/simprily.py $PARAM_FILE $MODEL_FILE macs 1 $ARRAY_FILE 0 True ."
echo
echo "Running: $CMD"
$CMD

# output files need unique names in the top level dir
tar czf outputs-$JOB_ID.tar.gz results_sims_* sim_values_*

