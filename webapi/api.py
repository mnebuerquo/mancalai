import os
from apistar import App, Route
from mancala import game_state

LISTEN_ADDR = os.environ.get('LISTEN_ADDR', '127.0.0.1')
LISTEN_PORT = int(os.environ.get('LISTEN_PORT', '5000'))
USE_DEBUGGER = True if os.environ.get('DEBUG') == "True" else False


def welcome() -> str:
    return 'Welcome to Mancala'


def gameNew(player1:str='human', player2:str='random') -> dict:
    return {
        'gameState': game_state.init()
    }


def gameList() -> dict:
    return {}


def gameGetState(gameid: str) -> dict:
    return {}


def gameMakeMove(gameid: str) -> dict:
    return {}


def gameWaitForAI(gameid: str) -> dict:
    return {}


routes = [
    Route('/', method='GET', handler=welcome),
    Route('/new', method='POST', handler=gameNew),
    Route('/list', method='GET', handler=gameList),
    Route('/game/{gameid}', method='GET', handler=gameGetState),
    Route('/game/{gameid}/move', method='POST', handler=gameMakeMove),
    Route('/game/{gameid}/wait', method='GET', handler=gameWaitForAI)

    # put new game
    # name
    # user, pass
    # ai type
    # any meta options
    # enumerate games
    # list games by name, date
    # resume game
    # get board state for game
    # put move into game
    # await server move (polling)
    # get game move list
]

app = App(routes=routes)

def main():
    app.serve(LISTEN_ADDR, LISTEN_PORT,
              use_debugger=USE_DEBUGGER, use_reloader=USE_DEBUGGER)

if __name__ == '__main__':
    main()
