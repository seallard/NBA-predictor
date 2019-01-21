# This script creates the prediction data set, used by make_predictions.py
import csv
import pandas as pd

with open("../data sets/2018_19_dataset.csv",'r') as infile:
    next(infile) # Skip header.
    
    data = []
    
    for row in infile:
        row = row.split(',')

        # Calculate field goals made percentage. 
        fg_made = row[0].split('-')[0]
        fg_attempted = row[0].split('-')[-1]
        fg_percent = round(int(fg_made)/int(fg_attempted), 4)

        # Calculate three-points made percentage.
        threept_made = row[1].split('-')[0]
        threept_attempted = row[1].split('-')[-1]
        threept_percent = round(int(threept_made)/int(threept_attempted), 4)

        # Calculate freethrows made percentage. 
        ft_made = row[2].split('-')[0]
        ft_attempted = row[1].split('-')[-1]
        ft_percent = round(int(ft_made)/int(ft_attempted), 4)

        # Extract remaining variables of interest. 
        date = row[-1].strip('\n')
        team = row[-3]

        points = row[11]
        rebounds = row[3:5]
        other_stats = row[6:10]

        # Save values
        clean_row = [team, points, fg_percent, threept_percent, ft_percent] + rebounds + other_stats + [date]

        # Write clean data to outfile.
        data.append(clean_row)

with open("../data sets/prediction_dataset.csv", "w", newline='') as outfile:

    filewriter = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    
    # Write header. 
    filewriter.writerow(['home_team', 'away_team', 'pts_h', 'fg%_h','3pt%_h','ft%_h','oreb_h','dreb_h',
                        'ast_h','stl_h','blk_h', 'to_h', 'pts_a', 'fg%_a','3pt%_a','ft%_a','oreb_a',
                        'dreb_a', 'ast_a','stl_a','blk_a', 'to_a', 'outcome','date'])
    
    for i, row in enumerate(data):
        if i > len(data)-2:
            break

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
df = pd.read_csv("../data sets/prediction_dataset.csv")
df = df.sort_values('date')

df.to_csv('../data sets/prediction_dataset.csv', index=False)
