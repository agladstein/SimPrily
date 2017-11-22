#!/bin/bash

# set -x
while getopts ":r:hp:m:g:a:z:y:w:x:" opt; do
  case $opt in
    r)
     runs=$OPTARG
      ;;
    p)
     parameter_file=$OPTARG
      ;;
    m)
     model_file=$OPTARG
      ;;
    g)
     geneticmap_file=$OPTARG
      ;;
    a)
     array_file=$OPTARG
      ;;
    z)
     parameter_outfile=$OPTARG
      ;;
    y)
     model_outfile=$OPTARG
      ;;
    w)
     geneticmap_outfile=$OPTARG
      ;;
    x)
     array_outfile=$OPTARG
      ;;
    h)
     usage
     exit 1
      ;;      
    \?)
     echo "Invalid option: -$OPTARG" >&2
     exit 1
      ;;
    :)
     echo "Option -$OPTARG requires an argument." >&2
     exit 1
      ;;
  esac
done

echo "# application/vnd.de.path-list+csv; version=1" > $parameter_outfile
echo "# application/vnd.de.path-list+csv; version=1" > $model_outfile
echo "# application/vnd.de.path-list+csv; version=1" > $geneticmap_outfile
echo "# application/vnd.de.path-list+csv; version=1" > $array_outfile

for i in $(seq 1 $runs); #This will run the for loop a user defined number of times
	do
		echo $parameter_file >> $parameter_outfile
    echo $model_file >> $model_outfile
    echo $geneticmap_file >> $geneticmap_outfile
    echo $array_file >> $array_outfile
	done
