import gamestate as s
import random


def move(state):
    moves = getLegalMoves(state)
    if not moves:
        raise s.NoMoves
    return random.choice(moves)
