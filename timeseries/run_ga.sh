#!/bin/bash

########### Variables ###########
DATAFILE="/home/minh/PycharmProjects/Ensemble/PythonESN/data_backup/edgar"

# Both hours_start and hours_end are inclusive
HOURS_START=1
HOURS_END=2207

# Top most directory of project
top_dir=$(git rev-parse --show-toplevel)

# Directory path (relative to top_dir) for storing GA results
results_dir='/timeseries/'

# File name for storing GA results
results_file='GA_results'

#################################

# Make sure results_dir exists
dir_path=${top_dir}${results_dir}
mkdir -p ${dir_path}

# Output path
result_path=${dir_path}${results_file}

# Execute script
#unbuffer python3 -m scoop -n 4 evolve.py $DATAFILE $HOURS_ELAPSED 2>&1 | tee ${result_path}
python3 -m scoop -n 4 evolve.py $DATAFILE $HOURS_START $HOURS_END $result_path