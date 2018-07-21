import game_state as s
import importlib
import sys
import logging
from time import process_time


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
    results.info([row['board'], row['move'], row['winner']])
    # temp = "Move: {}, Gamestate: {}, Player: {}, Algorithm: {}, IsWinner: {}"
    # root.info(temp.format(move, gamestate, player, algorithm, winner))
    # root.info(json.dumps(row))


def play_game(players):
    game = s.init()
    done = False
    moves = []
    while not done:
        # do move for someone
        player = s.getCurrentPlayer(game)
        move = players[player]['ai'].move(game)
        if move is None:
            print("null move! ", game)
        mt = {
            "move": s.flipMove(move, player),
            "board": s.flipBoardCurrentPlayer(game),
            "player": player,
            "name": players[player]['module'].__name__
        }
        moves.append(mt)
        game = s.doMove(game, move)
        done = s.isGameOver(game)
    winner = s.getWinner(game)
    # make training set with move, gamestate, and 1 for win, 0 for lose
    trainingset = [dict(d, winner=int(winner == d['player'])) for d in moves]
    i = 0
    for p in players:
        p['ai'].gameOver(i == winner)
        i += 1
    return (winner, trainingset)


def play_series(players, count):
    time_sum = 0
    time_cnt = 0
    for i in range(int(count)):
        ts = process_time()
        players = players[::-1]
        (winner, moves) = play_game(players)
        for move in moves:
            logMove(move)
        time_sum += (process_time() - ts)
        time_cnt += 1
        avg = (time_sum / max(1, time_cnt))
        template = "Winner: player {} ({}) avg sec: {}"
        root.info(template.format(winner + 1, players[winner]['name'], avg))


def main(name1="luck", name2="luck", count=1, logfile='trainingmoves.csv'):
    print("{} vs {} for {} games!".format(name1, name2, count))
    setupLogFile(logfile)
    players = []
    for p in [name1, name2]:
        player = {}
        player['module'] = importlib.import_module('ai.' + p)
        player['ai'] = player['module'].AI()
        player['name'] = p
        players.append(player)

    play_series(players, count)


if __name__ == '__main__':
    main(*sys.argv[1:])
