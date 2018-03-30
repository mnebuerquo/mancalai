import game_state as s
import random


class AiBase():

    taunts = [ 'Generic taunt!' ]

    def taunt(self):
        return random.choice(taunts)


    def youWin(self):
        pass


    def youLose(self):
        pass


    def train(self, data=None, datafile=None):
        pass


    def move(self, state):
        moves = s.getLegalMoves(state)
        if not moves:
            raise s.NoMoves(state)
        return random.choice(moves)

