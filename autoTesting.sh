#!/bin/bash


containsElement () {
    local -n arr=$2
    for i in "${arr[@]}";
    do
        if [ "$i" == "$1" ] ; then
            return 0
        fi
    done
    return 1
}

declare -a file_types=("" "_asc")
tests=("1" "3" "4" "6" "7")
PYTHON=$1
test=$2
END=1
if [[ $3 != "" ]]
then
    END=$3
fi

if [[ $test == "" ]]
then
    for i in 4 7 6 1 3;
    do
        for file_type in "${file_types[@]}"
        do
            ${PYTHON} simprily.py -p examples/eg${i}/param_file_eg${i}${file_type}.txt -m examples/eg${i}/model_file_eg${i}${file_type}.csv -g genetic_map_b37/genetic_map_GRCh37_chr1.txt.macshs -a array_template/ill_650_test.bed -i ${i} -o output_dir > /dev/null
            result=$?
            if [[ $result != 0 ]]; then
                echo "example $i$file_type has failed"
                exit 1
            fi
            echo "example $i$file_type has passed"
        done
    done
    exit
fi

containsElement $test tests
contains=$?
if [ $contains == 0 ]
then
    for file_type in "${file_types[@]}";
    do
        total=0
        bad=0

        for i in $(seq 1 $END);
        do
            echo example $test$file_type is currently running
            total=$((total+1))
            ${PYTHON} simprily.py -p examples/eg${test}/param_file_eg${test}${file_type}.txt -m examples/eg${test}/model_file_eg${test}${file_type}.csv -g genetic_map_b37/genetic_map_GRCh37_chr1.txt.macshs -a array_template/ill_650_test.bed -i ${test} -o output_dir
            result=$?
            if [[ $result != 0 ]]; then
                bad=$((bad+1))
            else
                echo "example $test$file_type has passed"
            fi
            percent=$(awk "BEGIN { pc=100-(100*${bad}/${total}); i=int(pc); print (pc-i<0.5)?i:i+1 }")
            echo "$percent% of tries has passed"
        done
    done
else
    echo "Example $test is not in the list of know tests."
    exit 1
fi