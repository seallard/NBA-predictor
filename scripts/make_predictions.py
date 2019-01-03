# This script use the trained netork to make new predictions and compares them to the bookmakers probabilitie. 
# It requires (atm) you to enter the competing teams and the bookmakers odds for the game.

import pandas as pd
import numpy as np

from keras.models import load_model
from validation_dataset import team_average

# Load trained network. 
model = load_model("net_1")

# Load training data set to calculate season averages below.
df = pd.read_csv("training_dataset.csv")

# Games to be predicted as tuples of (home, away). 
games = [('Cavaliers', 'Celtics')]
odds = [(1.80, 2.05)]

# Make prediction for each game.
for i, game in enumerate(games):
    home_team, away_team = game

    # Calculate season averages for teams.
    home_team_averages = team_average(home_team, len(df), df)
    away_team_averages = team_average(away_team, len(df), df)
    game = np.asarray([home_team_averages + away_team_averages])

    # Make prediction.
    prediction = model.predict(game)[0][0]
    print("Network gives a probability of {} that {} wins.".format(prediction, home_team))
    print("Network gives a probability of {} that {} wins.".format(1-prediction, away_team))
    
    # Bookmakers odds. 
    home_odds, away_odds = odds[i]

    # Calculate bookmakers implied probabilities. 
    bookmakers_fee = 1.041
    home_implied_probability = 1/(home_odds*bookmakers_fee)
    away_implied_probability = 1/(away_odds*bookmakers_fee)

    print("Bookmaker is {} sure that {} will win.".format(home_implied_probability, home_team))
    print("Bookmaker is {} sure that {} will win.".format(away_implied_probability, away_team))

    # Check if the networks expectations are larger than the bookmakers by 0.10.
    if prediction > home_implied_probability + 0.1:
        print("{} might be undervalued, the difference is {}.".format(home_team, prediction - home_implied_probability))

    if 1-prediction > away_implied_probability + 0.1:
        print("{} might be undervalued, the difference is {}.".format(away_team, prediction - away_implied_probability))