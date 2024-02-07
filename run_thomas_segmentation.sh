#!/bin/bash

#SBATCH --account bagshaap-eeg-fmri-hmm
#SBATCH --qos bbdefault
#SBATCH --time 120
#SBATCH --nodes 1  # ensure the job runs on a single node
#SBATCH --ntasks 10  # this will give you circa 40G RAM and will ensure faster conversion to the .sif format
#SBATCH --mem 48G
#SBATCH --constraint icelake

set -e

singularity run -B ${PWD}:${PWD} -W ${PWD} -u --cleanenv hipsthomas.sif bash -c "hipsthomas_csh -i sub-20240201c3e8_T1w.nii.gz -t1 -big" 
