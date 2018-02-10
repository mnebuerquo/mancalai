import game_state as s
import importlib
import sys


def play_game(algorithm1, algorithm2):
    game = s.init()
    players = (algorithm1, algorithm2)
    done = False
    while not done:
        # do move for someone
        player = s.getCurrentPlayer(game)
        move = players[player].move(game)
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
    return winner


def main(name1, name2, count=1):
    player1 = importlib.import_module('ai.'+name1)
    player2 = importlib.import_module('ai.'+name2)
    for i in range(int(count)):
        players = [player1, player2]
        if i % 2 > 0:
            players = players[::-1]
        winner = play_game(player1, player2)
        print("Winner: player{}".format(winner+1))


if __name__ == '__main__':
    main(*sys.argv[1:])
