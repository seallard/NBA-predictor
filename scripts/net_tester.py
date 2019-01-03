# Test network (net_1) trained with data from 17-18 season with games from 18-19 season.
import pandas as pd
import numpy as np
from keras.models import load_model
from validation_dataset import team_average

model = load_model("net_1")
df = pd.read_csv("training_dataset.csv")

correct_predictions = 0
made_predictions = 0

for i, game in df.iterrows():

    if i > 510:
        home_team_averages = team_average(game['home_team'], i, df)
        away_team_averages = team_average(game['away_team'], i, df)
        averages = np.asarray([home_team_averages + away_team_averages])

        prediction = int(round(model.predict(averages)[0][0]))
        made_predictions += 1
        outcome = game['outcome']
        
        if prediction == outcome:
            correct_predictions += 1

print("Number of predictions made: " + str(made_predictions))
print("Correct predictions: " + str(correct_predictions/made_predictions))