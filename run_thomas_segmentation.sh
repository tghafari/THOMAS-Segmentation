#!/bin/bash

#SBATCH --qos bbdefault
#SBATCH --time 120
#SBATCH --nodes 1
#SBATCH --ntasks 10
#SBATCH --mem 48G
#SBATCH --constraint icelake

set -e

# Define input and output directories

# Define root rds folder
rds_root="/rds/projects/j/jenseno-avtemporal-attention/Projects/subcortical-structures"

# Directory containing the T1 image.
input_dir="${rds_root}/load/MRI-data/Processed_Data/S01.anat"

# Directory to save outputs.
output_dir="${rds_root}/attention-striatum-7T/results"

# Directory where hipsthomas container is saved.
apptainer_dir="${rds_root}/attention-striatum-7T"

# Change directory to where the T1 is saved.
cd ${input_dir}

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
