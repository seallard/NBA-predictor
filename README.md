# NBA-predictor
A feedforward neural network for predicting the outcome of NBA games given current average box scores for the competing teams. The network is implemented using Keras with TensorFlow as the backend with GPU support. The model predicts ca 60 % of the games in the 2018-19 season correctly atm.

## TODO 
* Refactor and debug.
* ~~Train with the same data used for prediction and validation (averages).~~
* Normalize prediction data.
* Tune parameters: random search?
* Add keras callback to save model at each epoch.

## Data set
Box scores were collected for 1230 games in the 2017-18 season. The network was trained with the first 650 games and validated with the following 50 games. Averages of the following box scores were used as features: 

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

## Results 2019
The accuracy of the model seems to stabilize around 70 % after 100 games played in january 2019, see [spreadsheet](https://docs.google.com/spreadsheets/d/1JHCUvGb0eJoLNHFiahcgNU_1DlFqxn-eiWDytXJX-8M/edit?usp=sharing). 

## Dependencies
* Tensorflow 1.10.0
* Keras 2.2.4
* Numpy 1.14.5
* Pandas 0.23.4
* Beautifulsoup 4.6.3
* sklearn 0.20.1
* Selenium 3.141.0
* Chromedriver 2.45 (unzip in scripts folder)
