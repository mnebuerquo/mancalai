import game_state as s

SCORE_MOVE_AGAIN = 1
SCORE_CAPTURE = 1
SCORE_LOSER_MOVE = 1
SCORE_WINNER_MOVE = 1


def legalVector(state, vector, illegalScore=0):
    """
    >>> state = [1, 2, 3, 0, 5, 6, 0, 12, 11, 10, 9, 8, 7, 0, 0]
    >>> expected = [1, 1, 1, 0.5, 1, 1]
    >>> legalVector(state, [1]*6, 0.5) == expected
    True
    """
    return [vector[m] if s.isLegalMove(
        state, m) else illegalScore for m in range(6)]


def normalizeVector(vector):
    """
    >>> normalizeVector([2, 0, 2, 4, 0, 4])
    [0.5, 0.0, 0.5, 1.0, 0.0, 1.0]
    """
    mx = max(1, max(vector))
    return [x / mx for x in vector]


def moveToVector(state, m, isWinner, myscore=None, oppscore=None):
    """
    Create a vector of scores for winning moves and losing moves. Treat any
    illegal move as a losing move.

    >>> state = [1, 2, 3, 4, 5, 6, 0, 12, 11, 10, 9, 8, 7, 0, 0]
    >>> moveToVector(state, 0, 1) == [1.0, 0.5, 0.5, 1.0, 1.0, 1.0]
    True

    >>> state = [1, 2, 3, 0, 5, 6, 0, 12, 11, 7, 9, 8, 7, 0, 0]
    >>> moveToVector(state, 2, 0) == [0.125, 1.0, 0.0, 0.0, 0.25, 0.25]
    True
    """
    score_now = s.getScore(state)
    vector = ([0] * 6)[:]
    for move in range(6):
        if s.isLegalMove(state, move):
            # legal, so start at 1
            vector[move] = 1
            newstate = s.doMove(state, move)
            score_new = s.getScore(newstate)
            if s.getCurrentPlayer(newstate) == s.getCurrentPlayer(state):
                vector[move] += SCORE_MOVE_AGAIN
            vector[move] += SCORE_CAPTURE * (score_new[0] - score_now[0])
            if move == m:
                if isWinner:
                    vector[move] += SCORE_WINNER_MOVE
                else:
                    vector[move] -= SCORE_LOSER_MOVE
        else:
            # illegal, always zero
            vector[move] = 0
        vector[move] = max(0, vector[move])
    return normalizeVector(vector)
