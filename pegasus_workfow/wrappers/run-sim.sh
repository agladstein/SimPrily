#!/bin/bash

set -e
set -v

JOB_ID=$1
PARAM_FILE=$2
MODEL_FILE=$3

#export PYTHONPATH=/app
export PATH=/usr/local/bin:/usr/bin:/bin
ln -s /app/bin bin
touch outputs-$JOB_ID.tar.gz

CMD="python /app/simprily.py $PARAM_FILE $MODEL_FILE $JOB_ID ."
echo
echo "Running: $CMD"
$CMD

# output files need unique names in the top level dir
tar czf outputs-$JOB_ID.tar.gz results_*

