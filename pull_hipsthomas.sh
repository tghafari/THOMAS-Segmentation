#!/bin/bash

#SBATCH --account bagshaap-eeg-fmri-hmm
#SBATCH --qos bbdefault
#SBATCH --time 60
#SBATCH --nodes 1  # ensure the job runs on a single node
#SBATCH --ntasks 10  # this will give you circa 40G RAM and will ensure faster conversion to the .sif format
#SBATCH --mem 48G
#SBATCH --constraint icelake

set -e

IMAGE_PATH=/rds/projects/b/bagshaap-hcp-thalamus/thomas_segmentation/hipsthomas.sif

singularity pull --name ${IMAGE_PATH} docker://anagrammarian/thomasmerged
