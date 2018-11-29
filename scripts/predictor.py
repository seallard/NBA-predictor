import pandas as pd
from time import time

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.callbacks import TensorBoard

# Load training dataset.
training_df = pd.read_csv("training_dataset.csv")

# Select 650 first games, columns 2:-2 as patterns.
X_train = training_df.values[:650, 2:-2]

# Select outcomes of 650 first games as targets.
y_train = training_df.values[:650, -2]

# Load validation data set. 
validation_df = pd.read_csv("validation_dataset.csv")

# Select validation inputs.
X_test = validation_df.values[:, 0:24]

# Select validation targets.
y_test = validation_df.values[:, 24]

def model_config():

    # Create model. 
    model = Sequential()
    
    # Add input layer.
    model.add(Dense(24, input_dim=24, kernel_initializer='normal', activation='relu'))

    # Add hidden layer. 
    model.add(Dense(24, kernel_initializer='normal', activation='sigmoid'))

    # Add output neuron. 
    model.add(Dense(1, kernel_initializer='normal', activation='sigmoid'))
    
    # Compile model. 
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    return model

# Create tensorboard log.
tensorboard = TensorBoard(log_dir="logs/{}".format(time()))

# Train model.
model_config().fit(x=X_train, y=y_train, batch_size=32, epochs=50, verbose=1, 
callbacks = [tensorboard], validation_data=(X_test,y_test), shuffle=True)