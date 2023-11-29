
# %% [markdown]
# # Tilable terrain gan
# 
# - DC GAN for now
# - pending tiling features

# %%
# CD to correct dir
%cd /home/jovyan/work/tf-docker-data//TesisCode/TerrainSGAN/

# %%
# Bringing in tensorflow
import tensorflow as tf
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus: 
    tf.config.experimental.set_memory_growth(gpu, True)

# %%
import rasterio
import glob
import numpy as np
import random

# Constants
BUFFER_SIZE = 10000
BATCH_SIZE = 32
IMAGE_SIZE = 28
MAX_ALTITUDE = 1105
MIN_ALTITUDE = -23

# 1. Read the GeoTIFF files
# file_list = glob.glob("TesisCode/TerrainSGAN/Dataset/download2/*.tif")
file_list = glob.glob("Dataset/download2/*.tif")
ds = tf.data.Dataset.from_tensor_slices(file_list)

# 2. Decode and preprocess the images
def decode_image(filename):
    with rasterio.open(filename.numpy().decode('utf-8')) as src:
        image = src.read()
        image = image[0]
        
    # Resize to desired image size using TensorFlow
    size_rows, size_cols = np.shape(image)
    # random 28x28 crop of np array image
    start_row = random.randint(0, size_rows - IMAGE_SIZE)
    start_col = random.randint(0, size_cols - IMAGE_SIZE)
    image = image[start_row:start_row+IMAGE_SIZE, start_col:start_col+IMAGE_SIZE]

    # Normalize the pixel values to [0,1]
    image = (image - MIN_ALTITUDE) / (MAX_ALTITUDE - MIN_ALTITUDE)
    
    # reshape to 28x28x1
    image = np.expand_dims(image, axis=-1)

    # Convert to float32
    image = tf.cast(image, tf.float32)

    return image

# Use tf.py_function to call the rasterio function in a tensorflow map function
def tf_decode_image(filename):
    return tf.py_function(decode_image, [filename], tf.float32)

ds = ds.map(tf_decode_image, num_parallel_calls=tf.data.experimental.AUTOTUNE)

ds = ds.cache()

# Use repeat() to loop over the dataset indefinitely
ds = ds.repeat()

# Shuffle and batch the dataset as before
ds = ds.shuffle(BUFFER_SIZE).batch(BATCH_SIZE).prefetch(tf.data.experimental.AUTOTUNE)


# %% [markdown]
# ##  2. Viz data and build dataset

# %%
# do data transformation
import numpy as np

# %%
# setup connection aka iterator
dataiterator = ds.as_numpy_iterator()



# %% [markdown]
# # 4. Construct training loop

# %% [markdown]
# # 4.1 Setup losses and optimizers
# from TesisCode.TerrainSGAN.TerrainTileSGan import terrainTileGan, generator, discriminator
import sys
# sys.path.append("/home/jovyan/work/tf-docker-data//TesisCode/TerrainSGAN/")
from TerrainTileSGan import terrainTileGan, generator, discriminator

# %% [markdown]
# ## 4.3 Build callback

# %%
import os
from tensorflow.keras.preprocessing.image import array_to_img
from tensorflow.keras.callbacks import Callback

# %%
class ModelMonitor(Callback):
    def __init__(self, num_img=3, latent_dim=128):
        self.num_img = num_img
        self.latent_dim = latent_dim

    def on_epoch_end(self, epoch, logs=None):
        random_latent_vectors = tf.random.uniform((self.num_img, self.latent_dim,1))
        generated_images = self.model.generator(random_latent_vectors)
        generated_images *= 255
        generated_images.numpy()
        for i in range(self.num_img):
            img = array_to_img(generated_images[i])
            img.save(os.path.join('images', f'generated_img_{epoch}_{i}.png'))
            tf.summary.image(f'generated_img_{epoch}_{i}', generated_images[i], step=epoch)

# %% [markdown]
# ## Train

# %%
## Setup tensorboard

from tensorflow.keras.callbacks import TensorBoard
from time import time

tensorboard = TensorBoard(log_dir="logs/{}".format(time()), histogram_freq=1, write_graph=True, write_images=True)

# %%
import threading
import subprocess

## CHeck if there are any .h5 files in the directory
# if len(os.listdir()) > 0:
#     # If there are, load the latest one
#     latest_gen = max(glob.glob('gen*.h5'))
#     latest_disc = max(glob.glob('disc*.h5'))
#     generator.load_weights(latest_gen)
#     discriminator.load_weights(latest_disc)

def save_weights(iteration):
    generator.save(f'gen{iteration}.h5')
    discriminator.save(f'disc{iteration}.h5')

def run_tensorboard():
    subprocess.call(['tensorboard', '--logdir', 'logs'])

# tb_thread = threading.Thread(target=run_tensorboard)
# tb_thread.start()


# %%
## generator.load_weights('generator.h5')
## discriminator.load_weights('discriminator.h5')

steps_per_epoch = 200 # 11 seconds per epoch
epochs = 120 


hist = terrainTileGan.fit(ds, epochs=epochs, steps_per_epoch=steps_per_epoch, callbacks=[ModelMonitor(), tensorboard])
# hist = terrainTileGan.fit(ds, epochs=epochs, steps_per_epoch=steps_per_epoch)

# %% [markdown]
# ### 5.2 Save the model

# %%
# Create timestamp for filename
from datetime import datetime
timestamp = datetime.now().isoformat().replace(':', '_').replace('.', '_')
generator.save(f'generator_{timestamp}.keras')
discriminator.save(f'discriminator_{timestamp}.keras')

# %%
