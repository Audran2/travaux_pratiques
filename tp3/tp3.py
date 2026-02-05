import numpy as np
from keras import layers, Input, models
from tensorflow.keras.datasets import mnist

(x_train, _), (x_test, _) = mnist.load_data()
x_train = x_train.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0

x_train = np.expand_dims(x_train, -1)
x_test = np.expand_dims(x_test, -1)

def add_noise(images, noise_factor=0.5):
    noisy_images = images + noise_factor * np.random.randn(*images.shape)
    return np.clip(noisy_images, 0., 1.)

noise_factor_test = 0.2
x_train_noisy = add_noise(x_train, noise_factor_test)
x_test_noisy = add_noise(x_test, noise_factor_test)

def autoencoder():
    # Encoder
    encoder_input = Input(shape=(28, 28, 1))
    x = layers.Conv2D(32, 3, activation="relu", padding='same')(encoder_input)
    x = layers.MaxPooling2D((2, 2), padding='same')(x)
    x = layers.Conv2D(16, 3, activation="relu", padding='same')(x)
    encoded = layers.MaxPooling2D((2, 2), padding='same')(x)

    # Decodeur
    x = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(encoded)
    x = layers.UpSampling2D((2, 2))(x)
    x = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(x)
    x = layers.UpSampling2D((2, 2))(x)
    decoder_output = layers.Conv2D(1, (3, 3), activation='sigmoid', padding='same')(x)

    autoencoder = models.Model(encoder_input, decoder_output)
    return autoencoder

autoencoder = autoencoder()
autoencoder.compile(optimizer='adam', loss='binary_crossentropy', metrics=['mae'])

history = autoencoder.fit(
    x_train_noisy, x_train,
    epochs=50,
    batch_size=100,
    validation_data=(x_test_noisy, x_test),
    shuffle=True
)

autoencoder.save("autoencoder_mnist_denoiser_classic.keras")