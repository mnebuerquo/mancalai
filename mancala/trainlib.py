import random
import game_state as s
import logging
from logging.handlers import RotatingFileHandler
logger = logging.getLogger(__name__)

results = logging.getLogger('results')

BASE_PERCENT = .25


def setupLogFile(filename):
    global results
    fh = RotatingFileHandler(filename, maxBytes=10000000, backupCount=100)
    fh.setLevel(logging.DEBUG)
    results.addHandler(fh)
    results.propagate = False
    return results


def needRandomMove(numMoves):
    pctchance = BASE_PERCENT / (numMoves + 1)
    if random.random() < pctchance:
        return True
    return False


def play_one_game(players, lucky):
    global results
    game = s.init()
    done = False
    moves = []
    while not done:
        # do move for someone
        player = s.getCurrentPlayer(game)
        if needRandomMove(len(moves)):
            move = lucky.move(game)
        else:
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
