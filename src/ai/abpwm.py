from . import AiBase
import game_state as s
import random


def genMoves(state, movecount=0, chain=[]):
    """
    List possible moves. Moves are a list of moves, because some moves
    result in the player getting to move again.
    >>> genMoves([1, 2, 4, 4, 5, 6, 0, 12, 11, 10, 9, 8, 7, 0, 0])
    ([[0], [1], [2, 0], [2, 1], [2, 3], [2, 4], [2, 5], [3], [4], [5]], 11)
    """
    player = s.getCurrentPlayer(state)
    new = s.getLegalMoves(state)
    result = []
    for m in new:
        movecount += 1
        newstate = s.doMove(state, m)
        if player == s.getCurrentPlayer(newstate):
            r, movecount = genMoves(newstate, movecount, chain + [m])
            result = result + r
        else:
            result.append(chain + [m])
    return (result, movecount)


def score(state):
    """
    Return a numeric score for a board position.
    >>> score([1, 2, 4, 4, 5, 6, 0, 12, 11, 10, 9, 8, 7, 0, 0])
    35
    """
    score = 0
    for p in range(s.NUM_PLAYERS):
        row = s.getRow(state, p)
        rcnt = 0
        for b in row:
            rcnt += b
        cnt = s.getBowlCount(state, s.getMancalaIndex(p))
        if p == s.getCurrentPlayer(state):
            score -= cnt
            score -= rcnt
        else:
            score += cnt
            score += rcnt
    return score


def applyMove(node, moveseq):
    """
    >>> state = [1, 2, 4, 4, 5, 6, 0, 12, 11, 10, 9, 8, 7, 0, 0]
    >>> applyMove(state, [2, 3])
    [1, 2, 0, 0, 7, 8, 2, 13, 12, 10, 9, 8, 7, 0, 1]
    """
    child = node[:]
    for move in moveseq:
        child = s.doMove(child, move)
    return child


def alphaBeta(node, alpha=-9999, beta=9999, maximizingPlayer=True,
              meta=(0, 0), depth=0, maxdepth=2):
    """
    Do minimax with alpha-beta pruning. Returns the best score and move.
    >>> state = [1, 2, 4, 4, 5, 6, 0, 12, 11, 10, 9, 8, 7, 0, 0]
    >>> alphaBeta(state)
    (34, [2, 5], (41, 286))
    """
    (nodecount, movecount) = meta
    (children, movecount) = genMoves(node, movecount)
    meta = (nodecount + 1, movecount)
    bestMove = []
    if len(children) == 0 or depth >= maxdepth:
        return (score(node), bestMove, meta)
    elif maximizingPlayer:
        bestValue = alpha
        for moveseq in children:
            child = applyMove(node, moveseq)
            cvalue, ccm, meta = alphaBeta(child, bestValue, beta, False,
                                          meta, depth + 1, maxdepth)
            if cvalue > bestValue:
                bestValue = cvalue
                bestMove = moveseq
            if beta <= bestValue:
                break
    else:
        bestValue = beta
        for moveseq in children:
            child = applyMove(node, moveseq)
            cvalue, ccm, meta = alphaBeta(child, alpha, bestValue, True,
                                          meta, depth + 1, maxdepth)
            if cvalue < bestValue:
                bestValue = cvalue
                bestMove = moveseq
            if bestValue <= alpha:
                break
    return (bestValue, bestMove, meta)


def iterativeDeepening(state, movelimit, nodelimit):
    """
    Keep searching to find best move path, increasing search depth every
    iteration. Stop after evaluating too many moves or nodes.
    >>> state = [1, 2, 4, 4, 5, 6, 0, 12, 11, 10, 9, 8, 7, 0, 0]
    >>> iterativeDeepening(state, 100, 400)
    2
    """
    nodecount = 0
    movecount = 0
    maxdepth = 1
    bestMove = None
    ladder = {}
    while nodecount < nodelimit and movecount < movelimit:
        v, move, meta = alphaBeta(state, -9999, +9999, True,
                                  (nodecount, movecount), 0, maxdepth)
        (nodecount, movecount) = meta
        bestMove = move[0] if move else bestMove
        ladder[maxdepth] = (bestMove, nodecount, movecount)
        maxdepth += 1
    return bestMove


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
        return iterativeDeepening(state, 50000, 500000)
