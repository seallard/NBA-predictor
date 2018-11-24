# This script creates a validation data set of games 650-700 in the 17/18-season. 
# Season averages for each team up until game 650 are calculated. These averages
# replace actual stats in games 650-700 and are saved with the outcome. 

import pandas as pd
import numpy as np
import csv

# Load training data set.
df = pd.read_csv("training_dataset.csv")

# Get team names.
team_names = df.home_team.unique()

# Get games up until number 650.
first_df = df[:650]

# Calculate season averages for each team.
all_averages = {}

for team in team_names:

    # Find all games played at home by team and select their stats. 
    home_games = first_df.loc[df['home_team'] == team].iloc[:, 2:14]

    # Find all games played away by team and select their stats. 
    away_games = first_df.loc[df['away_team'] == team].iloc[:, 14:-2]
    
    # Calculate average statistics for team.
    averages = np.divide(home_games.mean().values + away_games.mean().values,2)
    averages = np.round(averages, decimals=3).tolist()

    # Save average stats for team in dictionary with team name as key.
    all_averages[team] = averages

# Select 50 following games. 
validation_games = df[651:682]

# Collect team names and outcomes for games. 
home_teams = validation_games['home_team'].tolist()
away_teams = validation_games['away_team'].tolist()
outcome = validation_games['outcome'].tolist()

# Collect average statistics of teams in the validation games and write to csv. 
with open("validation_dataset.csv", "w", newline='') as outfile:
    
    filewriter = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)

    # Iterate over games 650-700.
    for i in range(50):
        
        validation_vector = all_averages[home_teams[i]] + all_averages[away_teams[i]] + [outcome[i]]
        filewriter.writerow(validation_vector)