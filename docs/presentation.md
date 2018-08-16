# Playing Mancala using Tensorflow
<img src="https://images-na.ssl-images-amazon.com/images/I/81Y6ZP4rQWL._SL1500_.jpg" title="Photo of Mancala board" style="width:80%; height:auto;"/>

---

# Rules - The board

1. The Mancala board is made up of two rows of six holes, or pits, each. If you don't have a Mancala board handy, substitute an empty egg carton.
1. Four pieces—marbles, chips, or stones—are placed in each of the 12 holes. The color of the pieces is irrelevant.
1. Each player has a store (called a Mancala) to the right side of the Mancala board. (Cereal bowls work well for this purpose if you're using an egg carton.)

---

# Rules - Gameplay

1. The game begins with one player picking up all of the pieces in any one of the holes on his side.
1. Moving counter-clockwise, the player deposits one of the stones in each hole until the stones run out.
1. If you run into your own store, deposit one piece in it. If you run into your opponent's store, skip it.
1. If the last piece you drop is in your own store, you get a free turn.
1. If the last piece you drop is in an empty hole on your side, you capture that piece and any pieces in the hole directly opposite.
1. Always place all captured pieces in your store.
1. The game ends when all six spaces on one side of the Mancala board are empty.
1. The player who still has pieces on his side of the board when the game ends capture all of those pieces.
1. Count all the pieces in each store. The winner is the player with the most pieces.

---

# Where to start?

Represent both the state of the game and the rules in Python.

```
+-----+-----+-----+-----+-----+-----+-----+-----+
|     |     |     |     |     |     |     |     |
|     |  4  |  4  |  4  |  4  |  4  |  4  |     |
|     |     |     |     |     |     |     |     |
|  0  +-----+-----+-----+-----+-----+-----+  0  |
|     |     |     |     |     |     |     |     |
|     |  4  |  4  |  4  |  4  |  4  |  4  |     |
|     |     |     |     |     |     |     |     |
+-----+-----+-----+-----+-----+-----+-----+-----+
         A     B     C     D     E     F
```
In Python this is just a list:

```python
    [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0, 0]
```

---

# How indexes are mapped

```python
player = 0 if isMyTurn() else 1

gamestate = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, player]

# Board cells marked with array indexes:
# +----+----+----+----+----+----+----+----+
# |    | 12 | 11 | 10 |  9 |  8 |  7 |    |
# | 13 +----+----+----+----+----+----+  6 |
# |    |  0 |  1 |  2 |  3 |  4 |  5 |    |
# +----+----+----+----+----+----+----+----+
```

---

# AI Game Play

* Luck (pick a random legal move)
* Depth-first search (minimax algorithm, alpha-beta pruning)
* Machine Learning!

---

# Luck

This is not really an AI, but a placeholder which was trivial to implement.

```python
    moves = getLegalMoves(gamestate)
    return random.choice(moves)
```

It just picks a random move from the set of legal moves.

---

# Depth-first Search

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Depth-first-tree.svg/1200px-Depth-first-tree.svg.png" title="Depth-first search" style="width:70%; height:auto;"/>

1. Start at the root of the tree (initial board state)
2. If no children, evaluate the node and compute a score. Else evaluate each 
   child as a new tree (recursively find score)
3. After getting the scores of child nodes, choose best score to return as
   parent score.

---

# Minimax and Alpha-Beta Pruning

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/AB_pruning.svg/1212px-AB_pruning.svg.png" title="Alpha-Beta Pruning" style="width:80%; height:auto;"/>
1. Each player is trying to optimize to their own advantage.
2. The value of each state is bounded by each player's best move value at that
   position.
3. Once the upper bound of a player's value at any position is known to be
   worse than another position, no more moves in that subtree need to be
   evaluated.

---

# Limitations of Depth-First Search

Time complexity is explosive.

--

1. Prune branches which are not optimal so you don't evaluate them
   unnecessarily.
1. Use a database to remember positions you already evaluated.

--

    - A/B pruning may skip a subtree, but if opponent makes an _unexpected_ move, 
      then you may need that subtree after all. If it is not in your database
      or cache, you will need to evaluate it.

--

A pruned subtree might generate a different result at greater search depths.

--

1. Use iterative deepening to evaluate greater depths as time allows.
1. Sometimes you can evaluate better subtrees first by guessing what are good move
   candidates. This lets you prune earlier (sometimes).

--

    - An opponent using a long-term strategy may gain an advantage by planning
      more moves ahead than the search depth allows.

---

# Machine Learning

* Depth-first search is brute force
    - Takes a long time to search for best move
    - Requires faster hardware for better skill
* Neural Networks actually learn to play
    - Cost is all in training time.
    - Trained neural network requires minimal hardware.

---

# How does a Neural Network work?

A Neural Network receives a set of inputs, applies mathematical
functions to those inputs, and generates output values.

<img src="https://cdn-images-1.medium.com/max/1600/1*DW0Ccmj1hZ0OvSXi7Kz5MQ.jpeg" title="Neural Network" style="width:60%; height:auto;"/>

---

# Inputs

Recall we treated the board state as a Python list:
```python
    [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0, 0]
```

* This is an input layer with 14 neurons (12 if we omit the mancalas where we
  keep score). 
* Each neuron gets the integer count of beads in a bowl as its input.
* We rotate the board in the data structure, so the player always appears to be
  player 1.

---

# Output

The output layer indicates which move to make. 

* There can be up to 6 possible moves, each corresponding to one bowl.
* The output layer emits 6 values between 0 and 1, each representing a move.
* The highest output value indicates the chosen move.

If the chosen move is not legal (no beads in that cup) then pick the next
highest.

---

# Hidden Layers

This is where the magic happens. We can have any number of hidden layers, in
any shape. Adding more neurons increases training time, so be careful.

Shapes I have tried:

* 1 hidden layer, 128 neurons
* 2 hidden layers, 80 neurons each
* 3 hidden layers, 80 neurons each

---

# Training and Learning

* Generate Training Data
* Adversarial Training
* Retraining from History

---

# Generating Training Data

* Play thousands of games.
* Save move history of every game played.
* Saved as JSON Lines, files contain the same fields:
	- Game State
	- Selected Move
	- Who won
	- Score for each player

---

# Adversarial Training

1. Play games between two AI strategies in batches of N games each.
2. After each batch, do additional training using the games just played.

Both players learn from all the games. 

Game play should improve as the players continue playing.

---

# Learning from Repeated Training

1. Scoring of moves by outcome of game
	- Between 0 and 1
	- Illegal moves to 0
	- Move scored 1 if game was won
	- Move scored 0 (other moves 1) if game was lost

--

2. Alternate who moves first

--

3. Inject some randomness
	- A NN is deterministic
	- Needed variety of game states for training

--

4. Input encoding
	- array of bead counts
	- one-hot encoding

--

5. Back to scoring
	- Bonus for captures
	- Bonus for extra moves
	- Still scoring moves higher for game outcome
	- This basically trains a greedy algorithm into NN

---

# How do they do?

|          |    greedy|      luck|   nn1h128|    nn2h80|    nn3h80|  nnx1h128|   nnx3h80|
|:---------|---------:|---------:|---------:|---------:|---------:|---------:|---------:|
|    greedy|          |       100|       100|         0|       100|       100|       100|
|      luck|         0|          |         3|         1|         3|         5|         0|
|   nn1h128|       100|        97|          |       100|       100|       100|       100|
|    nn2h80|       100|       100|       100|          |       100|       100|       100|
|    nn3h80|       100|       100|       100|         0|          |       100|       100|
|  nnx1h128|       100|        99|       100|         0|       100|          |       100|
|   nnx3h80|       100|        99|       100|         0|       100|       100|          |

---

# Next Steps

* Convolutional Neural Networks
* Deeper networks
* Training values based on game score
* API and Mobile App
* Profit!

---

# References

* [Mancala Board on Amazon](https://www.amazon.com/Square-Root-00015-Mancala/dp/B001V9HJ1W)
* [Depth-First Search](https://en.wikipedia.org/wiki/Depth-first_search)
* [Alpha-Beta Pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)
* [About Neural Networks](https://towardsdatascience.com/machine-learning-fundamentals-ii-neural-networks-f1e7b2cb3eef)
* [Article about Mancala and AI](https://towardsdatascience.com/the-ancient-game-and-the-ai-d7704bea280d)
