#!/bin/bash

#SBATCH --qos bbdefault
#SBATCH --time 120
#SBATCH --nodes 1
#SBATCH --ntasks 10
#SBATCH --mem 48G
#SBATCH --constraint icelake

set -e

# change the rds_root, input_dir and T1_fname according to your data
# then cd to the directory where you save this script
# then write this in bluebear gui terminal: sbatch run_thomas_segmentation.sh

# Define root rds folder
rds_root="/rds/projects/j/jenseno-avtemporal-attention/Projects/subcortical-structures"

# Directory containing the T1 image.
input_dir="${rds_root}/SubStr-and-behavioral-bias/T1-scans"

# Get the T1 image name for this array task
T1_fname="S1032_20240229#C472_nifti"
input_fname="${input_dir}/${T1_fname}"

# Directory where hipsthomas container is saved.
apptainer_dir=${rds_root}

# Change directory to where the T1 is saved - THOMAS doesn't like to work from outside of the directory.
cd ${input_fname}

# Run the Apptainer command
apptainer run \
    -B "${input_fname}:${input_fname}" \
    -B "${apptainer_dir}:${apptainer_dir}" \
    -W "${input_fname}" \
    -u --cleanenv "${apptainer_dir}/hipsthomas.sif" bash -c \
    "hipsthomas_csh \
    -i T1_vol_v1_5.nii.gz \
    -t1 -big > ${input_fname}/THOMAS.log 2>&1"

