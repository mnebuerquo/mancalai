import game_state as s

BETTER_MOVE = 0.5
WINNING_MOVE = 1
LOSING_MOVE = 0


def losingVector(m):
    """
    Return vector of moves with losing move score set low, and others higher.
    >>> losingVector(3) == [BETTER_MOVE, BETTER_MOVE, BETTER_MOVE, \
                            LOSING_MOVE, BETTER_MOVE, BETTER_MOVE]
    True
    >>> losingVector(1) == [BETTER_MOVE, LOSING_MOVE, BETTER_MOVE, \
                            BETTER_MOVE, BETTER_MOVE, BETTER_MOVE]
    True
    """
    z = [BETTER_MOVE] * 6
    return z[:m] + [LOSING_MOVE] + z[m + 1:]


def winningVector(m):
    """
    Return vector of moves with winning move score set high, and others low.
    >>> winningVector(3) == [LOSING_MOVE, LOSING_MOVE, LOSING_MOVE, \
                            WINNING_MOVE, LOSING_MOVE, LOSING_MOVE]
    True
    >>> winningVector(1) == [LOSING_MOVE, WINNING_MOVE, LOSING_MOVE, \
                            LOSING_MOVE, LOSING_MOVE, LOSING_MOVE]
    True
    """
    z = [LOSING_MOVE] * 6
    return z[:m] + [WINNING_MOVE] + z[m + 1:]


def legalVector(state, vector):
    """
    >>> state = [1, 2, 3, 0, 5, 6, 0, 12, 11, 10, 9, 8, 7, 0, 0]
    >>> expected = [WINNING_MOVE, WINNING_MOVE, WINNING_MOVE, \
            LOSING_MOVE, WINNING_MOVE, WINNING_MOVE]
    >>> legalVector(state, [WINNING_MOVE]*6) == expected
    True
    """
    return [vector[m] if s.isLegalMove(
        state, m) else LOSING_MOVE for m in range(6)]


def moveToVector(state, m, iswinner, myscore=None, oppscore=None):
    """
    Create a vector of scores for winning moves and losing moves. Treat any
    illegal move as a losing move.

    >>> state = [1, 2, 3, 4, 5, 6, 0, 12, 11, 10, 9, 8, 7, 0, 0]
    >>> moveToVector(state, 0, 1) == [WINNING_MOVE, LOSING_MOVE, LOSING_MOVE, \
                            LOSING_MOVE, LOSING_MOVE, LOSING_MOVE]
    True
    >>> state = [1, 2, 3, 0, 5, 6, 0, 12, 11, 10, 9, 8, 7, 0, 0]
    >>> moveToVector(state, 2, 0) == [BETTER_MOVE, BETTER_MOVE, LOSING_MOVE, \
                            LOSING_MOVE, BETTER_MOVE, BETTER_MOVE]
    True
    """
    vector = winningVector(m) if iswinner else losingVector(m)
    if myscore is None or oppscore is None:
        ratio = 1
    else:
        ratio = myscore / s.MAX_BEADS
    return legalVector(state, [ratio * x for x in vector])
