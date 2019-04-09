# This script generates the training_dataset.csv.
# Each row contains statistics for a game and they are sorted by date. Each row consists of 10 scores for the 
# home team and 10 scores for the away team, the outcome, team names and the date. The outcome, names and date 
# are removed in predictor.py. So the training vectors will consist of 20 elements.  

import csv
import pandas as pd
import numpy as np


def team_average(team_name, game_number, df):

    partial_df = df.iloc[:game_number,:]
    home_games = partial_df.loc[partial_df['home_team'] == team_name].iloc[:, 2:12]
    away_games = partial_df.loc[partial_df['away_team'] == team_name].iloc[:, 12:-2]

    averages = np.divide(home_games.mean().values + away_games.mean().values, 2).tolist()

    return averages


year = "2017_18"

with open("../data sets/clean_{}.csv".format(year)) as infile:
    reader = csv.reader(infile)
    data = list(reader)

with open("../data sets/training_{}.csv".format(year), "w") as outfile:
    filewriter = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    
    # Write header. 
    filewriter.writerow(['home_team', 'away_team', 'pts_h', 'fg%_h','3pt%_h','ft%_h','oreb_h','dreb_h',
                        'ast_h','stl_h','blk_h', 'to_h', 'pts_a', 'fg%_a','3pt%_a','ft%_a',
                        'oreb_a', 'dreb_a', 'ast_a','stl_a','blk_a', 'to_a', 'outcome', 'date'])
    
    i = 1
    while i < (len(data)-2):

        row = data[i]

        away_team = [data[i][0]]
        away_stats = data[i][1:-1]

        home_team = [data[i+1][0]]
        home_stats = data[i+1][1:-1]

        date = [row[-1]]
        
        if int(home_stats[0]) - int(away_stats[0]) > 0:
            outcome = [1]

        else:
            outcome = [0]  # Home team lost.

        # Save home, away statistics, date and outcome to one row.
        filewriter.writerow(home_team + away_team + home_stats + away_stats + outcome + date)
        
        i += 2

# Sort training data by date. 
df = pd.read_csv("../data sets/training_{}.csv".format(year))
df = df.sort_values('date')


# Collect average statistics of teams in the validation games and write to csv.
with open("../data sets/training_{}.csv".format(year), "w", newline='') as outfile:

    filewriter = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)

    # Write header
    filewriter.writerow(['pts_h', 'fg%_h', '3pt%_h', 'ft%_h', 'oreb_h', 'dreb_h',
                            'ast_h', 'stl_h', 'blk_h', 'to_h', 'pts_a', 'fg%_a', '3pt%_a', 'ft%_a', 'oreb_a',
                            'dreb_a', 'ast_a', 'stl_a', 'blk_a', 'to_a', 'outcome'])

    # Iterate over games
    for i in range(len(df)):

        validation_game = df[i:i+1]

        home_team_name = validation_game['home_team'].tolist()[0]

        away_team_name = validation_game['away_team'].tolist()[0]

        outcome = validation_game['outcome'].tolist()[0]

        # Calculate team averages up until current game.
        home_team_averages = team_average(home_team_name, i, df)
        away_team_averages = team_average(away_team_name, i, df)

        validation_vector = home_team_averages + away_team_averages + [outcome]

        # Write to statistics to csv.
        filewriter.writerow(validation_vector)

df = pd.read_csv("../data sets/training_{}.csv".format(year))
df.dropna(how='any', inplace=True)
df.to_csv("../data sets/training_{}.csv".format(year), index=False)