# Pac-Man-RL-AI
This repository contains the code to build a self learning AI Bot for the game Pac-Man

Initially we are going to train and test it on the relatively smaller layout with 2 ghosts instead of 4.

The following features were used to represent a state in our neural network: 
1. Distance to blinky: Blinky is the red ghost that can kill pacman and end the game. 
2. Distance to inky: Inky is the blue ghost that can kill pacman and end the game. 
3. Distance to intersection: This is the tile at which the ghosts can change their direction of movement. 
4. Distance to nearest coin: Coin are the objects that we have to collect and increase our score.

Reward Values
The following reward values were used to calculate reward: 
1. Game end by death: -100 
2. Game end by winning: +100 
3. Collecting 1 coin: +10 
4. Going into an empty tile: -5

THE NETWORK 

The network consists of one hidden layer apart from one input and one output layer. The input layer has 4 units for the respective state features. The hidden layer has 10 hidden units i.e the weights and the output layer have one single unit i.e. the output of the network. First and second as well as second and third layers are fully connected. 
Instead of producing different output for every possible action, we are producing only one output because the input features given to the network are such that they correspond to the transformation from state s to state s’ through the action a instead to corresponding to a single state s. 
The whole network was implemented in python with the help of libraries tensorflow and numpy. For the transformation between one layer to another within the network weight matrix W(layer number) with dimensions [hidden units in previous layer, hidden units in next layer] were used along with a bias matrix. In addition to this, ReLu (rectified liner unit) function was used for the activation. For the training process, mini batches of size 32 with jumbled data from the database were used along with a RMS prop optimizer.

References :
1. CS188 by UC Berkeley – Intro to AI by Pieter Abbeel 
Excellent learning material for Q-learning and reinforcement learning. 
2. Implementation of Deep Q neural networks by Tejas Kulkarni (MIT) 
Deep Q neural networks for ATARI games

Use :
To see the trained model execute 
python train.py ckpt/model_1080
To start the training from initial state execute
delete the checkpoints saved in folder ckpt
python train.py
