import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import matplotlib.patches as mpatches

def diff(row_1,row_2):
    """
    Calculates the differences between box-scores from the csv as 
    home score - away score.
    """
    if row_1['home'] == 1:
        home = row_1
        away = row_2
    
    else:
        home = row_2
        away = row_1
    
    return home-away

# Load data into pandas dataframe.
df = pd.read_csv('clean_dataset.csv')

# Selecting which parameters (x, y, z), columns in the data set, to plot together.
parameters_to_plot = [(4, 8, 9), (0, 1, 2), (3, 6, 7), (5, 10, 11)] 

# Corresponding axis labels. 
xlabels = ['Defensive rebound difference', 'Field goal difference', 'Offensive rebound difference', 'Total rebound difference']
ylabels = ['Block difference', '3pt difference', 'Assist difference', 'Personal foul difference']
zlabels = ['Turnover difference', 'Freethrow difference', 'Steal difference', 'Total point difference']

# Iterate over the selected parameters to plot. 
for p, parameters in enumerate(parameters_to_plot):

    # Initialize plot. 
    fig = plt.figure(p)
    ax = fig.add_subplot(111, projection='3d')
    
    # Iterate over data set plot selected parameters of each game.
    for i in range(0, df.shape[0], 2):

        # Calculate difference between box scores in consecutive rows. 
        game_result = diff(df.ix[i],df.ix[i+1]) 

        # Set color of data point to green if home team won, else red. 
        if game_result[-2] > 0:
            c = 'green' 
        else:
            c = 'red'
    
        # Collect coordinates for selected parameters.
        x_column, y_column, z_column = parameters

        x = game_result[x_column]
        y = game_result[z_column]
        z = game_result[y_column]

        # Plot data point.
        ax.scatter(x, y, z, c=c)
    
    # Format plot.
    ax.set_xlabel(xlabels[p])
    ax.set_ylabel(ylabels[p])
    ax.set_zlabel(zlabels[p])

    green_patch = mpatches.Patch(color='green', label='Home team won')
    red_patch = mpatches.Patch(color='red', label='Home team lost')
    plt.legend(handles=[green_patch, red_patch])

plt.show()