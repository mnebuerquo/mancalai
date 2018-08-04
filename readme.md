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
