# +----+----+----+----+----+----+----+----+
# |    | 12 | 11 | 10 |  9 |  8 |  7 |    |
# | 13 +----+----+----+----+----+----+  6 |
# |    |  0 |  1 |  2 |  3 |  4 |  5 |    |
# +----+----+----+----+----+----+----+----+

# state is a list, offsets for different bowls
NUM_PLAYERS = 2
PLAYER_1_CAPTURES = 6
PLAYER_1_ROW = 0
PLAYER_2_CAPTURES = 13
PLAYER_2_ROW = 7
PLAYER_TURN = 14
PLAYER_1 = 0
PLAYER_2 = 1


class InvalidMove(Exception):
    def __init___(self, state, move):
        Exception.__init__(self, "InvalidMove: " + move +
                           ' State: ' + ','.join(state))
        self.state = state
        self.move = move


class InvalidPlayer(Exception):
    def __init__(self, player):
        Exception.__init__(self, "InvalidPlayer: "+str(player))
        self.player = player


class InvalidIndex(Exception):
    def __init__(self, index):
        Exception.__init__(self, "InvalidIndex: "+str(index))
        self.index = index


def init():
    """
    Creates the game data structure for initial state of the game.

    >>> init()
    [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0, 0]
    """
    newstate = [4, 4, 4, 4, 4, 4, 0,
                4, 4, 4, 4, 4, 4, 0,
                PLAYER_1]
    return newstate


def validateIndex(index):
    """
    Is this index on the board at all?
    >>> validateIndex(4)
    4
    >>> validateIndex(-1)
    Traceback (most recent call last):
        ...
    game_state.InvalidIndex: InvalidIndex: -1
    >>> validateIndex(14)
    Traceback (most recent call last):
        ...
    game_state.InvalidIndex: InvalidIndex: 14
    """
    if index >= 0 and index < NUM_PLAYERS*7:
        return index
    else:
        raise InvalidIndex(index)


def validatePlayer(player):
    """
    Ensure player is a valid index.
    >>> validatePlayer(1)
    1
    >>> validatePlayer(2)
    Traceback (most recent call last):
        ...
    game_state.InvalidPlayer: InvalidPlayer: 2
    """
    if player >= 0 and player < NUM_PLAYERS:
        return player
    else:
        raise InvalidPlayer(player)


def getPlayerRowOffset(player):
    """
    Returns the index into the game array for the first of the player's bowls.

    >>> getPlayerRowOffset(0)
    0
    >>> getPlayerRowOffset(1)
    7
    >>> getPlayerRowOffset(2)
    Traceback (most recent call last):
        ...
    game_state.InvalidPlayer: InvalidPlayer: 2
    """
    if player < 0 or player >= NUM_PLAYERS:
        raise InvalidPlayer(player)
    offset = player*7
    return offset


def getRow(state, player):
    """
    Returns the row for the player as an array of his bowls.

    >>> getRow([1, 2, 3, 4, 5, 6, 0, \
                12, 11, 10, 9, 8, 7, 0, \
                PLAYER_1], PLAYER_1)
    [1, 2, 3, 4, 5, 6]
    """
    offset = getPlayerRowOffset(player)
    return state[offset:offset+6]


def getMaxBowls():
    """
    Returns the number of bowls in the board.
    >>> getMaxBowls()
    14
    """
    return NUM_PLAYERS*7


def getOppositeBowl(index):
    """
    Returns the index of the bowl opposite the bowl with the given index.
    >>> getOppositeBowl(3)
    9
    >>> getOppositeBowl(11)
    1
    >>> getOppositeBowl(0)
    12
    >>> getOppositeBowl(14)
    Traceback (most recent call last):
        ...
    game_state.InvalidIndex: InvalidIndex: 14
    """
    # bowl index and opposite add up to 12
    validateIndex(index)
    opposite = (PLAYER_2_CAPTURES-1-index)
    return opposite


