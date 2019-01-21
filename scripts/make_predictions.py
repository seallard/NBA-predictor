# This script use the trained netork to make new predictions and compares them to the bookmakers probabilitie. 
# It requires (atm) you to enter the competing teams and the bookmakers odds for the game.

import csv
import pandas as pd
import numpy as np

from keras.models import load_model
from validation_dataset import team_average

from datetime import date
from datetime import timedelta

# Load trained network. 
model = load_model("../trained network/net_1")

# Load data set to calculate season averages below.
df = pd.read_csv("../data sets/prediction_dataset.csv")

# Games to be predicted as tuples of (home, away). 
games = [('Wizards', 'Knicks'), ('Pacers', '76ers'),('Hornets', 'Kings'), ('Raptors','Suns'), ('Nuggets', 'Bulls'), ('Thunder', 'Lakers')]

# Bookmakers odds (home, away).
odds = [(1.33, 3.40),(1.66, 2.30),(1.64, 2.35),(1.090, 8.00),(1.090, 8.00),(1.18, 5.25)]

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

        # Difference of implied probability and networks probability
        prob_dif = prediction - home_implied_probability 
        
        #Prints to terminal
        print("Implied probability: {:.3f}% that {} wins. Odds: {}".format(home_implied_probability*100, home_team, home_odds))
        print("Prediction: {:.3f}% that {} wins.".format(prediction*100, home_team))

        print("Implied probability: {:.3f}% that {} will win. Odds: {}".format(away_implied_probability*100, away_team, away_odds))
        print("Network gives a probability of {:.3f}% that {} wins.".format((1-prediction)*100, away_team))

        print("Network and implied probability differs with {:.3f}%,".format(abs(prob_dif)*100), end = ' ')
        if prob_dif > 0:
            print("in favor of {}".format(home_team))
        else:
            print("in favor of {}".format(away_team))
        print("------------------")

        #Prints to file
        filewriter.writerow([home_team, away_team, str(date.today() + timedelta(days=1)), home_odds, away_odds, round(prediction, 3)]) 
