import numpy as np
import nibabel as nb

def split_atlas(atlas, output_dir):
    atlas_img = nb.load(atlas)
    atlas_array = atlas_img.get_fdata()
    n_regions = int(np.max(atlas_array))
    for region in range(1, n_regions + 1):
        atlas_array_copy = np.copy(atlas_array)
        atlas_array_copy[atlas_array_copy != region] = 0
        print(f"Region {region}: Max value = {np.max(atlas_array_copy)}")
        if np.max(atlas_array_copy) == 0:
            print("No Region Found. Skipping...")
        else:
            isolated_region_img = nb.Nifti1Image(atlas_array_copy, atlas_img.affine)
            nb.save(isolated_region_img, f"{output_dir}/region_{region}.nii.gz")

