#!/usr/bin/env bash


containsElement () {
  local e match="$1"
  shift
  for e; do [[ "$e" == "$match" ]] && return 0; done
  return 1
}


 total=0
 bad=0
i=6
#if [ $1 != "a" ]; then echo hi; fi
#while true;
#do
#    total=$((total+1))
# 	~/simprily_env/bin/python simprily.py -p examples/eg${i}/param_file_eg${i}_asc.txt -m examples/eg${i}/model_file_eg${i}_asc.csv -g genetic_map_b37/genetic_map_GRCh37_chr1.txt.macshs -a array_template/ill_650_test.bed -i ${i} -o output_dir
# 	result=$?
# 	if [[ $result != 0 ]]; then
# 		bad=$((bad+1))
#
# 	else
# 		echo "example $i has passed"
# 	fi
# 	percent=$(awk "BEGIN { pc=100-(100*${bad}/${total}); i=int(pc); print (pc-i<0.5)?i:i+1 }")
# 	echo $percent
# done

declare -a arr=("" "_asc")
for i in 4 7 6 1 3;
do
    for file_type in "${arr[@]}"
    do
        ~/simprily_env/bin/python simprily.py -p examples/eg${i}/param_file_eg${i}${file_type}.txt -m examples/eg${i}/model_file_eg${i}${file_type}.csv -g genetic_map_b37/genetic_map_GRCh37_chr1.txt.macshs -a array_template/ill_650_test.bed -i ${i} -o output_dir > /dev/null
        result=$?
        if [[ $result != 0 ]]; then
            echo "example $i$file_type has failed"
            exit 1
        fi
        echo "example $i$file_type has passed"
    done
done