import game_state as s
import draw_game as d
import importlib
import sys
import logging


root = logging.getLogger('root')
root.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stderr)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

results = logging.getLogger('results')
results.setLevel(logging.INFO)


def setupLogFile(filename):
    global results
    fh = logging.FileHandler(filename)
    fh.setLevel(logging.DEBUG)
    results.addHandler(fh)
    return results


def logMove(row):
    (move, gamestate, winner) = row
    results.info(list(row))
    root.info("Move: {}\nGamestate: \n{}\nIsWinner: {}".format(
        move,
        d.getStateDrawing(gamestate),
        winner))


def play_game(algorithm1, algorithm2):
    game = s.init()
    players = (algorithm1, algorithm2)
    done = False
    moves = []
    while not done:
        # do move for someone
        player = s.getCurrentPlayer(game)
        move = players[player].move(game)
        mt = (s.flipMove(move, player),
              s.flipBoard(game),
              player)
        moves.append(mt)
        game = s.doMove(game, move)
        done = s.isGameOver(game)
    winner = s.getWinner(game)
    i = 0
    for p in players:
        if i == winner:
            p.youWin()
        else:
            p.youLose()
        i += 1
    # make training set with move, gamestate, and 1 for win, 0 for lose
    trainingset = [(m, g, int(winner == p)) for m, g, p in moves]
    return (winner, trainingset)


def main(name1="luck", name2="luck", count=1, logfile='trainingmoves.csv'):
    setupLogFile(logfile)
    outputmoves = []
    player1 = importlib.import_module('ai.' + name1)
    player2 = importlib.import_module('ai.' + name2)

    for i in range(int(count)):
        players = [player1, player2]
        if i % 2 > 0:
            players = players[::-1]
        (winner, moves) = play_game(player1, player2)
        outputmoves += moves
        root.info("Winner: player{}".format(winner + 1))

    for move in outputmoves:
        logMove(move)


if __name__ == '__main__':
    main(*sys.argv[1:])
