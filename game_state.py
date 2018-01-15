# +----+----+----+----+----+----+----+----+
# |    | 12 | 11 | 10 |  9 |  8 |  7 |    |
# | 13 +----+----+----+----+----+----+  6 |
# |    |  0 |  1 |  2 |  3 |  4 |  5 |    |
# +----+----+----+----+----+----+----+----+

# state is a list, offsets for different bowls
PLAYER_1_CAPTURES = 6
PLAYER_1_ROW = 0
PLAYER_2_CAPTURES = 13
PLAYER_2_ROW = 7
PLAYER_TURN = 14
PLAYER_1 = 'A'
PLAYER_2 = 'B'

def init():
    return [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0, 0]
