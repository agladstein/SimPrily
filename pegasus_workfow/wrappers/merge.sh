#!/bin/bash

set -e

OUT_FILE=$1
shift

cat "$@" > $OUT_FILE


