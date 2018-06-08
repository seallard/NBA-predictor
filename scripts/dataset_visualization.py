import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

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


#Initialize plot. 
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#Load data into pandas dataframe.
df = pd.read_csv('clean_dataset.csv')

#Iterate over dataframe and plot each game. 
i=0
while i < df.shape[0]:
    game_result = diff(df.ix[i],df.ix[i+1]) #Takes two consecutive rows and calls diff function. 
    i += 2

    #Set color of data point, if home won: green, else: red. 
    if game_result[-2] > 0:
        c = 'green'
    else:
        c = 'red'
    
    #Plot data points (change indexes to plot different score differentials). 
    x = game_result[3]
    y = game_result[6]
    z = game_result[7]
    
    ax.scatter(x, y, z, c=c)


ax.set_xlabel('Offensive rebound differential')
ax.set_ylabel('Assist differential')
ax.set_zlabel('Steal differential')

plt.show()