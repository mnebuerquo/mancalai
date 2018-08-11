from .lib import AiBase
from .lib.move_scoring import moveToVector
import game_state as s


class AI(AiBase):

    taunts = [
        "I want all the beads.",
        "I'm going to win it all.",
        "Oops. I did it again.",
        "You're on the ropes now.",
        "I've got you right where I want you.",
    ]

    def move(self, state):
        # rotate the board for current player
        player = s.getCurrentPlayer(state)
        if player != 0:
            flip = True
            board = s.flipBoard(state)
        else:
            flip = False
            board = state

        # pick best move
        vector = moveToVector(board)
        bestmove = None
        bestscore = 0
        for i in range(6):
            move = 5 - i
            if vector[move] > bestscore:
                bestmove = move
                bestscore = vector[move]

        # flip move
        if flip:
            bestmove = s.flipMove(bestmove, player)
        return bestmove
