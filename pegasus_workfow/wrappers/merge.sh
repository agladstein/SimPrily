#!/bin/bash

set -e

OUT_FILE=$1
shift

head -1 "$1" > $OUT_FILE

for f in "$@"
do
    tail -n +2 $f >> $OUT_FILE
done


