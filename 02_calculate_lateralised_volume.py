"""
===============================================
03. calculate_lateralised_volume

This code reads the volume of thalamus segments
(output of run_thomas_segmentation.sh) and 
calculates lateralised index.


written by Tara Ghafari
==============================================
"""

import numpy as np
import os.path as op
import pandas as pd
import matplotlib.pyplot as plt

# Function to read nuclei volumes from a file
def read_nuclei_volumes(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
    nuclei_volumes = {}
    for line in lines:
        parts = line.split()
        nuclei_volumes[parts[0]] = int(float(parts[1]))
    return nuclei_volumes

# Function to calculate lateralisation volume
def calculate_lateralisation_volume(vol_right, vol_left):
    return (vol_right - vol_left) / (vol_right + vol_left)

platform = 'mac'

# Define where to read and write the data
if platform == 'bluebear':
    jenseno_dir = '/rds/projects/j/jenseno-avtemporal-attention/Projects'
elif platform == 'mac':
    jenseno_dir = '/Volumes/jenseno-avtemporal-attention/Projects'

# Define where to read and write the data
mri_deriv_dir = op.join(jenseno_dir ,'subcortical-structures/SubStr-and-behavioral-bias/derivatives/MRI_lateralisations')
subStr_segmented_dir = op.join(mri_deriv_dir, 'substr_segmented')
output_dir = op.join(mri_deriv_dir, 'thalamus_lateralisation_indices')
vol_output_fname = op.join(output_dir, 'all_subs_thalamus_volumes_5.csv')
lat_output_fname = op.join(output_dir,'thal_lateralisation_volumes_5.csv')

# list of subjects folders
num_sub_list = range(1,5)

# Initialize lists to store lateralisation volumes for all participants
lateralisation_volumes = {structure: [] for structure in ['1-THALAMUS', '2-AV', '4-VA', '5-VLa', '6-VLP', 
                                                          '7-VPL', '8-Pul', '9-LGN', '10-MGN', '11-CM', '12-MD-Pf', 
                                                          '13-Hb', '14-MTT']}

data_vol = []
all_subject_substr_volume_table = np.full((6, 15), np.nan)
sub_IDs =[]
structures = ['1-THALAMUS', '2-AV', '4-VA', '5-VLa', '6-VLP', '7-VPL', '8-Pul', '9-LGN', '10-MGN', '11-CM', '12-MD-Pf', '13-Hb', '14-MTT']

# Read good subjects 
for num_sub in num_sub_list:
   
    substr_dir = op.join(subStr_segmented_dir, 'S' + str(1000+num_sub) + '.SubVol')
    if op.exists(substr_dir):
        sub_code = str(1000+num_sub)
        sub_IDs.append(sub_code)
        left_filepath = op.join(substr_dir, 'left/nucleiVols.txt')
        right_filepath = op.join(substr_dir, 'right/nucleiVols.txt')
        left_volumes = read_nuclei_volumes(left_filepath)
        right_volumes = read_nuclei_volumes(right_filepath)

        # Create a dictionary to store the volumes for the current participant
        participant_data = {'Participant': sub_code}
        
        # Add left volumes to participant_data
        for structure, volume in left_volumes.items():
            participant_data[f'{structure}_left'] = volume
        
        # Add right volumes to participant_data
        for structure, volume in right_volumes.items():
            participant_data[f'{structure}_right'] = volume
        
        data_vol.append(participant_data)


        # Calculate lateralisation volumes for each structure
        for structure in left_volumes.keys():
            vol_left = left_volumes[structure]
            vol_right = right_volumes[structure]
            lateralisation_vol = calculate_lateralisation_volume(vol_right, vol_left)
            lateralisation_volumes[structure].append(lateralisation_vol)

# Create a DataFrame from to store volumes
df_vol = pd.DataFrame(data_vol)

# Reorder columns to have 'Participant' as the first column
columns_vol = ['Participant'] + [col for col in df_vol.columns if col != 'Participant']
df_vol = df_vol[columns_vol]
df_vol.to_csv(vol_output_fname)

# Create a DataFrame to store lateralisation volumes
df_lat = pd.DataFrame(lateralisation_volumes)
df_lat.index = sub_IDs
df_lat.to_csv(lat_output_fname)

# Plot histogram of lateralisation volumes
df_lat.hist(figsize=(12, 8))
plt.suptitle('Histogram of Lateralisation Volumes', fontsize=16)
plt.xlabel('Lateralisation Volume')
plt.ylabel('Frequency')
plt.show()

# Plot scatter plots
for structure in structures:
    plt.figure(figsize=(8, 6))
    plt.scatter(df_vol[f'{structure}_right'], df_vol[f'{structure}_left'])
    plt.title(f'Scatter Plot of {structure} Right vs Left Volume')
    plt.xlabel(f'{structure} Right Volume')
    plt.ylabel(f'{structure} Left Volume')
    plt.show()

    if structure != 'THALAMUS':
        plt.figure(figsize=(8, 6))
        plt.scatter(df_vol['1-THALAMUS_right'] + df_vol['1-THALAMUS_left'], df_vol[f'{structure}_right'] + df_vol[f'{structure}_left'])
        plt.title(f'Scatter Plot of {structure} Total Volume vs Thalamus Total Volume')
        plt.xlabel('Thalamus Total Volume')
        plt.ylabel(f'{structure} Total Volume')
        plt.show()


        for idx, label in enumerate(labels):
            volume_label = 'volume' + str(label) + '.txt'
            substr_vol_fname = op.join(substr_dir, volume_label)
            if op.exists(substr_vol_fname):
                print(f"reading structure {structures[idx]} in subject #S100 {str(num_sub)}")
                # Read the text file
                with open(substr_vol_fname, "r") as file:
                    line = file.readline()
                substr_volume_array = np.fromstring(line.strip(), sep=' ')[1]     
            else:
                print(f"no volume for substructure {structures[idx]} found for subject #S100 {str(num_sub)}")
                substr_volume_array = np.nan  
            
            # Store the volume of each substr in one columne and data of each subject in one row  
            all_subject_substr_volume_table[i, idx] = substr_volume_array
    else:
        print('no substructures segmented by fsl for subject #S100' + str(num_sub))
        all_subject_substr_volume_table[i, :] = np.nan 
    
    
    
 
# Create a dataframe for all the data
columns = ['SubID'] + structures
df = pd.DataFrame(np.hstack((np.array(sub_IDs).reshape(-1, 1), all_subject_substr_volume_table)),
                  columns=columns)
df.set_index('SubID', inplace=True)

# Save 
df.to_csv(output_fname)   