import sys
import importlib
from random import randint
import draw_game
import game_state as s


def main(name="nn", inputfile='trainingmoves.csv'):
    ai = importlib.import_module('ai.' + name)

    player = ai.AI()

    player.train(datafile=inputfile)

    stones = 48
    state = ([0]*15)[:]
    bowl = 0
    while stones > 0:
        handful = randint(0, 4)
        state[bowl] += handful
        stones -= handful
        bowl = (bowl+1) % 14
    move = player.move(state)
    draw_game.drawState(state)
    print("player: {}".format(s.getCurrentPlayer(state)))
    print("move: {}".format(move))


if __name__ == '__main__':
    main(*sys.argv[1:])
