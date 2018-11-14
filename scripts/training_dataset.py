# This script generates the training_dataset.csv.
# Each row consists of 12 scores for the home team and 12 scores for 
# the away team, the outcome and the date. So the training vectors will 
# consist of 25 elements. The games are sorted by date. 

import csv
import pandas as pd

with open("clean_dataset.csv") as infile:    
    reader = csv.reader(infile)
    data = list(reader)

with open("training_dataset.csv", "w") as outfile:

    filewriter = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        
    # Write header. 
    filewriter.writerow(['fg_h','3pt_h','ft_h','oreb_h','dreb_h','reb_h','ast_h','stl_h','blk_h',
                        'to_h','pf_h','pts_h', 'fg_a','3pt_a','ft_a','oreb_a','dreb_a','reb_a',
                        'ast_a','stl_a','blk_a', 'to_a','pf_a','pts_a', 'outcome', 'date'])
    
    # Creating training dataset csv file. 
    for i, row in enumerate(data[1:]):

        # Two consecutive rows contains, in order, home and away team scores.
        if i % 2:
            away_team = data[i]
            home_team = data[i+1][:-1]
            
            # Check outcome of game.
            if int(home_team[-1]) - int(away_team[-2]) > 0:

                outcome = 1 # Home team won. 
            
            else:
                outcome = 0 # Home team lost.
            
            # Save home, away statistics, date and outcome to one row.
            filewriter.writerow(home_team + away_team[:-1] + [outcome] + [away_team[-1]])
              
# Sort training data by date. 
df = pd.read_csv("training_dataset.csv")
df = df.sort_values('date')

df.to_csv('training_dataset.csv', index=False)