def getBowlOwner(index):
    """
    Return ID of player who owns this bowl.
    >>> getBowlOwner(4)
    0
    >>> getBowlOwner(12)
    1
    >>> getBowlOwner(14)
    Traceback (most recent call last):
        ...
    game_state.InvalidIndex: InvalidIndex: 14
    """
    return int(validateIndex(index)/7)


def getBowlCount(state, index):
    """
    Get the number of stones in any bowl on the board.

    >>> getBowlCount([1, 2, 3, 4, 5, 6, 0, 12, 11, 10, 9, 8, 7, 0, 0], 7)
    12
    >>> getBowlCount([1, 2, 3, 4, 5, 6, 0, 12, 11, 10, 9, 8, 7, 0, 0], 14)
    Traceback (most recent call last):
        ...
    game_state.InvalidIndex: InvalidIndex: 14
    """
    return state[validateIndex(index)]


def getCurrentPlayer(state):
    """
    Get the ID of the player whose turn it is to move.

    >>> getCurrentPlayer([1, 2, 3, 4, 5, 6, 0, 12, 11, 10, 9, 8, 7, 0, 1])
    1
    >>> getCurrentPlayer([1, 2, 3, 4, 5, 6, 0, 12, 11, 10, 9, 8, 7, 0, 2])
    Traceback (most recent call last):
        ...
    game_state.InvalidPlayer: InvalidPlayer: 2
    """
    return validatePlayer(state[PLAYER_TURN])


def isLegalMove(state, move):
    """
    Determine if move is legal for given game state.

    If trying to move stones for wrong player:
    >>> isLegalMove([1, 2, 3, 4, 5, 6, 0, 12, 11, 10, 9, 8, 7, 0, 1], 2)
    False

    Legal move:
    >>> isLegalMove([1, 2, 3, 4, 5, 6, 0, 12, 11, 10, 9, 8, 7, 0, 0], 2)
    True
    """
    validateIndex(move)
    if getBowlOwner(move) != getCurrentPlayer(state):
        return False
    elif 0 == getBowlCount(state, move):
        return False
    else:
        return True


def validateMove(state, move):
    """
    Ensure move is valid for state. Raise exception if not. If valid, return a
    copy of state and move.

    >>> validateMove([1, 2, 3, 4, 5, 6, 0, 12, 11, 10, 9, 8, 7, 0, 1], 2)
    Traceback (most recent call last):
        ...
    game_state.InvalidMove: ([1, 2, 3, 4, 5, 6, 0, 12, 11, 10, ..., 1], 2)

    >>> validateMove([1, 2, 3, 4, 5, 6, 0, 12, 11, 10, 9, 8, 7, 0, 1], 8)
    ([1, 2, 3, 4, 5, 6, 0, 12, 11, 10, 9, 8, 7, 0, 1], 8)
    """
    player = getCurrentPlayer(state)
    index = validateIndex(move)
    if getBowlOwner(move) != player:
        raise InvalidMove(state, index)
    if 0 == getBowlCount(state, move):
        raise InvalidMove(state, index)
    return state[:], move


def isGameOver(state):
    """
    Return true if game is ended, else false to keep playing. Game ends when
    either player has an empty row.

    >>> isGameOver([1, 2, 3, 4, 5, 6, 0, 12, 11, 10, 9, 8, 7, 0, 1])
    False

    >>> isGameOver([0, 0, 0, 0, 0, 0, 9, 12, 11, 10, 9, 8, 7, 0, 1])
    True
    """
    for player in range(NUM_PLAYERS):
        row = getRow(state, player)
        # false if any bowl for this player has nonzero count in it
        try:
            if next(True for bowl in row if bowl > 0):
                return False
        except StopIteration:
            return True
    return True


def isMancala(index):
    """
    Test if the bowl at the given index is the mancala bowl. This is where a
    player tries to gather the stones for scoring.

    >>> isMancala(6)
    True
    >>> isMancala(13)
    True
    >>> isMancala(10)
    False
    >>> isMancala(14)
    Traceback (most recent call last):
        ...
    game_state.InvalidIndex: InvalidIndex: 14
    """
    m = (validateIndex(index) % 7 == 6)
    return m


