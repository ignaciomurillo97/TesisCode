# %%
# Bring in the sequential api for the generator and discriminator
from tensorflow.keras.models import Sequential
# Bring in the layers for the neural network
from tensorflow.keras.layers import Conv2D, LeakyReLU, Dropout, BatchNormalization
from tensorflow.keras.layers import Lambda, BatchNormalization

# %%

def build_discriminator():
    model = Sequential()

    # Normalize input
    # model.add(BatchNormalization(input_shape=(28, 28, 1)))

    # first conv block
    model.add(Conv2D(64, 5, input_shape=(28, 28, 1)))
    model.add(LeakyReLU(0.2))
    model.add(Dropout(0.4))

    # Second conv block
    model.add(Conv2D(64, 5))
    model.add(LeakyReLU(0.2))
    model.add(Dropout(0.4))

    # third conv block
    model.add(Conv2D(64, 5))
    model.add(LeakyReLU(0.2))
    model.add(Dropout(0.4))

    # fourth conv block
    model.add(Conv2D(64, 5))
    model.add(LeakyReLU(0.2))
    model.add(Dropout(0.4))

    # fifth conv block
    model.add(Conv2D(64, 5, activation='sigmoid'))
    return model

# %%
discriminator = build_discriminator()

# %%
