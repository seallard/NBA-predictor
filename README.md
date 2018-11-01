# NBA-predictor
A feedforward neural network for predicting the outcomes of NBA games given current season average box scores for each team. The network is implemented using keras with tensorflow as the backend with gpu-support. For an introduction to neural networks, see chapter 3 of [Neural Networks](http://www.dkriesel.com/_media/science/neuronalenetze-en-zeta2-2col-dkrieselcom.pdf). See [Predicting NBA Games Using Neural
Networks](http://sci-hub.tw/https://www.degruyter.com/view/j/jqas.2009.5.1/jqas.2009.5.1.1156/jqas.2009.5.1.1156.xml?format=INT&intcmp=trendmd) for relevant research.

## Data set
Statistics were collected for 1230 games in the 2017-18 season. The network is trained with data from the first 620 games of the season and evaluated with the following 30 games. Current season averages are used as features for the unplayed games.

## Network

## Installation guide
If you want to run the classifier you will need to install CUDA, cudnn and tensorflow. This can be quite a hassle on windows, so follow [this guide](https://www.pugetsystems.com/labs/hpc/The-Best-Way-to-Install-TensorFlow-with-GPU-Support-on-Windows-10-Without-Installing-CUDA-1187/).
