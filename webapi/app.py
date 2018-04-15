import os
from apistar import App, Route

LISTEN_ADDR = os.environ.get('LISTEN_ADDR', '127.0.0.1')
LISTEN_PORT = os.environ.get('LISTEN_PORT', '5000')
USE_DEBUGGER = True if os.environ.get('DEBUG') == "True" else False

def welcome():
    return {'message': 'Welcome to Mancala'}


routes = [
    Route('/', method='GET', handler=welcome),

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


if __name__ == '__main__':
    app.serve(LISTEN_ADDR, LISTEN_PORT,
            use_debugger=USE_DEBUGGER, use_reloader=USE_DEBUGGER)
