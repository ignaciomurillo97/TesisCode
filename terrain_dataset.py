# %%
import rasterio as rs
import numpy as np
from tensorflow.data.Dataset import from_tensor_slices
from os import listdir
from os.path import isfile, join

# %%
def GetDataset(geotiff_dir="./Dataset/download2/"):
    contents = listdir(geotiff_dir)

    array_set = False
    tiff_array = None

    for file in contents:
        filepath = join(geotiff_dir, file)
        if isfile(filepath):
            dataset = rs.open(filepath)
            data = dataset.read()
            cropped_data = data[:1,:28,:28]
            if not array_set:
                tiff_array = cropped_data
                array_set = True
            else:
                tiff_array = np.concatenate((tiff_array, cropped_data), axis=0)
    
    return from_tensor_slices(tiff_array)

