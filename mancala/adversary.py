import game_state as s
import importlib
import sys
from time import process_time
import logging
from logging.handlers import RotatingFileHandler

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


def trainingRow(row):
    return [row['board'], row['move'], row['winner']]


def setupLogFile(filename):
    global results
    fh = RotatingFileHandler(filename, maxBytes=10000000, backupCount=100)
    fh.setLevel(logging.DEBUG)
    results.addHandler(fh)
    return results


def winloss(players, gps, games):
    message = "{} -- {}"
    pinfo = sorted([(p['name'], p['wins'], round(p['wins']/games, 2)) for p in players])
    logger.info(
        message.format(' '.join(["{}:{}:{}".format(*p) for p in pinfo]), gps))


def play_one_game(players):
    game = s.init()
    done = False
    moves = []
    while not done:
        # do move for someone
        player = s.getCurrentPlayer(game)
        move = players[player]['ai'].move(game)
        if move is None:
            logger.error("null move! ", game)
        mt = [s.flipBoardCurrentPlayer(game), s.flipMove(move, player), player]
        moves.append(mt)
        game = s.doMove(game, move)
        done = s.isGameOver(game)
    winner = s.getWinner(game)
    score = s.getScore(game)
    # make training set with move, gamestate, and 1 for win, 0 for lose
    trainingset = [d[0:2] + [int(winner == d[2])] + list(score)[::1 - d[2] * 2]
                   for d in moves]
    for move in trainingset:
        results.info(move)
    i = 0
    for p in players:
        isWinner = (1 if i == winner else 0)
        p['ai'].gameOver(isWinner)
        p['wins'] += isWinner
        i += 1
    return (winner, trainingset)


def play_games(plist):
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
        (winner, moves) = play_one_game(players)
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
        for p in [name1, name2]:
            player = {}
            player['module'] = importlib.import_module('ai.' + p)
            player['ai'] = player['module'].AI()
            player['name'] = places.pop() + '_' + p
            player['wins'] = 0
            players.append(player)
        # infinite loop here
        play_games(players)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main(*sys.argv[1:])
