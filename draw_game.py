# just drawing stuff, no actual content here
from game_state import *

def _drawStaticPart(filler,joiner,numslots=9):
    return (filler * 5).join( [joiner] * numslots )

def _drawCellNumber(num):
    return '{:^5}'.format(num)

def drawEdge(state, row):
    return (_drawStaticPart('-','+'), row)

def drawGap(state, row):
    return (_drawStaticPart(' ','+'), row)

def drawMiddle(state, row):
    return ('|' +
            _drawCellNumber(state[PLAYER_2_CAPTURES]) +
            _drawStaticPart('-','+',7) +
            _drawCellNumber(state[PLAYER_1_CAPTURES]) +
            '|', row)

def drawRow(state, rowOffset):
    cells = [_drawCellNumber('')] + \
            [ _drawCellNumber(state[i]) for i in range(rowOffset, rowOffset+6) ] + \
            [_drawCellNumber('')]
    return ('|'+'|'.join(cells)+'|', PLAYER_2_ROW)

def drawState(state):
    scanlines = [
            drawEdge,
            drawGap, drawRow, drawGap,
            drawMiddle,
            drawGap, drawRow, drawGap,
            drawEdge
            ]
    output = []
    rowOffset = PLAYER_1_ROW
    for s in scanlines:
        line, rowOffset = s(state, rowOffset)
        output += [line]
    print("\n".join(output))
