#!/bin/bash

#SBATCH --account jenseno-avtemporal-attention
#SBATCH --qos bbdefault
#SBATCH --time 60
#SBATCH --nodes 1  # ensure the job runs on a single node
#SBATCH --ntasks 10  # this will give you circa 40G RAM and will ensure faster conversion to the .sif format
#SBATCH --mem 48G
#SBATCH --constraint icelake

# this code downloads thomaships docker using singularity 
# edit the IMAGE_PATH to where you'd like the docker to download to and run sbatch pull_hipsthomas.sh

set -e

IMAGE_PATH=/rds/projects/j/jenseno-avtemporal-attention/Projects/subcortical-structures/attention-striatum-7T/hipsthomas.sif

singularity pull --name ${IMAGE_PATH} docker://anagrammarian/thomasmerged
