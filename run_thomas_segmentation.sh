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

# module purge
# module load bluebear
# module load FSL/6.0.5.1-foss-2021a

# Define input and output directories
rds_root="/rds/projects/j/jenseno-avtemporal-attention/Projects/subcortical-structures"
input_dir="${rds_root}/load/MRI-data/Processed_Data/S01.anat"
output_dir="${rds_root}/attention-striatum-7T/results"
singularity_dir="${rds_root}/attention-striatum-7T" 

set -e

# Run the Singularity command
singularity run \
    -B "${input_dir}:${input_dir}" \
    -B "${output_dir}:${output_dir}" \
    -W "${input_dir}" \
    -u --cleanenv "${singularity_dir}/hipsthomas.sif" bash -c \
    "hipsthomas_csh \
    -i "${input_dir}/T1.nii.gz" \
    -t1 -big > ${output_dir}/THOMAS.log"