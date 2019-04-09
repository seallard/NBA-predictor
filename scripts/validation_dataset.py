# This script creates a validation data set of games 650-700 in the 17/18-season.
# Season averages are calculated for each team up until the game being played. These averages
# replace actual stats in games 650-700 and are saved with the outcome.

import pandas as pd
import numpy as np
import csv

year = "2017_18"

df = pd.read_csv("../data sets/training_{}.csv".format(year))
validation_df = df.iloc[650:700, :]
validation_df.to_csv('../data sets/validation_2017_18.csv', index=False)