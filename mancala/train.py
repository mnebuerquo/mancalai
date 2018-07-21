import sys
import importlib
import draw_game
import game_state as s


def main(name="nn", inputfile='trainingmoves.csv'):
    ai = importlib.import_module('ai.' + name)

    player = ai.AI()

    player.train(datafile=inputfile)

    state = s.randomState()
    move = player.move(state)
    draw_game.drawState(state)
    print("player: {}".format(s.getCurrentPlayer(state)))
    print("move: {}".format(move))


if __name__ == '__main__':
    main(*sys.argv[1:])
