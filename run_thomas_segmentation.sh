#!/bin/bash

#SBATCH --qos bbdefault
#SBATCH --time 120
#SBATCH --nodes 1
#SBATCH --ntasks 10
#SBATCH --mem 48G
#SBATCH --constraint icelake

set -e

# Define input and output directories
rds_root="/rds/projects/j/jenseno-avtemporal-attention/Projects/subcortical-structures"
input_dir="${rds_root}/load/MRI-data/Processed_Data/S01.anat"
output_dir="${rds_root}/attention-striatum-7T/results"
apptainer_dir="${rds_root}/attention-striatum-7T"

# Run the Apptainer command
apptainer run \
    -B "${input_dir}:${input_dir}" \
    -B "${output_dir}:${output_dir}" \
    -B "${apptainer_dir}:${apptainer_dir}" \
    -W "${input_dir}}" \
    -u --cleanenv "${apptainer_dir}/hipsthomas.sif" bash -c \
    "hipsthomas_csh \
    -i T1.nii.gz \
    -t1 -big > ${output_dir}/THOMAS.log 2>&1"
