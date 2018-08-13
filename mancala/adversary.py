import importlib
import sys
from time import process_time
import logging
from ai import luck
import random
from trainlib import setupLogFile, play_one_game

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stderr)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

results = logging.getLogger('results')
results.setLevel(logging.INFO)

BASE_PERCENT = .37


def needRandomMove(numMoves):
    pctchance = BASE_PERCENT / (numMoves + 1)
    if random.random() < pctchance:
        return True
    return False


def trainingRow(row):
    return [row['board'], row['move'], row['winner']]


def winloss(players, gps, games):
    message = "{} -- {}"
    pinfo = sorted([(p['name'], p['wins'], round(p['wins'] / games, 2))
                    for p in players])
    logger.info(
        message.format(' '.join(["{}:{}:{}".format(*p) for p in pinfo]), gps))


def play_games(plist, lucky):
    batch_size = 5000
    trainingGames = 100
    players = plist[:]
    time_sum = 0
    games = 0
    tgames = 0
    training = []
    while True:
        ts = process_time()
        players = players[::-1]
        (winner, moves) = play_one_game(players, lucky)
        training += moves
        tgames += 1
        if len(training) >= batch_size or tgames >= trainingGames:
            for p in players:
                p['ai'].train(data=training)
            training = []
            tgames = 0
        time_sum += (process_time() - ts)
        games += 1
        gps = (max(1, games) / time_sum)
        winloss(players, gps, games)


def main(name1="nn", name2="nn"):
    setupLogFile('training/' + '-'.join([name1, name2]) + '.jsonl')
    places = ['left', 'right']
    try:
        logger.info("{} vs {}! Begin!".format(name1, name2))
        players = []
        lucky = luck.AI()
        for p in [name1, name2]:
            player = {}
            player['module'] = importlib.import_module('ai.' + p)
            player['ai'] = player['module'].AI()
            player['name'] = places.pop() + '_' + p
            player['wins'] = 0
            players.append(player)
        # infinite loop here
        play_games(players, lucky)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main(*sys.argv[1:])
