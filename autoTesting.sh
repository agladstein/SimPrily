#!/usr/bin/env bash
 total=0
 bad=0
 i=6
 while true;
 do
 	total=$((total+1))
 	~/simprily_env/bin/python simprily.py -p examples/eg${i}/param_file_eg${i}.txt -m examples/eg${i}/model_file_eg${i}.csv -g genetic_map_b37/genetic_map_GRCh37_chr1.txt.macshs -a array_template/ill_650_test.bed -i ${i} -o output_dir
 	result=$?
 	if [[ $result != 0 ]]; then
 		bad=$((bad+1))

 	else
 		echo "example $i has passed"
 	fi
 	percent=$(awk "BEGIN { pc=100-(100*${bad}/${total}); i=int(pc); print (pc-i<0.5)?i:i+1 }")
 	echo $percent
 done

for i in 6 1 3 4 7; 
do
	~/simprily_env/bin/python simprily.py -p examples/eg${i}/param_file_eg${i}.txt -m examples/eg${i}/model_file_eg${i}.csv -g genetic_map_b37/genetic_map_GRCh37_chr1.txt.macshs -a array_template/ill_650_test.bed -i ${i} -o output_dir > /dev/null
	result=$?
	if [[ $result != 0 ]]; then
		echo "example $i has failed" 
		exit 1
	fi
	echo "example $i has passed"
done