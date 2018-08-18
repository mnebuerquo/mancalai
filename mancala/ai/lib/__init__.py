import game_state as s
from .nn_lib import trainingStream
import random


class AiBase():

    taunts = ['Generic taunt!']

    def taunt(self):
        return random.choice(self.taunts)

    def gameOver(self, youWin):
        pass

    def train(self, data=None, datafile=None, batch_size=None):
        pass

    def move(self, state):
        moves = s.getLegalMoves(state)
        if not moves:
            raise s.NoMoves(state)
        return random.choice(moves)


class AiNNBase(AiBase):
    def __init__(self):
        super().__init__()

    def train(self, data=None, datafile=None, batch_size=None):
        if data:
            self.nn.train(data, batch_size=batch_size)
        if datafile is not None:
            with open(datafile, "r") as infile:
                self.nn.train(trainingStream(infile), batch_size=batch_size)

    def move(self, state):
        return self.nn.getMove(state)
