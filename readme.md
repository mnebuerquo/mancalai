# Mancala AI Experiment

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

Coming soon. First game rules, then training an AI to play.
