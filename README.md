# NBA-predictor
A feedforward neural network for predicting the outcomes of NBA games given current season average box scores for each team. The network is implemented using keras with tensorflow as the backend with gpu-support. For an introduction to neural networks, see chapter 3 of [Neural Networks](http://www.dkriesel.com/_media/science/neuronalenetze-en-zeta2-2col-dkrieselcom.pdf). See [Predicting NBA Games Using Neural
Networks](http://sci-hub.tw/https://www.degruyter.com/view/j/jqas.2009.5.1/jqas.2009.5.1.1156/jqas.2009.5.1.1156.xml?format=INT&intcmp=trendmd) for relevant research.

## Data set
Statistics were collected for 1230 games in the 2017-18 season. The network is trained with data from the first 620 games of the season and evaluated with the following 30 games. Current season averages are used as features for the unplayed games.

## Network

## Prerequisites
If you want to train the classifier you will need to install CUDA, cudnn and tensorflow. This can be quite a hassle on Windows, so follow the guide below ([source](https://www.pugetsystems.com/labs/hpc/The-Best-Way-to-Install-TensorFlow-with-GPU-Support-on-Windows-10-Without-Installing-CUDA-1187/)).

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

Install tensorflow with gpu-support in the activated environment:
```
conda install -c aaronzs tensorflow-gpu
```

Install the CUDA and cuDNN packages in the activated environment:
```
conda install -c anaconda cudatoolkit
conda install -c anaconda cudnn
```

To check that your installation is functioning, run the following in the activated environment:
```
python
import tensorflow as tf
hello = tf.constant('Hello, TensorFlow!')
sess = tf.Session()
print(sess.run(hello))
```
