from . import AiBase
import game_state as s
import random


class Meta():
    nodecount = 0
    movecount = 0

    def countNode(self):
        self.nodecount += 1

    def countMove(self):
        self.movecount += 1


def genMoves(state, movecount=0, chain=[]):
    """
    List possible moves. Moves are a list of moves, because some moves
    result in the player getting to move again.
    >>> genMoves([1, 2, 4, 4, 5, 6, 0, 12, 11, 10, 9, 8, 7, 0, 0])
    ([[0], [1], [[2, 0], [2, 1], [2, 3], [2, 4], [2, 5]], [3], [4], [5]], 11)
    """
    player = s.getCurrentPlayer(state)
    new = s.getLegalMoves(state)
    result = []
    for m in new:
        movecount += 1
        newstate = s.doMove(state, m)
        if player == s.getCurrentPlayer(newstate):
            r, movecount = genMoves(newstate, movecount, chain + [m])
            result.append(r)
        else:
            result.append(chain + [m])
    return (result, movecount)


def score(state):
    return 5


def alphaBeta(node, alpha, beta, maximizingPlayer, meta, depth, maxdepth):
    children = genMoves(node)
    if len(children) == 0 or depth >= maxdepth:
        meta.countNode()
        return (score(node), meta)
    elif maximizingPlayer:
        bestValue = alpha
        for move in children:
            child = node
            for m in move:
                child = s.doMove(child, m)
            cvalue = alphaBeta(child, bestValue, beta, False,
                               meta, depth + 1, maxdepth)
            bestValue = max(bestValue, cvalue)
            if beta <= bestValue:
                break
    else:
        bestValue = beta
        for move in children:
            child = node
            for m in move:
                child = s.doMove(child, m)
            cvalue = alphaBeta(child, alpha, bestValue, True,
                               meta, depth + 1, maxdepth)
            bestValue = min(bestValue, cvalue)
            if bestValue <= alpha:
                break
    return bestValue


class AI(AiBase):

    taunts = [
        "You're such a beta.",
        "Prepare to get pruned.",
        "This is a losing branch for you.",
    ]

    def __init__(self):
        # TODO: load dictionary of visited moves
        pass

    def move(self, state):
        moves = s.getLegalMoves(state)
        if not moves:
            raise s.NoMoves(state)
        return random.choice(moves)
