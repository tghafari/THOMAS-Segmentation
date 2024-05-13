# THOMAS-Segmentation

A repo to collaborate on thalamus segmentation using 
[THOMAS algorithm](https://github.com/thalamicseg/hipsthomasdocker)

0. Navigate to the directory containing the bash scripts
1. Pull the docker by running pull_hipsthomas.sh 
2. Once you have the container downloaded, open run_thomas_segmentation
3. Navigate to the directory of your T1, container, and output
3. Segment Thalamus by running run_thomas_segmentation.sh
4. Visualise the segmentation usign fsleye
5. run 02_calculate_lateralised_volume.py for laterlity volumes and scatter plots
