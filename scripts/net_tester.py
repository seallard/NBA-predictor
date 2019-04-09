# Test network (net_1) trained with data from 17-18 season with games from 18-19 season.

import pandas as pd
import numpy as np
from keras.models import load_model
import math
from sklearn.preprocessing import MinMaxScaler

year = "2017_18"
scaler = MinMaxScaler()

df = pd.read_csv("../data sets/training_{}.csv".format(year))
norm_df = scaler.fit_transform(df)

for m in range(10):

    model = load_model("../trained network/net_{}".format(m))

    correct_predictions = 0
    made_predictions = 0
    
    for game in norm_df:
        
        stats = np.reshape(game[:-1], (-1, len(game[:-1])))
        prediction = model.predict(stats)[0][0]
        

        if not math.isnan(prediction):
            made_predictions += 1

            if int(round(prediction)) == game[-1]:
                correct_predictions += 1

    print("Model: {}".format(m))
    print("Number of predictions made: " + str(made_predictions))
    print("Correct predictions: " + str(correct_predictions/made_predictions))