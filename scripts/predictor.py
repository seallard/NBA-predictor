import pandas as pd
from time import time
from sklearn.preprocessing import MinMaxScaler

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import Adam
from keras.callbacks import TensorBoard

# Load training dataset.
training_df = pd.read_csv("training_dataset.csv")

# Select 650 first games, columns 2:-2 as patterns.
X_train = training_df.values[:650, 2:-2]

# Normalize training data.
scaler = MinMaxScaler()
X_train_normalized = scaler.fit_transform(X_train)

# Select outcomes of 650 first games as targets.
y_train = training_df.values[:650, -2]

# Rescale training targets from 0 to 0.01 and from 1 to 0.99.
zero_indices = y_train < 1
one_indices = y_train > 0

y_train[zero_indices] = 0.01
y_train[one_indices] = 0.99

# Load validation data set. 
validation_df = pd.read_csv("validation_dataset.csv")

# Select validation inputs and normalize.
X_test = validation_df.values[:, 0:-1]
X_test_normalized = scaler.fit_transform(X_test)

# Select validation targets.
y_test = validation_df.values[:, -1]

# Rescale validation targets from 0 to 0.01 and from 1 to 0.99.
zero_indices = y_test < 1
one_indices = y_test > 0

y_test[zero_indices] = 0.01
y_test[one_indices] = 0.99

def model_config():

    # Create model. 
    model = Sequential()
    
    # Add input layer.
    model.add(Dense(units=20, input_dim=20, activation='sigmoid'))

    # Add fully connected hidden layer. 
    model.add(Dense(units=12, activation='sigmoid'))
    
    # Add output neuron. 
    model.add(Dense(units=1, activation='sigmoid'))

    # Compile model. 
    model.compile(loss='binary_crossentropy', optimizer='Adam', metrics=['accuracy'])

    return model

# Create tensorboard log.
tensorboard = TensorBoard(log_dir="logs/{}".format(time()))

# Train model.
model = model_config()

model.fit(x=X_train_normalized, y=y_train, batch_size=30, epochs=70, verbose=1, callbacks = [tensorboard], 
          validation_data=(X_test_normalized,y_test), shuffle=False)

# Save model. 
model_json = model.to_json()
with open("model.json", "w") as f:
    f.write(model_json)

# Save weights.
model.save_weights("model.h5")