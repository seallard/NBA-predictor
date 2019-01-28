# This script uses the trained model to make predictions for upcoming games.
# Competing teams and odds are collected from the bookmakers site automatically. 
# Download chromedriver from https://chromedriver.storage.googleapis.com/index.html?path=2.45/ 
# and unzip it in this folder (scripts). 

import csv
import pandas as pd
import numpy as np

from keras.models import load_model
from validation_dataset import team_average

from datetime import date
from datetime import timedelta

from selenium import webdriver 
import time as time

# Choose model 1 (uses home+away average) or 5 (uses away or home averages).
model_name = input("Choose net, 1 (tested, ca 70 % acc) or 5 (not tested yet):  \n")
model = load_model("../trained network/net_{}".format(model_name))

# Load data set to calculate season averages below.
df = pd.read_csv("../data sets/prediction_dataset.csv")

# Collect games and odds from bookmaker.  
chrome_driver_path = "./chromedriver_win32/chromedriver.exe"
browser = webdriver.Chrome(executable_path=chrome_driver_path)

url = "https://www.bet365.com/?&cb=10326423948#/AC/B18/C20604387/D48/E1453/F10/"
browser.get(url)
browser.get(url) # Get past advert.
time.sleep(8)

teams = browser.find_elements_by_class_name("sl-CouponParticipantGameLineTwoWay_NameText ")
team_iterator = iter([team.text.split(" ")[-1] for team in teams])
games = list(zip(team_iterator, team_iterator)) # Tuples (away team, home team).


odds = browser.find_elements_by_class_name("gl-ParticipantCentered_NoHandicap")
odds = [odd.text for odd in odds][-len(teams):]
odds_iterator = iter([float(odd) for odd in odds])
odds = list(zip(odds_iterator, odds_iterator)) # Tuples (away odds, home odds).

browser.quit()

print("------------------------------------------------------------------")

with open("../data sets/make_prediction.csv", "w+", newline='') as outfile:

    filewriter = csv.writer(outfile,delimiter=',',quoting=csv.QUOTE_MINIMAL)

    # Make prediction for each game.
    for i, game in enumerate(games):

        away_team, home_team = game

        # Fix name error.
        if away_team == "Blazers":
            away_team = "Trail Blazers"
        
        if home_team == "Blazers":
            home_team = "Trail Blazers"

        # Calculate season averages for teams.
        home_team_averages = team_average(home_team, len(df), df, "home", model_name)
        away_team_averages = team_average(away_team, len(df), df, "away", model_name)
        
        # Input vector of home team and away team averages.
        game = np.asarray([home_team_averages + away_team_averages])
        
        # Make prediction.
        prediction = model.predict(game)[0][0]

        # Calculate bookmakers implied probabilities. 
        away_odds, home_odds = odds[i]
        bookmakers_fee = 1.041
        home_implied_probability = round(1/(home_odds*bookmakers_fee), 3)
        away_implied_probability = round(1/(away_odds*bookmakers_fee), 3)
        
        print("Implied probability: {:.3f}% that {} wins. Odds: {}".format(home_implied_probability*100, home_team, home_odds))
        print("Prediction: {:.3f}% that {} wins.".format(prediction*100, home_team))

        print("Implied probability: {:.3f}% that {} will win. Odds: {}".format(away_implied_probability*100, away_team, away_odds))
        print("Prediction: {:.3f}% that {} wins.".format((1-prediction)*100, away_team))

        print("------------------------------------------------------------------")

        # Write to file.
        filewriter.writerow([home_team, away_team, str(date.today() + timedelta(days=1)), home_odds, away_odds, round(prediction, 3)])