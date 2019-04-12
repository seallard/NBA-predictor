# Test network (net_1) trained with data from 17-18 season with games from 18-19 season.

import pandas as pd
import numpy as np
from keras.models import load_model
import math
from sklearn.preprocessing import MinMaxScaler
import os

year = "2017_18"
scaler = MinMaxScaler()

df = pd.read_csv("../data sets/training_{}.csv".format(year))
norm_df = scaler.fit_transform(df)


for net in os.listdir("../trained network/"):

    model = load_model("../trained network/" + net)

    correct_predictions = 0
    made_predictions = 0
    
    for game in norm_df:
        
        stats = np.reshape(game[:-1], (1, 20))
        prediction = model.predict(stats)[0][0]

        if not math.isnan(prediction):
            made_predictions += 1

            if int(round(prediction)) == game[-1]:
                correct_predictions += 1

    print("Model: {}".format(net))
    print("Correct predictions: " + str(round(100*correct_predictions/made_predictions, 3)) + " %")