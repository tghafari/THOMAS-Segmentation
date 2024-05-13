#!/bin/bash

#SBATCH --qos bbdefault
#SBATCH --time 120
#SBATCH --nodes 1
#SBATCH --ntasks 10
#SBATCH --mem 48G
#SBATCH --constraint icelake

set -e

# change the rds_root, input_dir and T1_fname according to your data
# then write this in bluebear gui: sbatch run_thomas_segmentation.sh

# Define root rds folder
rds_root="/rds/projects/j/jenseno-avtemporal-attention/Projects/subcortical-structures"

# Directory containing the T1 image.
input_dir="${rds_root}/SubStr-and-behavioral-bias/T1-scans"
t1_fnames=('S1021_20220923#C47E_nifti' 'S1022_20221102#C5F2_nifti' 'S1023_20240208#C3FA_nifti')
            # 'S1024_20230426#C399_nifti' 'S1025_20211029#C3B4_nifti' 'S1026_20240313#C469_nifti'
            # 'S1027_20240229#C472_nifti' 'S1028_20221202#C47B_nifti' 'S1029_20240229#C515_nifti' 
            # 'S1030_20220308#C3A1_nifti' 'S1031_20240215#C416_nifti' 'S1032_20240229#C472_nifti')

# Get the T1 image name for this array task
T1_fname="S1010_20211007#C4DF_nifti"
#T1_fname="${T1_fnames[$SLURM_ARRAY_TASK_ID]}"
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

