# NBA-predictor
A feedforward neural network for predicting the outcome of NBA games given current average box scores for the competing teams. The network is implemented using Keras with TensorFlow as the backend with GPU support. An average validation accuracy of 72 % was achieved, similar to what was reported in [Predicting NBA Games Using Neural
Networks, Loeffelholz et al. (2009)](http://sci-hub.tw/https://www.degruyter.com/view/j/jqas.2009.5.1/jqas.2009.5.1.1156/jqas.2009.5.1.1156.xml?format=INT&intcmp=trendmd).

## Data set
Box scores were collected for 1230 games in the 2017-18 season. The network was trained with individual data from the first 650 games and validated with the following 50 games. The validation data set consists of team averages up until the game being validated, the "unplayed" game. The following statistics from the box scores, for the home and away team, were used as features to train the network: 

| Acronym | Explanation |
| ------------- | ------------- |
| pts  | points  |
| fg %  | field goal %  |
| 3pt %  | three point %  |
| ft %   | freethrow %  |
| oreb  | offensive rebounds  |
| dreb  | defensive rebounds  |
| ast  | assists  |
| stl  | steals  |
| blk  | blocks  |
| to  | turn overs  |

The percentages are calculated as made/attempted. Note that all data was normalized. The outcome of the games (1 if the home team won, 0 if it lost) was used as targets.

## Network
The network consists of three fully connected layers (20, 12, 1). The input layer consists of 20 nodes, 10 for the home team and 10 for the away team statistics. The hidden layer consists of 12 nodes and the output is a single node. Binary crossentropy was chosen as the loss function and Adam as the optimizer. All layers use a sigmoid activation function. The network was trained over 30 epochs with a batch size of 20.

![Validation accuracy](https://raw.githubusercontent.com/seallard/NBA-predictor/master/graphs/validation_accuracy_20_runs.PNG)

## Results 2019
The accuracy of the model seems to stabilize around 70 % after 100 games played in january 2019, see [spreadsheet](https://docs.google.com/spreadsheets/d/1JHCUvGb0eJoLNHFiahcgNU_1DlFqxn-eiWDytXJX-8M/edit?usp=sharing). 

## Prerequisites
* Tensorflow 1.10.0
* Keras 2.2.4
* Numpy 1.14.5
* Pandas 0.23.4
* Beautifulsoup 4.6.3
* sklearn 0.20.1
* Selenium 3.141.0
* Chromedriver 2.45 (unzip in scripts folder)

To make new predictions using the trained netork (net_1):
1. Run NBA_scraper.py to collect the latest box scores from espn.com. 
2. Run prediction_dataset.py to generate the data set required to make new predictions.
3. Run make_predictions.py. 
