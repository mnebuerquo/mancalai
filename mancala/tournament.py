import game_state as s
import sys
from ai_list import makeAIList
from print_table import printTable
import logging

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


def matchups(num_players, num_epochs):
    for e in range(num_epochs):
        for i in range(num_players):
            for j in range(num_players):
                yield (i, j, e)


def play_game(*players):
    game = s.init()
    done = False
    while not done:
        player = s.getCurrentPlayer(game)
        move = players[player].move(game)
        game = s.doMove(game, move)
        done = s.isGameOver(game)
    return s.getWinner(game)


def main(numEpochs="3"):
    numEpochs = int(numEpochs)
    aiList = makeAIList()
    numPlayers = len(aiList)
    resultList = [[[0, 0, 0] for n in range(numPlayers)]
                  for m in range(numPlayers)]
    for i, j, e in matchups(numPlayers, numEpochs):
        # play game
        winner = play_game(aiList[i]['ai'], aiList[j]['ai']) + 1
        resultList[i][j][winner] += 1
    printTable(resultList, [x['name'] for x in aiList])


if __name__ == '__main__':
    main(*sys.argv[1:])
