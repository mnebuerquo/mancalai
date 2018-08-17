# Mancala AI Experiment

## Presentation

[View the Slide Show (https://mnebuerquo.github.io/mancalai/)](https://mnebuerquo.github.io/mancalai/)

## Rules for Mancala

[As found on the interwebs](https://www.thespruce.com/how-to-play-mancala-409424):

1. The Mancala board is made up of two rows of six holes, or pits, each. If you don't have a Mancala board handy, substitute an empty egg carton.
1. Four pieces—marbles, chips, or stones—are placed in each of the 12 holes. The color of the pieces is irrelevant.
1. Each player has a store (called a Mancala) to the right side of the Mancala board. (Cereal bowls work well for this purpose if you're using an egg carton.)
1. The game begins with one player picking up all of the pieces in any one of the holes on his side.
1. Moving counter-clockwise, the player deposits one of the stones in each hole until the stones run out.
1. If you run into your own store, deposit one piece in it. If you run into your opponent's store, skip it.
1. If the last piece you drop is in your own store, you get a free turn.
1. If the last piece you drop is in an empty hole on your side, you capture that piece and any pieces in the hole directly opposite.
1. Always place all captured pieces in your store.
1. The game ends when all six spaces on one side of the Mancala board are empty.
1. The player who still has pieces on his side of the board when the game ends capture all of those pieces.
1. Count all the pieces in each store. The winner is the player with the most pieces.

## Game Board

To represent the game board on the console, we will draw an ascii table:
```
+---+---+---+---+---+---+---+---+
|   | 4 | 4 | 4 | 4 | 4 | 4 |   |
|   +---+---+---+---+---+---+   |
|   | 4 | 4 | 4 | 4 | 4 | 4 |   |
+---+---+---+---+---+---+---+---+
```

The numbers in the squares are the count of stones in the bowl. The larger
end boxes are the bowls where you collect your captured stones. 

## AI 

These are all the AI modules I've added so far. There will be more.

### Dumb Luck

This AI is the trivial case. It chooses randomly from the available legal
moves. This one should only rarely win a game.

### Minimax

For years, the state of the art in Chess AI was in variations on the Minimax
algorithm. The basic algorithm is that each player is trying to maximize its
own score with each move, while minimizing the score of the opposing player.
Variations on this include Alpha-Beta Pruning, and a database of previously
scored moves.

I implemented a basic version of depth first minimax search. This is slow,
especially in python, so I have not used it for training the neural networks.

### Neural Networks

Since [AlphaZero](https://www.chess.com/news/view/google-s-alphazero-destroys-stockfish-in-100-game-match),
we can expect more use of neural networks for playing board games. My goal
is to create some basic trained networks using an adversarial approach
against the Minimax solution, then use the trained networks as trainers for
new networks and to improve themselves.

Most of this repo is about training neural networks to play.

These are the neural networks I have put together so far:

* greedy - Not a neural network, a deterministic algorithm
* luck - Not a neural network, just randomly choose a move
* nn1h128 - One hidden layer, 128 neurons
* nn2h80 - Two hidden layers, 80 neurons each
* nn3h80 - Three hidden layers, 80 neurons each
* nns1h128 - Input only includes the 12 cups, no mancalas
* nnx1h128 - One-hot encoding inputs
* nnx3h80 - One-hot encoding inputs
* cnns1h128 - a very simple convolutional neural network

# Project Structure

All of the game rules and AI modules are in the [mancala](./mancala) directory.
The game rules with tests are in [game_state.py](./mancala/game_state.py).
AI modules are in the [mancala/ai](./mancala/ai) directory, and look for the
base class for my neural networks in [nn_lib](./mancala/ai/lib/nn_lib.py).

Tools for running in Docker containers are in [deploy](./deploy).
There is a very simple HTTP API in [webapi](./webapi).

## Build the Docker container

These instructions all run the programs in docker containers. First you must
build a container to run in.

All of these commands start in the top level directory of this repo.

```bash
./deploy/build.sh dev
```

## How to run the programs

### CI

I use autopep8, flake8, and doctest to keep my code neat and tested.

```bash
./deploy/dev.sh --ci /dev/null
```

### Random Training
To simply start training all the neural networks at once, use the random_train
module:

```bash
./deploy/dev.sh mancala/random_train.py
```

This will randomly match neural networks against each other, or against luck or
greedy algorithms. After each game, the moves will be saved, and after a batch
of games the training will begin. This will run forever or until you stop it
(ctrl+c), training all neural networks from the moves recorded in all of the
games played.

You may also specify a list of AI players on the comnand line to limit the
matches to just those players.

### Adversarial

Sometimes you want two neural networks to practice against each other. This
allows them both to improve their skills by playing batches of games against
each other. As one improves, the other should improve also.

To start this kind of training you must specify which networks are to train:
```bash
./deploy/dev.sh mancala/adversary.py nn1h128 cnns1h128
```

### Play Human vs. Machine

When you want to play against any of the AI players, specify which ai you want
on the command line:

```bash
./deploy/dev.sh mancala/play.py nn1h128
```

### Tournament Mode

To play each AI against the others and get a table of their win rates:
```bash
./deploy/dev.sh mancala/tournament.py 3
```

The `3` is the number of matches between each pair of AI players.

### Training from Files

To train an AI player from a set of saved game moves, you must specify the name
of the AI on the command line:

```bash
./deploy/dev.sh mancala/train.py nn1h128
```

This will train that AI using moves saved in JSONL files in the
[training](./training) directory.
