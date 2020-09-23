#!/bin/bash

DIRECTORY="/home/kob4/Desktop/FLT-graphs/src/data/.datasets/refinedDataForRPQ/"

DATASETS=(LUBM300 LUBM500 LUBM1M LUBM1.5M LUBM1.9M geospecies mappingbased_properties_en proteomes uniprotkb_archea_asgard_group_1935183_0)

export PYTHONPATH="${PYTHONPATH}:../../"

for dataset in ${DATASETS[*]}
do
  graph="$DIRECTORY/$dataset/$dataset.txt"
  regexp_folder="$DIRECTORY/$dataset/regexes/*"
  output="time/${dataset}_adjency.txt"
  for regex in $regexp_folder
  do
    python3 ./../main/main.py "$graph" "$regex" >> "$output"
  done
done
