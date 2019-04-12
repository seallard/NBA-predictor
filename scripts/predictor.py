# This script creates and trains the network.

import pandas as pd
from time import time
from sklearn.preprocessing import MinMaxScaler

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import Adam
from keras.callbacks import TensorBoard
from keras.callbacks import TensorBoard, ModelCheckpoint

scaler = MinMaxScaler()

# Load training dataset.
df = pd.read_csv("../data sets/training_2017_18.csv")

# Select 650 first games, columns 2:-2 as patterns.
x_train = df.values[:650, :-1]

# Normalize training data.
x_train_normalized = scaler.fit_transform(x_train)

# Select outcomes of 650 first games as targets.
y_train = df.values[:650, -1]

# Load validation data set.
validation_df = pd.read_csv("../data sets/validation_2017_18.csv")

# Select validation inputs and normalize.
x_validation = validation_df.values[:, :-1]
x_validation_normalized = scaler.fit_transform(x_validation)

# Select validation targets.
y_validation = validation_df.values[:, -1]


def model_config():

    # Create model.
    model = Sequential()

    # Add fully connected hidden layer.
    model.add(Dense(units=12, activation='relu'))

    # Add output neuron.
    model.add(Dense(units=1, activation='sigmoid'))

    # Compile model.
    model.compile(loss='binary_crossentropy',
                  optimizer='Adam', metrics=['accuracy'])

    return model


filepath = "../trained network/{epoch:02d}-{val_acc:.2f}"
val_acc = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
val_loss = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='min')

for i in range(20):

    # Create tensorboard log.
    tensorboard = TensorBoard(log_dir="logs/{}".format(i))

    # Train model.
    model = model_config()
    model.fit(x=x_train_normalized, y=y_train, batch_size=20, epochs=26, verbose=1, callbacks=[tensorboard, val_acc, val_loss],
              validation_data=(x_validation_normalized, y_validation), shuffle=False)

