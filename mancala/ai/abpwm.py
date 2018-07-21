import json
from . import AiBase
import game_state as s
import datetime
import movedb


def testMetaSeconds(meta, limit=None):
    timelimit = limit or meta[7]
    if timelimit is None:
        return True
    end = datetime.datetime.now()
    elapsed = end - meta[5]
    return elapsed < datetime.timedelta(seconds=timelimit)


def incMeta(meta=None, nodecount=0, movecount=0,
            pruned=0, recalled=0, stored=0, end=None,
            timelimit=None):
    """
    >>> incMeta()
    (0, 0, 0, 0, 0, ..., None)
    """
    if meta is None:
        meta = (0, 0, 0, 0, 0, datetime.datetime.now(), None, timelimit)
    return (meta[0] + nodecount, meta[1] + movecount,
            meta[2] + recalled, meta[3] + stored,
            meta[4] + pruned,
            meta[5],
            end or meta[6],
            timelimit or meta[7])


def serializeMeta(meta):
    return {
            "nodecount": meta[0],
            "movecount": meta[1],
            "recalled": meta[2],
            "stored": meta[3],
            "pruned": meta[4],
            }


def genMoves(state, chain=[]):
    """
    List possible moves. Moves are a list of moves, because some moves
    result in the player getting to move again.
    >>> genMoves([1, 2, 4, 4, 5, 6, 0, 12, 11, 10, 9, 8, 7, 0, 0])
    ([[0], [1], [2, 0], [2, 1], [2, 3], [2, 4], [2, 5], [3], [4], [5]], 11)
    >>> genMoves([0, 2, 0, 0, 1, 5, 17, 0, 0, 0, 0, 0, 1, 20, 1])
    ([[12]], 1)
    """
    movecount = 0
    player = s.getCurrentPlayer(state)
    new = s.getLegalMoves(state)
    if len(new) == 0:
        # no legal moves, so game is over: return move chain so far
        result = [chain] if len(chain) > 0 else []
    else:
        result = []
        for m in new:
            movecount += 1
            newstate = s.doMove(state, m)
            currentChain = chain + [m]
            if player == s.getCurrentPlayer(newstate):
                # still our move after move m, so recurse and grow the chain
                r, moves = genMoves(newstate, currentChain)
                movecount = movecount + moves
                # r is list of move chains we generated, so merge lists
                result = result + r
            else:
                # no more moves in this chain, add it to result list
                result = result + [currentChain]
    return (result, movecount)


def computeScore(state):
    """
    Return a numeric score for a board position.
    >>> computeScore([1, 2, 4, 4, 5, 6, 0, 12, 11, 10, 9, 8, 7, 0, 0])
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
            score -= cnt * 2
            score -= rcnt
        else:
            score += cnt * 2
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
              meta=incMeta(), depth=0, maxdepth=2):
    """
    Do minimax with alpha-beta pruning. Returns the best score and move.
    >>> state = [1, 2, 4, 4, 5, 6, 0, 12, 11, 10, 9, 8, 7, 0, 0]
    >>> alphaBeta(state)
    (33, [2, 5], (41, 286, ...))
    """
    (scoreDepth, score, bestMove) = movedb.recallState(node) or (-1000, 0, [])
    if depth + scoreDepth >= maxdepth:
        return (score, bestMove, incMeta(meta, recalled=1))
    (children, moves) = genMoves(node)
    meta = incMeta(meta, nodecount=1, movecount=moves)
    bestMove = []
    if len(children) == 0 or depth >= maxdepth:
        return (computeScore(node), bestMove, meta)
    if not testMetaSeconds(meta):
        meta = incMeta(meta, end=datetime.datetime.now())
        return (computeScore(node), bestMove, meta)
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
                meta = incMeta(meta, pruned=1)
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
                meta = incMeta(meta, pruned=1)
                break
    meta = incMeta(meta, stored=1)
    movedb.memorizeState(node, maxdepth-depth, bestValue, bestMove)
    return (bestValue, bestMove, meta)


def oneDepth(state, meta, maxdepth, bestMove, ladder):
    v, move, meta = alphaBeta(state, -9999, +9999, True,
                              meta, 0, maxdepth)
    bestMove = move[0] if move else bestMove
    ladder[maxdepth] = (bestMove, serializeMeta(meta))
    return (bestMove, meta, maxdepth + 1, ladder)


def iterativeDeepening(state, movelimit, nodelimit):
    """
    Keep searching to find best move path, increasing search depth every
    iteration. Stop after evaluating too many moves or nodes.
    >>> state = [1, 2, 4, 4, 5, 6, 0, 12, 11, 10, 9, 8, 7, 0, 0]
    >>> iterativeDeepening(state, 200, 800)[0]
    2
    """
    maxdepth = 1
    bestMove = None
    ladder = {}
    meta = incMeta()
    while meta[0] < nodelimit and meta[1] < movelimit and maxdepth <= 10:
        (bestMove, meta, maxdepth, ladder) = oneDepth(
                state, meta, maxdepth, bestMove, ladder)
    return (bestMove, ladder)


def timedIterativeDeepening(state, timelimit):
    maxdepth = 1
    bestMove = None
    ladder = {}
    meta = incMeta(timelimit=timelimit)
    while testMetaSeconds(meta):
        (bestMove, meta, maxdepth, ladder) = oneDepth(
                state, meta, maxdepth, bestMove, ladder)
    return (bestMove, ladder)


class AI(AiBase):

    taunts = [
        "You're such a beta.",
        "Prepare to get pruned.",
        "This is a losing branch for you.",
    ]

    def __init__(self):
        global database
        try:
            movedb.loadMoveDB()
        except Exception as e:
            print(e)
            pass

    def move(self, state):
        # (bestMove, ladder) = iterativeDeepening(state, 50000, 500000)
        (bestMove, ladder) = timedIterativeDeepening(state, 6)
        return bestMove

    def gameOver(self, youWin):
        movedb.saveMoveDB()
