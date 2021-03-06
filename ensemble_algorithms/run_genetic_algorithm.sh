#!/bin/bash

###
# $1 => name of dataset (e.g. edgar_10_12).
# $2 => results_suffix (e.g. 1).

# Usage examples:
# (venv)$ ./run_genetic_algorithm.sh edgar_10_12 1
# (venv)$ ./run_genetic_algorithm.sh edgar_10_12 2
# (venv)$ ./run_genetic_algorithm.sh edgar_10_12 3
###

########### Variables ###########
# Top most directory of project
top_dir=$(git rev-parse --show-toplevel)

# Data directory (where output of base.py is stored)
data_dir=${top_dir}"/PythonESN/data_backup/"

# Data set
data_set=$1

# Test Size
test_size=240

# Line number (both inclusive) of base.py output
# to process in genetic algorithm. GA will access
# up-to past 500 (default) lines before start_line
start_line=$(expr `cat ${data_dir}${data_set} | wc -l` - ${test_size} + 1) # +1 to include self
end_line=`cat ${data_dir}${data_set} | wc -l`

echo "Start Line: "${start_line}
echo "End Line: "${end_line}

# Directory path (relative to top_dir) for storing GA results
results_dir='/ensemble_algorithms/results/'$1'/'
logs_dir='/ensemble_algorithms/results/logs/'$1'/'

# File name prefix for storing GA results
results_prefix='Ensemble_GA_'

# File name suffix for multiple runs
results_suffix='_'$2

# Processors
cpus=$(cat /proc/cpuinfo | grep 'processor' | wc -l)

#################################

# Make sure results_dir exists
dir_path=${top_dir}${results_dir}
logs_path=${top_dir}${logs_dir}
mkdir -p ${dir_path}
mkdir -p ${logs_path}

# Output path
result_path=${dir_path}${results_prefix}${data_set}${results_suffix}

# Execute script
python3 -m scoop -n ${cpus} ensemble_genetic_algorithm.py \
    ${data_dir}${data_set} \
    ${start_line} \
    ${end_line} \
    ${result_path} \
    ${logs_path}${results_prefix}${data_set}${results_suffix}'.log'