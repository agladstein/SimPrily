#!/bin/bash

set -e

OUT_FILE=$1
shift

for FILE in "$@"; do
    echo "Untarring $FILE"
    tar xzf $FILE
done

echo "Creating merged tarball $OUT_FILE"
tar czf $OUT_FILE results_sims_* sim_values_*


