# Test network (net_1) trained with data from 17-18 season with games from 18-19 season.

import pandas as pd
import numpy as np
from keras.models import load_model
import math
from sklearn.preprocessing import MinMaxScaler

year = "2017_18"
df = pd.read_csv("../data sets/training_{}.csv".format(year))

scaler = MinMaxScaler()


for m in range(20):

    model = load_model("../trained network/net_{}".format(m))

    correct_predictions = 0
    made_predictions = 0
    
    for i, game in df.iterrows():
        test = [game.values[:-1]]
        normalized_averages = scaler.fit_transform(test)
        
        prediction = model.predict(normalized_averages)[0][0]

        if not math.isnan(prediction):
            made_predictions += 1

            if int(round(prediction)) == game['outcome']:
                correct_predictions += 1

    print("Model: {}".format(m))
    print("Number of predictions made: " + str(made_predictions))
    print("Correct predictions: " + str(correct_predictions/made_predictions))