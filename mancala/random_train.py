from ai_list import makeAIList
from ai import luck
from random import randrange
from trainlib import setupLogFile, play_one_game
from time import process_time
from print_table import printTable
import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stderr)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

NUM_BATCHES = 2
BATCH_SIZE = 10000
MAX_MOVES = NUM_BATCHES * BATCH_SIZE - 25
MAX_GAMES = MAX_MOVES / 20


def timeIt():
    startTime = process_time()
    while True:
        endTime = process_time()
        delta = endTime - startTime
        yield delta
        startTime = endTime


def resultsInit(numPlayers):
    return [[[0, 0, 0] for n in range(numPlayers)] for m in range(numPlayers)]


training_moves = []
training_games = 0
training_timer = timeIt()
games_start = timeIt()
batch_results = None


def saveMoves(aiList, moves):
    global training_moves
    global training_games
    global batch_results
    numPlayers = len(aiList)
    msg = "Played {} moves in {} games in {} seconds."
    max_moves = MAX_MOVES
    max_games = MAX_GAMES
    training_moves += moves
    numMoves = len(training_moves)
    training_games += 1
    if numMoves >= max_moves or training_games >= max_games:
        printTable(batch_results, [x['name'] for x in aiList])
        games_delta = next(games_start)
        sec = int(games_delta * 1000) / 1000
        logger.info(msg.format(numMoves, training_games, sec))
        next(training_timer)
        for p in aiList:
            p['ai'].train(data=training_moves, batch_size=BATCH_SIZE)
        train_delta = next(training_timer)
        sec = int(train_delta * 1000) / 1000
        logger.debug("Training done in {} sec".format(sec))
        training_moves = []
        training_games = 0
        batch_results = resultsInit(numPlayers)
        games_delta = next(games_start)


def main(args):
    global batch_results
    setupLogFile('training/random.jsonl')
    aiList = makeAIList(args)
    numPlayers = len(aiList)
    resultList = resultsInit(numPlayers)
    batch_results = resultsInit(numPlayers)
    lucky = luck.AI()
    try:
        while True:
            i = randrange(numPlayers)
            j = randrange(numPlayers)
            if i == j:
                continue
            # play game
            players = [aiList[i], aiList[j]]
            (winner, moves) = play_one_game(players, lucky)
            saveMoves(aiList, moves)
            resultList[i][j][winner + 1] += 1
            batch_results[i][j][winner + 1] += 1
    except KeyboardInterrupt:
        printTable(resultList, [x['name'] for x in aiList])


if __name__ == '__main__':
    main(sys.argv[1:])
