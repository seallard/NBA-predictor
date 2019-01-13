# This script use the trained netork to make new predictions and compares them to the bookmakers probabilitie. 
# It requires (atm) you to enter the competing teams and the bookmakers odds for the game.

import csv
import pandas as pd
import numpy as np

from keras.models import load_model
from validation_dataset import team_average

from datetime import date

# Load trained network. 
model = load_model("../trained network/net_1")

# Load data set to calculate season averages below.
df = pd.read_csv("prediction_dataset.csv")

# Games to be predicted as tuples of (home, away). 
games = [('76ers', 'Hawks'), ('Wizards', 'Bucks'),('Raptors', 'Nets'), ('Knicks','Pacers'), ('Rockets', 'Cavaliers'), ('Timberwolves', 'Mavericks'), ('Trail Blazers', 'Hornets'), ('Jazz', 'Lakers'), ('Warriors', 'Bulls')]

# Bookmakers odds (home, away).
odds = [(1.10, 7.25),(2.95, 1.42),(1.20,4.75),(4.20, 1.25),(1.076, 9.00),(1.52, 2.67),(1.40, 3.05),(1.28, 3.75),(1.058, 11.00)]

print("------------------")

with open("../data sets/make_prediction.csv", "w+", newline='') as outfile:

    filewriter = csv.writer(outfile,delimiter=',',quoting=csv.QUOTE_MINIMAL)

    # Make prediction for each game.
    for i, game in enumerate(games):
        home_team, away_team = game

        # Calculate season averages for teams.
        home_team_averages = team_average(home_team, len(df), df)
        away_team_averages = team_average(away_team, len(df), df)
        game = np.asarray([home_team_averages + away_team_averages])
    
        # Make prediction.
        prediction = model.predict(game)[0][0]

        # Calculate bookmakers implied probabilities. 
        home_odds, away_odds = odds[i]
        bookmakers_fee = 1.041
        home_implied_probability = round(1/(home_odds*bookmakers_fee),3)
        away_implied_probability = round(1/(away_odds*bookmakers_fee),3)

        #Prints to terminal
        print("Implied probability: {} that {} wins. Odds: {}".format(home_implied_probability, home_team, home_odds))
        print("Prediction: {} that {} wins.".format(prediction, home_team))

        print("Implied probability: {} that {} will win. Odds: {}".format(away_implied_probability, away_team, away_odds))
        print("Network gives a probability of {} that {} wins.".format(1-prediction, away_team))
    
        print("------------------")

        #Prints to file
        filewriter.writerow([home_team, away_team, str(date.today()), home_odds, away_odds, round(prediction, 3)]) 
