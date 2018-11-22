import pandas as pd
from time import time

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.callbacks import TensorBoard

# Load training dataset.
df = pd.read_csv("training_dataset.csv")

# Select all rows (games), columns 0:24 as patterns. 
training_samples = df.values[:, 0:24]

# Select all rows, column 24 as correct outputs. 
targets = df.values[:, 24]

def model_config():

    # Create model. 
    model = Sequential()
    
    # Add hidden layer of the same dimensionality as the input layer.
    model.add(Dense(24, input_dim=24, kernel_initializer='normal', activation='relu'))

    # Add output neuron. 
    model.add(Dense(1, kernel_initializer='normal', activation='sigmoid'))
    
    # Compile model. 
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    return model

# Create tensorboard log.
tensorboard = TensorBoard(log_dir="logs/{}".format(time()))

# Train model.
model_config().fit(x=training_samples, y=targets, batch_size=32, epochs=50, verbose=1, 
callbacks = [tensorboard], validation_split=0.3, shuffle=True)