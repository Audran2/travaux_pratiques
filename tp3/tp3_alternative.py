import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, Input, models
from tensorflow.keras.datasets import mnist
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint

# Data
(x_train, _), (x_test, _) = mnist.load_data()
x_train = x_train.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0
x_train = np.expand_dims(x_train, -1)
x_test = np.expand_dims(x_test, -1)

def add_noise(images, noise_factor=0.2):
    noisy = images + noise_factor * np.random.randn(*images.shape)
    return np.clip(noisy, 0., 1.)

# Train on multiple noise levels for robustness
noise_levels = [0.1, 0.2, 0.3]
x_train_noisy = np.concatenate([add_noise(x_train, n) for n in noise_levels], axis=0)
x_train_clean = np.concatenate([x_train for _ in noise_levels], axis=0)
x_test_noisy = add_noise(x_test, 0.2)

# U-Net lightweight
def unet(input_shape=(28,28,1)):
    inp = Input(input_shape)
    # Encoder
    c1 = layers.Conv2D(32,3,padding='same')(inp)
    c1 = layers.BatchNormalization()(c1)
    c1 = layers.LeakyReLU()(c1)
    p1 = layers.MaxPooling2D()(c1)

    c2 = layers.Conv2D(64,3,padding='same')(p1)
    c2 = layers.BatchNormalization()(c2)
    c2 = layers.LeakyReLU()(c2)
    p2 = layers.MaxPooling2D()(c2)

    # Bottleneck
    b = layers.Conv2D(128,3,padding='same')(p2)
    b = layers.BatchNormalization()(b)
    b = layers.LeakyReLU()(b)

    # Decoder
    u1 = layers.UpSampling2D()(b)
    u1 = layers.Concatenate()([u1, c2])
    c3 = layers.Conv2D(64,3,padding='same')(u1)
    c3 = layers.BatchNormalization()(c3)
    c3 = layers.LeakyReLU()(c3)

    u2 = layers.UpSampling2D()(c3)
    u2 = layers.Concatenate()([u2, c1])
    c4 = layers.Conv2D(32,3,padding='same')(u2)
    c4 = layers.BatchNormalization()(c4)
    c4 = layers.LeakyReLU()(c4)

    out = layers.Conv2D(1,3,activation='sigmoid',padding='same')(c4)
    return models.Model(inp, out)

model = unet()
model.summary()

# SSIM loss helper
def ssim_loss(y_true, y_pred):
    s = tf.image.ssim(y_true, y_pred, max_val=1.0)
    return 1.0 - tf.reduce_mean(s)

def combined_loss(y_true, y_pred):
    mse = tf.reduce_mean(tf.math.squared_difference(y_true, y_pred))
    return 0.5 * mse + 0.5 * ssim_loss(y_true, y_pred)

model.compile(optimizer=keras.optimizers.Adam(1e-3),
              loss=combined_loss,
              metrics=[keras.metrics.MeanAbsoluteError()])

callbacks = [
    EarlyStopping(patience=8, restore_best_weights=True),
    ReduceLROnPlateau(factor=0.5, patience=4),
    ModelCheckpoint("best_unet_mnist.h5", save_best_only=True)
]

history = model.fit(x_train_noisy, x_train_clean,
                    epochs=25, batch_size=256,
                    validation_data=(x_test_noisy, x_test),
                    callbacks=callbacks, shuffle=True)

model.save("unet_mnist_denoiser.keras")