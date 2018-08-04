import sys
import glob
import importlib
import draw_game
import game_state as s
import logging
from random import shuffle
from timeit import default_timer as timer
import time

logger = logging.getLogger(__name__)
ch = logging.StreamHandler(sys.stderr)
logger.addHandler(ch)


def trainFile(player, filename):
    print("training {} with {}".format(player.nn.name, filename))
    player.train(datafile=filename)


def oldmain(name="nn", inputfile='trainingmoves.csv'):
    ai = importlib.import_module('ai.' + name)

    player = ai.AI()

    player.train(datafile=inputfile)

    state = s.randomState()
    move = player.move(state)
    draw_game.drawState(state)
    print("player: {}".format(s.getCurrentPlayer(state)))
    print("move: {}".format(move))


def main(name="nn", directory="training"):
    message = "epoch {}: completed {} / {} files | remaining for epoch {}"
    ai = importlib.import_module('ai.' + name)
    player = ai.AI()
    files = glob.glob(directory + '/*.jsonl*')
    # We will do epochs by replaying all the files instead of replaying each
    # batch in training. That way we get through all the files faster.
    player.nn.epochs = 1
    player.nn.batch_size = 50000
    for epoch in range(50):
        shuffle(files)
        total = len(files)
        done = 0
        start = timer()
        for f in files:
            trainFile(player, f)
            done += 1
            end = timer()
            remaining = 0
            if total > 0 and done > 0:
                pctdone = done / total
                elapsed = end - start
                est_total_time = elapsed / pctdone
                remaining = est_total_time - elapsed
                timestr = time.strftime('%H:%M:%S', time.gmtime(remaining))
            print(message.format(epoch, done, total, timestr))


if __name__ == '__main__':
    main(*sys.argv[1:])
