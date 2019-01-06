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
games = [('Bulls', 'Nets'), ('Timberwolves', 'Lakers'), ('Clippers', 'Magic'), ('Hawks','Heat'),('Thunder','Wizards'),
         ('Raptors','Pacers'),('Suns','Hornets')]

odds = [(2.15, 1.74),(1.40, 3.05),(1.35,3.30), (3.05, 1.40),(1.16,5.50),(1.55,2.60),(2.10,1.76)]

print("------------------")

# Make prediction for each game.
for i, game in enumerate(games):
    home_team, away_team = game

    # Calculate season averages for teams.
    home_team_averages = team_average(home_team, len(df), df)
    away_team_averages = team_average(away_team, len(df), df)
    game = np.asarray([home_team_averages + away_team_averages])

    # Make prediction.
    prediction = model.predict(game)[0][0]
    
    # Bookmakers odds. 
    home_odds, away_odds = odds[i]

    # Calculate bookmakers implied probabilities. 
    bookmakers_fee = 1.041
    home_implied_probability = round(1/(home_odds*bookmakers_fee),3)
    away_implied_probability = round(1/(away_odds*bookmakers_fee),3)

    # Check if the networks expectations are larger than the bookmakers by 0.10 for home team.
    print("Implied probability: {} that {} wins. Odds: {}".format(home_implied_probability, home_team, home_odds))
    print("Prediction: {} that {} wins.".format(prediction, home_team))

    # Check if the networks expectations are larger than the bookmakers by 0.10 for away team.
    print("Implied probability: {} that {} will win. Odds: {}".format(away_implied_probability, away_team, away_odds))
    print("Network gives a probability of {} that {} wins.".format(1-prediction, away_team))
    
    print("------------------")