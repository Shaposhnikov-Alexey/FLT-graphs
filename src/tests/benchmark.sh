#!/bin/bash

#DIRECTORY="/home/kob4/Desktop/FLT-graphs/src/data/.datasets/refinedDataForRPQ/"
DIRECTORY="/mnt/x/refinedDataForRPQ"
REGEXP_DIRECTORY="/mnt/x/refinedDataForRPQ/LUBM300/regexes/"
REGEXPS=(q_13_6 q_16_3 q1_7 q4_2_0 q4_5_4 q5_7 q8_9 q10_2_0 q11_2_3 q11_2_9)

DATASETS=(LUBM300 LUBM500 LUBM1M LUBM1.5M LUBM1.9M proteomes uniprotkb_archea_asgard_group_1935183_0)

export PYTHONPATH="${PYTHONPATH}:../../"

for dataset in ${DATASETS[*]}
do
  graph="$DIRECTORY/$dataset/$dataset.txt"
    output="benchmark/${dataset}_adjency.txt"
  for regex in ${REGEXPS[*]}
  do
    python3 ./../main/main.py "$graph" "${REGEXP_DIRECTORY}${regex}" >> "$output"
  done
done
