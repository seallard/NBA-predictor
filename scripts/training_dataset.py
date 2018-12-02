# This script generates the training_dataset.csv.
# Each row contains statistics for a game and they are sorted by date. Each row consists of 10 scores for the 
# home team and 10 scores for the away team, the outcome, team names and the date. The outcome, names and date 
# are removed in predictor.py. So the training vectors will consist of 20 elements.  

import csv
import pandas as pd

with open("clean_dataset.csv") as infile:    
    reader = csv.reader(infile)
    data = list(reader)

with open("training_dataset.csv", "w") as outfile:

    filewriter = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    
    # Write header. 
    filewriter.writerow(['home_team', 'away_team', 'pts_h', 'fg%_h','3pt%_h','ft%_h','oreb_h','dreb_h',
                        'ast_h','stl_h','blk_h', 'to_h', 'pts_a', 'fg%_a','3pt%_a','ft%_a','oreb_a',
                        'dreb_a', 'ast_a','stl_a','blk_a', 'to_a', 'outcome', 'date'])
    
    # Create training dataset csv file. 
    for i, row in enumerate(data[1:]):

        # Even rows contain away team score, odd contain home team score.  
        if i % 2:
            away_stats = data[i][1:-1]
            away_team = [data[i][0]]
            
            home_stats = data[i+1][1:-1]
            home_team = [data[i+1][0]]

            date = [row[-1]]

            # Check outcome of game.
            if int(home_stats[0]) - int(away_stats[0]) > 0:

                outcome = [1] # Home team won. 
            
            else:
                outcome = [0] # Home team lost.
            
            # Save home, away statistics, date and outcome to one row.
            filewriter.writerow(home_team + away_team + home_stats + away_stats + outcome + date)
              
# Sort training data by date. 
df = pd.read_csv("training_dataset.csv")
df = df.sort_values('date')

df.to_csv('training_dataset.csv', index=False)