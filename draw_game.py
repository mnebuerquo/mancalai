# just drawing stuff, no actual content here
from game_state import *

CELL_WIDTH = 5

def _drawStaticPart(filler,joiner,numslots=9):
    return (filler * CELL_WIDTH).join( [joiner] * numslots )

def _drawCellNumber(num):
    return ('{:^'+str(CELL_WIDTH)+'}').format(num)

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
    row = state[rowOffset:rowOffset+6]
    row = row if PLAYER_1_ROW==rowOffset else row[::-1]
    cells = [_drawCellNumber('')] + \
            [ _drawCellNumber(r) for r in row ] + \
            [_drawCellNumber('')]
    return ('|'+'|'.join(cells)+'|', PLAYER_1_ROW)

def drawState(state):
    scanlines = [
            drawEdge,
            drawGap, drawRow, drawGap,
            drawMiddle,
            drawGap, drawRow, drawGap,
            drawEdge
            ]
    output = []
    rowOffset = PLAYER_2_ROW
    for s in scanlines:
        line, rowOffset = s(state, rowOffset)
        output += [line]
    print("\n".join(output))