def getMancalaIndex(player):
    """
    Get the index of the given player's mancala.

    >>> getMancalaIndex(0)
    6
    >>> getMancalaIndex(1)
    13
    >>> getMancalaIndex(2)
    Traceback (most recent call last):
        ...
    game_state.InvalidPlayer: InvalidPlayer: 2
    """
    return ((validatePlayer(player) * 7) + 6)


def scoreGame(state):
    """
    Move remaining stones to the appropriate Mancala for the endgame scoring.

    >>> scoreGame([0, 0, 0, 0, 0, 0, 9, 12, 11, 10, 9, 8, 7, 0, 1])
    [0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 57, 1]
    >>> scoreGame([0, 0, 1, 0, 0, 0, 9, 12, 11, 10, 9, 8, 7, 0, 1])
    [0, 0, 1, 0, 0, 0, 9, 12, 11, 10, 9, 8, 7, 0, 1]
    """
    if not isGameOver(state):
        return state
    newstate = ([0] * 15)[:]
    newstate[PLAYER_TURN] = state[PLAYER_TURN]
    for player in range(NUM_PLAYERS):
        mindex = getMancalaIndex(player)
        score = getBowlCount(state, mindex)
        row = getRow(state, player)
        score = sum(row, score)
        newstate[mindex] = score
    return newstate


def getWinner(gamestate):
    """
    Returns the index of the winner of the game.

    >>> getWinner([0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 57, 1])
    1
    """
    winner = -1
    score = 0
    for player in range(NUM_PLAYERS):
        c = getBowlCount(gamestate, getMancalaIndex(player))
        if c > score:
            score = c
            winner = player
    return winner


def nextPlayer(player):
    """
    Return the next player after the given player.

    >>> nextPlayer(1)
    0
    >>> nextPlayer(0)
    1
    """
    return ((validatePlayer(player)+1) % NUM_PLAYERS)


def getOpponentMancalas(player):
    """
    Get a list of indexes which are opponent Mancalas.

    >>> getOpponentMancalas(1)
    [6]
    >>> getOpponentMancalas(0)
    [13]
    """
    nxt = nextPlayer(player)
    indexes = []
    while nxt != player:
        indexes.append(getMancalaIndex(nxt))
        nxt = nextPlayer(nxt)
    return indexes


def translateMove(state, n):
    """
    This turns a selected move in the range [0,6] into a board index.

    >>> translateMove([1, 2, 3, 4, 5, 6, 0, 12, 11, 10, 9, 8, 7, 0, 0], 4)
    4
    >>> translateMove([1, 2, 3, 4, 5, 6, 0, 12, 11, 10, 9, 8, 7, 0, 1], 4)
    8
    """
    isPlayer1 = (PLAYER_1 == getCurrentPlayer(state))
    nprime = n if isPlayer1 else PLAYER_2_CAPTURES-1-n
    return nprime


def doMove(state, move):
    newstate, move = validateMove(state, move)
    player = getCurrentPlayer(newstate)
    stones = newstate[move]
    newstate[move] = 0
    skip = getOpponentMancalas(player)
    freeTurn = False
    wasEmpty = False
    nextBowl = move
    for i in range(stones):
        nextBowl = (nextBowl + 1) % getMaxBowls()
        freeTurn = False
        wasEmpty = False
        if nextBowl in skip:
            continue
        if getBowlOwner(nextBowl) == player:
            if isMancala(nextBowl):
                freeTurn = True
            else:
                if 0 == getBowlCount(newstate, nextBowl):
                    wasEmpty = True
        newstate[nextBowl] += 1  # drop a stone
    if wasEmpty:
        opposite = getOppositeBowl(nextBowl)
        captured = newstate[opposite]
        newstate[opposite] = 0
        newstate[getMancalaIndex(player)] += captured
    if not freeTurn:
        newstate[PLAYER_TURN] = nextPlayer(player)
    return scoreGame(newstate)

# TODO: for opponent, reverse board? Maybe useful for training network?
