import pandas as pd
from time import time
from sklearn.preprocessing import MinMaxScaler

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import Adam, SGD
from keras.callbacks import TensorBoard

# Load training dataset.
training_df = pd.read_csv("training_dataset.csv")

# Select 650 first games, columns 2:-2 as patterns.
X_train = training_df.values[:650, 2:-2]

# Normalize training data.
scaler = MinMaxScaler()
scaler = scaler.fit(X_train)
X_train_normalized = scaler.fit_transform(X_train)

# Select outcomes of 650 first games as targets.
y_train = training_df.values[:650, -2]

# Load validation data set. 
validation_df = pd.read_csv("validation_dataset.csv")

# Select validation inputs and normalize.
X_test = validation_df.values[:, 0:24].astype(float)
X_test_normalized = scaler.fit_transform(X_test)

# Select validation targets.
y_test = validation_df.values[:, 24]

def model_config():

    # Create model. 
    model = Sequential()
    
    # Add input layer.
    model.add(Dense(units=24, input_dim=24, activation='relu'))

    # Add fully connected hidden layer. 
    model.add(Dense(units=8, activation='relu'))
    
    # Add output neuron. 
    model.add(Dense(units=1, activation='sigmoid'))

    # Compile model. 
    model.compile(loss='binary_crossentropy', optimizer='Adam', metrics=['accuracy'])

    return model

# Create tensorboard log.
tensorboard = TensorBoard(log_dir="logs/{}".format(time()))

# Train model.
model = model_config()

model.fit(x=X_train_normalized, y=y_train, batch_size=30, epochs=100, verbose=1, callbacks = [tensorboard], 
          validation_data=(X_test_normalized,y_test), shuffle=False)
