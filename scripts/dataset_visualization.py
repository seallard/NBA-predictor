import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import matplotlib.patches as mpatches

def diff(i):
    """
    Returns the difference between scores in two rows i and row i+1 as
    home team scores - away team scores. 
    """
    # Select rows from data frame.
    first_row = df.iloc[i]
    second_row = df.iloc[i+1]

    # Determine which row represents home team scores.
    if first_row['home']:
        home = first_row
        away = second_row
    
    else:
        home = second_row
        away = first_row

    return home-away

# Load data into pandas dataframe.
df = pd.read_csv('clean_dataset.csv')

# Selecting which parameters (x, y, z), columns in the data set, to plot together.
scores_to_plot = [('dreb', 'blk', 'to'), ('fg', '3pt', 'ft'), ('oreb', 'ast', 'stl'), ('reb', 'pf', 'pts')] 

# Corresponding axis labels. 
axis_labels = {'dreb':'Defensive rebound', 'fg':'Field goal', 'oreb':'Offensive rebound', 'reb':'Total rebound',
                'blk':'Block', '3pt':'3 pointer', 'ast':'Assist', 'pf':'Personal foul', 'to':'Turnover', 'ft':'Freethrow', 
                'stl':'Steal', 'pts':'Total point'}

# Iterate over the selected parameters to plot. 
for p, parameters in enumerate(scores_to_plot):

    # Initialize plot. 
    fig = plt.figure(p)
    ax = fig.add_subplot(111, projection='3d')
    
    # Iterate over data set and plot selected parameters.
    for i in range(0, df.shape[0], 2):

        # Calculate difference between box scores in consecutive rows.
        game_result = diff(i)

        # Set color of data point to green if home team won, else red.
        if game_result['pts'] > 0:
            color = 'green' 

        else:
            color = 'red'
            
        # Collect coordinates for selected parameters.
        x_column, y_column, z_column = parameters

        x = game_result[x_column]
        y = game_result[y_column]
        z = game_result[z_column]

        # Plot data point (each point represents a single game).
        ax.scatter(x, y, z, c=color)
    
    # Set axis labels.
    ax.set_xlabel(axis_labels[x_column] + ' difference')
    ax.set_ylabel(axis_labels[y_column] + ' difference')
    ax.set_zlabel(axis_labels[z_column] + ' difference')

    # Set legend.
    green_patch = mpatches.Patch(color='green', label='Home team won')
    red_patch = mpatches.Patch(color='red', label='Home team lost')
    plt.legend(handles=[green_patch, red_patch])
    
plt.show()