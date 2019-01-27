# This script filters the raw data set and extracts the relevant statistics to clean_dataset.csv.
# 

import csv

with open("../data sets/raw_dataset.csv",'r') as infile:

    next(infile) # Skip header.

    outfile = open("../data sets/clean_dataset.csv",'w', newline='')
    writer = csv.writer(outfile)
    writer.writerow(['team', 'pts', 'fg%', '3pt%', 'ft%', 'oreb', 'dreb', 'ast', 'stl', 'blk', 'to', 'date'])

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
        writer.writerow(clean_row)