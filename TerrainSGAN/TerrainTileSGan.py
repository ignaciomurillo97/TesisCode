# %%

import tensorflow as tf
# Optimizer for both
from tensorflow.keras.optimizers import Adam
# Loss for both
from tensorflow.keras.losses import BinaryCrossentropy

# from TesisCode.TerrainSGAN.Discriminator import discriminator
# from TesisCode.TerrainSGAN.Generator import generator

from Discriminator import discriminator
from Generator import generator

# %%
g_opt = Adam(learning_rate=0.0001)
d_opt = Adam(learning_rate=0.00001)

g_loss = BinaryCrossentropy()
d_loss = BinaryCrossentropy()

# %% [markdown]
# # 4.2 Subclass model

# %%
# Import base model class to subclass our training step
from tensorflow.keras.models import Model

# %%
# 3 key functions

class TerrainTileGan(Model):
    def __init__(self, generator, discriminator, *args, **kwargs):
        # Pass to base class
        super().__init__(*args, **kwargs)
        
        # Create attributes for gen end disc
        self.generator = generator
        self.discriminator = discriminator

    def compile(self, g_opt, d_opt, g_loss, d_loss, *args, **kwargs):
        ## Compile w/ baseclass
        super().compile(*args, **kwargs)

        # Attributes for losses and optimizers
        self.g_opt = g_opt
        self.d_opt = d_opt
        self.g_loss = g_loss
        self.d_loss = d_loss

    def train_step(self, batch):
        # get the data
        real_images = batch
        # 128 because we start with a linear layer w/ 128 neurons. Gets reshaped lated
        fake_images = self.generator(tf.random.normal((128, 128, 1)), training = False)

        # Train discriminator
        with tf.GradientTape() as d_tape:
            # 1. pass real and fake imgs to discriminaotr
            yhat_real = self.discriminator(real_images, training=True)
            yhat_fake = self.discriminator(fake_images, training=True)
            yhat_realfake = tf.concat([yhat_real, yhat_fake], axis=0)
            
            # 2. cresate labels for real and fakes
            y_realfake = tf.concat([tf.zeros_like(yhat_real), tf.ones_like(yhat_fake)], axis=0)

            # 3. add noise to output to avoid learning too fast
            noise_real = 0.15*tf.random.uniform(tf.shape(yhat_real))
            noise_fake = 0.15*tf.random.uniform(tf.shape(yhat_fake))
            y_realfake += tf.concat([noise_real, noise_fake], axis=0)

            # 4. Calculate loss - BINARYCROSSENTROPY
            total_d_loss = self.d_loss(y_realfake, yhat_realfake)

        # 5. Backpropagate -- nn learn
        dgrad = d_tape.gradient(total_d_loss, self.discriminator.trainable_variables)
        self.d_opt.apply_gradients(zip(dgrad, self.discriminator.trainable_variables))

        # Train gen
        with tf.GradientTape() as g_tape:
            # Generate new images
            gen_images = self.generator(tf.random.normal((128, 128, 1)), training=True)

            # Create predicted labels
            predicted_labels = self.discriminator(gen_images, training=False)

            # Calculate loss (rewared when disc says fake is real - hence zeros)
            total_g_loss = self.g_loss(tf.zeros_like(predicted_labels), predicted_labels)
            # No need to pass real images bc we're not training discriminator

        # Apply backprop
        ggrad = g_tape.gradient(total_g_loss, self.generator.trainable_variables)
        self.g_opt.apply_gradients(zip(ggrad, self.generator.trainable_variables))

        return {"d_loss":total_d_loss, "g_loss": total_g_loss}
            
    # Also option for train_test

# %%
## Alt
# @tf.function
# def train_step():
#     pass

# %%
# Create instance of subclassed model
terrainTileGan = TerrainTileGan(generator, discriminator)

# %%
# Compile model
terrainTileGan.compile(g_opt, d_opt, g_loss, d_loss)
# %%
