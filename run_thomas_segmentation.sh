#!/bin/bash

#SBATCH --qos bbdefault
#SBATCH --time 120
#SBATCH --nodes 1
#SBATCH --ntasks 10
#SBATCH --mem 48G
#SBATCH --constraint icelake
#SBATCH --array=0-11  # Run one task for each subject name

set -e

# change the rds_root, input_dir and T1_fname according to your data
# then cd to the directory where you save this script
# then write this in bluebear gui terminal: sbatch run_thomas_segmentation.sh
# After this finished running, you have to manually move the thalamus segments to sub.SubVol folder
# because the it can only save the segments in input_fname

# Define root rds folder
rds_root="/rds/projects/j/jenseno-avtemporal-attention/Projects/subcortical-structures"

# Directory containing the T1 image.
input_dir="${rds_root}/SubStr-and-behavioral-bias/T1-scans"

# Get the T1 image name for this array task
t1_fnames=('S1038_20240507#C5F7_nifti' 'S1041_20240422#C57E_nifti' 'S1039_20240621#C533_nifti'
'S1042_20240522#C64D_nifti' 'S1040_20240605#C546_nifti' 
'S1037_20230525#C4D0_nifti' 'S1036_20240503#C416_nifti' 
'S1035_20240411#C453_nifti' 'S1034_20240502#C423_nifti'
'S1033_20240503#C389_nifti' 'S1032_20240229#C472_nifti')
# 'S1045_20240618#C40C_nifti' 'S1044_20240624#C537_nifti' 'S1043_20240729#C388_nifti'


t1_fname="${t1_fnames[$SLURM_ARRAY_TASK_ID]}"  # if wanting to run on one subject, put the name of subject in t1_fname
input_fname="${input_dir}/${t1_fname}"

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

