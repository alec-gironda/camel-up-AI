# Camel Up AI

Final Project for Middlebury College CSCI 0311: Artifical Intelligence.

The goal of this project is to develop an intelligent agent for the board game Camel Up. Using reinforcement learning and an expectimax algorithm, our agent should be able to determine the optimal policy at each game state and take actions accordingly.

[Here](https://github.com/alec-gironda/camel-up-AI/blob/main/) is our abstract that describes more of the details surrounding our goals, methods, and results.
[Here](https://github.com/alec-gironda/camel-up-AI/blob/main/) is our poster.

By running `learn.py`, one can simulate 100 games of `MaxPlayer` against `RandomPlayer` (see abstract Table 1 for player class descriptions) to train
a `SmartPlayer`, and then simulate 100 games of `SmartPlayer` against `RandomPlayer`. The program will also print the outcomes of the games.

By running `game.py`, one can play Camel Up against a pre-trained `SmartPlayer`. Our game is built with the `pygame` library.

![](https://github.com/alec-gironda/camel-up-AI/blob/main/)
