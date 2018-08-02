# Playing Mancala using Tensorflow
<img src="https://images-na.ssl-images-amazon.com/images/I/81Y6ZP4rQWL._SL1500_.jpg" title="Photo of Mancala board" style="width:80%; height:auto;"/>

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

# AI Game Play

* Luck (pick a random legal move)
* Depth-first search (minimax algorithm, alpha-beta pruning)
* Machine Learning!

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

# Tricks and Problems with Depth-First Search

* Time complexity is explosive.

--

1. Prune branches which are not optimal so you don't evaluate them
   unnecessarily.
1. Use a database to remember positions you already evaluated.

--

    - A/B pruning may skip a subtree, but if opponent makes an _unexpected_ move, 
      then you may need that subtree after all. If it is not in your database
      or cache, you will need to evaluate it.

--

* A pruned subtree might generate a different result at greater search depth.

--

1. Use iterative deepening to evaluate greater depths as time allows.
1. Sometimes you can evaluate better subtrees first by guessing what are good move
   candidates. This lets you prune earlier (sometimes).

--

    - An opponent using a long-term strategy may gain an advantage by planning
      more moves ahead than the search depth allows.

---


