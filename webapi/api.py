from flask import Flask, request
from mancala import game_state
from flask_json import FlaskJSON, as_json, JsonError, jsonify
from mancala.aimove import aiMove
from mancala.game_state import isGameOver, scoreGame, getScore, getWinner

app = Flask(__name__)
FlaskJSON(app)


def fixInputData(state):
    return [int(x) for x in state]


def errorMessage(code, message):
    message = {
        'status': code,
        'message': message,
        'httpcat': 'https://http.cat/' + str(code)
    }
    resp = jsonify(message)
    resp.status_code = code
    return resp


def checkWin(response):
    gamestate = response['gamestate']
    gamestate = scoreGame(gamestate)
    response['gameOver'] = isGameOver(gamestate)
    if response['gameOver']:
        response['gameOver'] = True
        response['winner'] = getWinner(gamestate)
        response['score'] = getScore(gamestate)
    return response


@app.errorhandler(404)
def not_found(error=None):
    return errorMessage(404, 'Not Found: ' + request.url)


@app.errorhandler(405)
def not_allowed(error=None):
    return errorMessage(405, 'Method not allowed')


@app.route("/")
@as_json
def slash():
    return {"message": "Welcome to Mancala!"}


@app.route("/move", methods=['POST'])
@as_json
def move():
    """
    Evaluate a player move and return the new gamestate.

    curl -X POST --data \
            '{"gamestate":[4,4,4,4,4,4,0,4,4,4,4,4,4,0,0],"move":4}' \
            http://localhost:5000/move
    """
    data = request.get_json(force=True)
    try:
        state = fixInputData(data['gamestate'])
        move = int(data['move'])
    except (KeyError, TypeError, ValueError):
        raise JsonError(description='Invalid value.')
    resp = {"gamestate": game_state.doMove(state, move)}
    return checkWin(resp)


@app.route("/aimove", methods=['POST'])
@as_json
def aimove():
    """
    Get the ai move for the current gamestate, as well as the resulting
    gamestate.

    curl -X POST --data \
            '{"gamestate":[4,4,4,4,4,4,0,4,4,4,4,4,4,0,0],"ai-name":"luck"}' \
            http://localhost:5000/aimove
    """
    data = request.get_json(force=True)
    try:
        state = fixInputData(data['gamestate'])
        ai = str(data['ai-name'])
    except (KeyError, TypeError, ValueError):
        raise JsonError(description='Invalid value.')
    move = aiMove(ai, state)
    resp = {
        "pre-state": state,
        "ai-name": ai,
        "move": move,
        "gamestate": game_state.doMove(state, move)
    }
    return checkWin(resp)


@app.route("/new")
@as_json
def new():
    """
    Create a new game, return its state.
    """
    return checkWin({"gamestate": game_state.init()})


def main():
    app.run(host='0.0.0.0')
