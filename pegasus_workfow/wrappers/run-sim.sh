#!/bin/bash

set -euo pipefail

JOB_ID=$1
PARAM_FILE=$2
MODEL_FILE=$3
ARRAY_FILE=$4
REC_MAP=$5

#export PYTHONPATH=/app
export PATH=/usr/local/bin:/usr/bin:/bin
ln -s /app/bin bin
touch results_${JOB_ID}.txt

if [ -n "$REC_MAP" -a -n "$ARRAY_FILE" ]; then
  echo 1
  CMD="python /app/simprily.py -p $PARAM_FILE -m $MODEL_FILE -i $JOB_ID -o . -g $REC_MAP -a $ARRAY_FILE"
elif [ -n "$REC_MAP" -a -z "$ARRAY_FILE" ]; then
  echo 2
  CMD="python /app/simprily.py -p $PARAM_FILE -m $MODEL_FILE -i $JOB_ID -o . -g $REC_MAP"
elif [ -z "$REC_MAP" -a -n "$ARRAY_FILE" ]; then
  echo 3
  CMD="python /app/simprily.py -p $PARAM_FILE -m $MODEL_FILE -i $JOB_ID -o . -a $ARRAY_FILE"
else
  echo 4
  CMD="python /app/simprily.py -p $PARAM_FILE -m $MODEL_FILE -i $JOB_ID -o ."
fi

echo
echo "Running: $CMD"
$CMD

# output files need unique names in the top level dir
#tar czf outputs-$JOB_ID.tar.gz results
mv results/results_${JOB_ID}.txt .
