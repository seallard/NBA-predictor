# NBA-predictor
A feedforward neural network for predicting the outcome of NBA games given current average box scores for the competing teams. The network is implemented using Keras with TensorFlow as the backend with GPU support.

## Data set
Box scores were collected for 1230 games in the 2017-18 season. The network was trained with individual data from the first 650 games and validated with the following 50 games. The validation data set consists of team averages up until the game being validated, the "unplayed" game. The following features, for the home and away team, were used from the box scores to train the network: 

Acronym | pts | fg % | 3pt % | ft % | oreb | dreb | ast | stl | blk | to 
--- | --- | --- | --- |--- |--- |--- |--- |--- |--- |--- |---
Explanation | points | field goal % | three point % | freethrow % | offensive rebounds | defensive rebounds | assists | steals | blocks | turn overs 


| First Header  | Second Header |
| ------------- | ------------- |
| Content Cell  | Content Cell  |
| Content Cell  | Content Cell  |

The percentages are calculated as made/attempted. Note that all data was normalized. The outcome of the games (1 if the home team won, 0 if it lost) was used as targets.

## Network
The network consists of three dense layers, i.e. fully connected. The input layer consists of 20 nodes, 10 for the home team and 10 for the away team statistics. The hidden layer consists of 12 nodes and the output is a single node. Binary crossentropy was chosen as the loss function and Adam as the optimizer. The input and hidden layer use relu-activation and the output use a sigmoid function. 

## Prerequisites
If you want to train the classifier you will need to install CUDA, cuDNN, TensorFlow and Keras. This can be quite a hassle on Windows, so follow the guide below ([source](https://www.pugetsystems.com/labs/hpc/The-Best-Way-to-Install-TensorFlow-with-GPU-Support-on-Windows-10-Without-Installing-CUDA-1187/)). Note that a NVIDIA GPU card with [compute capability](https://developer.nvidia.com/cuda-gpus) 3.5 or higher is required.

Download and install Anaconda:
[Anaconda3-5.2.0-Windows-x86_64.exe](https://repo.continuum.io/archive/Anaconda3-5.2.0-Windows-x86_64.exe)

Make sure that you check the boxes for "Add Anaconda to path variable" and "Register Anaconda as default python" during the installation.

Open a terminal and run the following commands to update Anaconda:
```
conda update conda
conda update anaconda
conda update python
conda update --all
```

Create an environment named tf-gpu:
```
conda create --name tf-gpu
```

Activate the tf-gpu environment:
```
activate tf-gpu
```

Install TensorFlow with GPU support in the activated environment:
```
conda install -c aaronzs tensorflow-gpu
```

Install the CUDA and cuDNN packages in the activated environment:
```
conda install -c anaconda cudatoolkit
conda install -c anaconda cudnn
```

Install Keras in the activated environment:
```
conda install keras-gpu
```

To verify your installation, run the following in the activated environment:
```
python
import tensorflow as tf
hello = tf.constant('Hello, TensorFlow!')
sess = tf.Session()
print(sess.run(hello))
```

To deactivate the environment: 
```
deactivate
```
