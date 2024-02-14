#!/bin/bash

#SBATCH --account jenseno-avtemporal-attention
#SBATCH --qos bbdefault
#SBATCH --time 120
#SBATCH --nodes 1  # ensure the job runs on a single node
#SBATCH --ntasks 10  # this will give you circa 40G RAM and will ensure faster conversion to the .sif format
#SBATCH --mem 48G
#SBATCH --constraint icelake

# This code segments thalamus running hipsthomas in singularity container
# input_dir is where you read the T1w file
# output_dir is where you'd save the output
# singularity_dir is where you saved the hipsthomas container

# Define input and output directories
input_dir="/rds/projects/q/quinna-camcan/cc700/mri/pipeline/release004/BIDS_20190411/anat/sub-CC110037/anat"
output_dir="/rds/projects/j/jenseno-avtemporal-attention/Projects/subcortical-structures/attention-striatum-7T/results"
singularity_dir="/rds/projects/j/jenseno-avtemporal-attention/Projects/subcortical-structures/attention-striatum-7T" 

set -e

# Run the Singularity command
singularity run \
    -B "${input_dir}:${input_dir}" \
    -B "${output_dir}:${output_dir}" \
    -W "${input_dir}" \
    -u --cleanenv "${singularity_dir}/hipsthomas.sif" bash -c \
    "hipsthomas_csh \
    -i ${input_dir}/sub-CC110037_T1w.nii.gz \
    -t1 -big > ${output_dir}/THOMAS.log"