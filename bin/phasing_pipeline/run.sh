#!/bin/sh

# BEAGLE Heap Size
HEAP=1024

# --- SOFTWARE SOURCES --- #

# Full path to the pipeline
PIPE=`/home/agladstein/Jews/Khazaria/BeharPaper/Euro_MidEast_Jews_Caucasus_CentAsia/Phasing/ $0`
PED_TO_BGL="$PIPE/ped_to_bgl"
BGL_TO_PED="$PIPE/bgl_to_ped"
SEARCH="$PIPE/search"

# Full path to GERMLINE executable
GERMLINE="$PIPE/germline"
# Full path to BEAGLE 3.0.1 jar file
BEAGLE="$PIPE/beagle.jar"

# --- SOFTWARE SOURCES --- #

BOOL_T=1
BOOL_F=0

if [ $# -lt 3 ]; then
  echo -e "USAGE:\t$0\t[ped file] [map file] [output name]"
  exit
fi

function verify_file
{
  if [ ! -s $1 ]; then
    echo "ERROR: $1 does not exist or is empty"
    return $BOOL_F
  fi
  return $BOOL_T
}

verify_file $PED_TO_BGL
if [ $? == $BOOL_F ]; then exit; fi
verify_file $BGL_TO_PED
if [ $? == $BOOL_F ]; then exit; fi

PED=$1
MAP=$2
OUT=$3

verify_file $PED
if [ $? == $BOOL_F ]; then exit; fi
verify_file $MAP
if [ $? == $BOOL_F ]; then exit; fi

echo "Converting to BEAGLE"
$PED_TO_BGL \
$PED \
$MAP \
> $OUT.pre_phase.bgl

verify_file $OUT.pre_phase.bgl
if [ $? == $BOOL_F ]; then exit; fi

nr_ind=`cat $PED | wc -l`
if [ $nr_ind -lt 250 ]; then
  samples=20;
elif [ $nr_ind -lt 500 ]; then
  samples=10;
elif [ $nr_ind -lt 1000 ]; then
  samples=4;
elif [ $nr_ind -lt 2000 ]; then
  samples=2;
else
  samples=1;
fi

echo "Run BEAGLE"
java -Xmx${HEAP}m -jar $BEAGLE \
unphased=$OUT.pre_phase.bgl log=$OUT.bgl \
nsamples=$samples missing=0

verify_file $OUT.pre_phase.bgl.phased
if [ $? == $BOOL_F ]; then exit; fi

tail -n+2 $OUT.pre_phase.bgl.phased > $OUT.phased.bgl
rm $OUT.pre_phase.bgl.phased $OUT.pre_phase.bgl
if [ -s $OUT.pre_phase.bgl.gprobs ]; then
  cut -f 1 -d ' ' $OUT.pre_phase.bgl.gprobs | $SEARCH $MAP 2 > $OUT.phased.map
else
  cp $MAP $OUT.phased.map
fi

awk '{ print $1,$2,$3,$4,$5,$6; }' $PED > $OUT.fam
$BGL_TO_PED \
$OUT.phased.bgl \
$OUT.fam 0 \
> $OUT.phased.ped

verify_file $OUT.phased.ped
if [ $? == $BOOL_F ]; then exit; fi

rm $OUT.bgl.log $OUT.pre_phase.bgl.r2 $OUT.pre_phase.bgl.gprobs
rm $OUT.fam $OUT.phased.bgl

bash $PIPE/gline.sh $OUT.phased.ped $OUT.phased.map $OUT "$4"
