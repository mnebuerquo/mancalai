# just drawing stuff, no actual content here
import game_state as gs

CELL_WIDTH = 5


def _staticPart(filler, joiner, numslots=9):
    return (filler * CELL_WIDTH).join([joiner] * numslots)


def _cellNumber(num):
    return ('{:^' + str(CELL_WIDTH) + '}').format(num)


def _boardEdge(state, row):
    return (_staticPart('-', '+'), row)


def _boardGap(state, row):
    return (_staticPart(' ', '|'), row)


def _boardMiddle(state, row):
    ret = ('|' +
           _cellNumber(state[gs.PLAYER_2_CAPTURES]) +
           _staticPart('-', '+', 7) +
           _cellNumber(state[gs.PLAYER_1_CAPTURES]) +
           '|', row)
    return ret


def _boardRow(state, rowOffset):
    row = state[rowOffset:rowOffset + 6]
    # reverses player 2
    row = row if gs.PLAYER_1_ROW == rowOffset else row[::-1]
    cells = [_cellNumber('')] + \
            [_cellNumber(r) for r in row] + \
            [_cellNumber('')]
    return ('|' + '|'.join(cells) + '|', gs.PLAYER_1_ROW)


def getStateDrawing(state):
    scanlines = [
        _boardEdge,
        _boardGap, _boardRow, _boardGap,
        _boardMiddle,
        _boardGap, _boardRow, _boardGap,
        _boardEdge
    ]
    output = []
    rowOffset = gs.PLAYER_2_ROW
    for s in scanlines:
        line, rowOffset = s(state, rowOffset)
        output += [line]
    return "\n".join(output)


def drawState(state):
    print(getStateDrawing(state))


def getCommandOptionsLine():
    opts = ['', 'A', 'B', 'C', 'D', 'E', 'F', '']
    return ' ' + ' '.join([_cellNumber(x) for x in opts]) + ' '


def drawCommandOptions():
    print(getCommandOptionsLine())
