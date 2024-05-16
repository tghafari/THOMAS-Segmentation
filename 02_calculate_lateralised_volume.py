"""
===============================================
02. calculate_lateralised_volume

This code reads the volume of thalamus segments
(output of run_thomas_segmentation.sh).
saves the right and left volumes in one csv,
calculates lateralised index and saves in another
csv file.


written by Tara Ghafari
==============================================
"""

import numpy as np
import os.path as op
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon, norm

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
scatters = False  # do you want to plot the sanity scatter plots?

# Define where to read and write the data
if platform == 'bluebear':
    jenseno_dir = '/rds/projects/j/jenseno-avtemporal-attention/Projects'
elif platform == 'mac':
    jenseno_dir = '/Volumes/jenseno-avtemporal-attention/Projects'

# Define where to read and write the data
mri_deriv_dir = op.join(jenseno_dir ,'subcortical-structures/SubStr-and-behavioral-bias/derivatives/MRI_lateralisations')
subStr_segmented_dir = op.join(mri_deriv_dir, 'substr_segmented')
output_dir = op.join(mri_deriv_dir, 'lateralisation_indices')
vol_output_fname = op.join(output_dir, 'all_subs_thalamus_volumes_32.csv')
lat_output_fname = op.join(output_dir,'thal_lateralisation_volumes_32.csv')

# list of subjects folders
num_sub_list = range(1,33)

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

# Calculate Wilcoxon test p-values for each structure
p_values = {}
for structure in df_lat.columns:
    stat, p = wilcoxon(df_lat[structure] - 0)
    p_values[structure] = p

# Plot histogram of lateralisation volumes with p-values
fig, axes = plt.subplots(4, 4, figsize=(16, 16))
axes = axes.flatten()

for idx, structure in enumerate(df_lat.columns):
    ax = axes[idx]
    df_lat[structure].hist(ax=ax, bins=10, edgecolor='black', grid=False, density=True)
    # Plot normal density plot
    x = np.linspace(df_lat[structure].min(), df_lat[structure].max(), 100)
    p = norm.pdf(x, df_lat[structure].mean(), df_lat[structure].std())
    ax.plot(x, p, 'k', linewidth=2)
    # Add vertical line at 0
    ax.axvline(0, color='r', linestyle='--', linewidth=2)

    ax.set_title(f'{structure}')
    if idx > 8:
        ax.set_xlabel('Lateralisation Volume')
    ax.set_ylabel('Frequency')
    # Add p-value as text inside the plot
    textstr = f'p-value: {p_values[structure]:.4f}'
    # Place the text in the upper right corner of the plot
    ax.text(0.95, 0.95, textstr, transform=ax.transAxes, fontsize=12,
            verticalalignment='top', horizontalalignment='right', bbox=dict(facecolor='white', alpha=0.5))

# Hide any unused subplots
for i in range(len(df_lat.columns), len(axes)):
    fig.delaxes(axes[i])

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.suptitle('Histogram of Lateralisation Volumes with Wilcoxon Test p-values', fontsize=16)
plt.show()


if scatters:
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
