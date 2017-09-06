# TO SET MINIMUM MATCH LENGTH; ADD "-min_m <length>" TO YOUR RUN.GLINE.SH OR RUN.SH CALL (WITH QUOTES)
MATCH=3

if [ $# -lt 4 ]; then
  echo -e "USAGE:\t$0\t[GERMLINE executable] [ped file] [map file] [output name] [optional parameters]"
  exit
fi

GERMLINE=$1
PED=$2
MAP=$3
OUT=$4

if [ ! -s $PED ]; then
  echo "$PED does not exist or is empty"
  exit
fi

if [ ! -s $MAP ]; then
  echo "$MAP does not exist or is empty"
  exit
fi

echo -e "1\trunning GERMLINE"
echo '1' > $OUT.run
echo $MAP >> $OUT.run
echo $PED >> $OUT.run
echo $OUT >> $OUT.run

echo 1 2 3 | $GERMLINE \
-bits 128 \
-err_hom 4 \
-err_het 1 \
-min_m $MATCH \
$5 < $OUT.run

rm $OUT.run 
