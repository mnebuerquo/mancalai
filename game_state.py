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
    def __init___(self,state,move):
        Exception.__init__(self,"InvalidMove: "+move+ \
                ' State: '+','.join(state))
        self.state = state
        self.move = move

class InvalidPlayer(Exception):
    def __init__(self,player):
        Exception.__init__(self,"InvalidPlayer: "+player)
        self.player = player

class InvalidIndex(Exception):
    def __init__(self,index):
        Exception.__init__(self,"InvalidIndex: "+index)
        self.index = index

def init():
    newstate = [4, 4, 4, 4, 4, 4, 0,
            4, 4, 4, 4, 4, 4, 0,
            PLAYER_1]
    return newstate

def getPlayerRowOffset(player):
    if player<0 or player>=NUM_PLAYERS:
        raise InvalidPlayer(player)
    offset = player*7
    return offset

def getRow(state, player):
    offset = getPlayerRowOffset(player)
    return state[offset:offset+6]

def getPlayerRowIndexes(player):
    offset = getPlayerRowOffset(player)
    return range(offset:offset+6)

def getOppositeBowl(index):
    # bowl index and opposite add up to 12
    opposite = (PLAYER_2_CAPTURES-1-index) if \
            index<PLAYER_2_CAPTURES and index>=0 and \
            index!=PLAYER_1_CAPTURES \
            else None
    return opposite

def getBowlOwner(index):
    if index>=(NUM_PLAYERS*7):
        raise InvalidIndex(index)
    return index/7

def getBowlCount(state, index):
    if index>=(NUM_PLAYERS*7):
        raise InvalidIndex(index)
    return state[index]

def getCurrentPlayer(state):
    return state[PLAYER_TURN]

def isLegalMove(state, move):
    if getBowlOwner(move)!=getCurrentPlayer(state):
        return False
    elif 0==getBowlCount(state, move):
        return False
    else
        return True

def isGameOver(state):
    for player in [PLAYER_1, PLAYER_2]:
        row = getRow(state, player)
        if next(True for bowl in row if bowl>0):
            return false
    return True

def isMancala(index):
    if index>=(NUM_PLAYERS*7):
        raise InvalidIndex(index)
    m = (index%7==6)
    return m

def getMancalaIndex(player):
    if player==PLAYER_1:
        return PLAYER_1_CAPTURES
    elif player==PLAYER_2:
        return PLAYER_2_CAPTURES
    else:
        return None

def scoreGame(state):
    if not isGameOver(state):
        return state
    newstate = [0] * 15
    newstate[PLAYER_TURN] = state[PLAYER_TURN]
    for player in [PLAYER_1, PLAYER_2]:
        mindex = getMancalaIndex(player)
        score = state[mindex]
        row = getRow(state, player)
        score = sum(row, score)
        newstate[mindex] = score
    return newstate

def nextPlayer(player):
    return ((player+1) % NUM_PLAYERS)

def getOpponentMancalas(player):
    nxt = nextPlayer(player)
    indexes = []
    while nxt != player:
        indexes.append(getMancalaIndex(nxt))
        nxt = nextPlayer(nxt)
    return indexes

def doMove(state, move):
    if not isLegalMove(state, move):
        raise InvalidMove(state,move)
    newstate = state[:]
    player = getCurrentPlayer(newstate)
    stones = newstate[move]
    skip = getOpponentMancalas(player)
    freeTurn = false
    wasEmpty = false
    nextBowl = move
    for i in range(stones):
        nextBowl+=1
        freeTurn = False
        wasEmpty = False
        if nextBowl in skip:
            continue
        if getBowlOwner(nextBowl)==player
            if isMancala(nextBowl):
                freeTurn = True
            else:
                if 0==getBowlCount(newstate, nextBowl):
                    wasEmpty = True
        newstate[nextBowl]+=1 # drop a stone
    if wasEmpty:
        opposite = getOppositeBowl(nextBowl)
        captured = newstate[opposite]
        newstate[opposite] = 0
        newstate[nextBowl]+=captured
    if not freeTurn:
        newstate[PLAYER_TURN] = nextPlayer(player)
    return scoreGame(newstate)

#TODO: for opponent, reverse board? Maybe useful for training network?
