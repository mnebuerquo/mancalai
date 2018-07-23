from flask import Flask, request
from mancala import game_state
from flask_json import FlaskJSON, as_json, JsonError, jsonify
from mancala.aimove import aiMove

app = Flask(__name__)
FlaskJSON(app)


def decodeState(state):
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
    curl -X POST --data \
            '{"gamestate":[4,4,4,4,4,4,0,4,4,4,4,4,4,0,0],"move":4}' \
            http://localhost:5000/move
    """
    data = request.get_json(force=True)
    try:
        state = decodeState(data['gamestate'])
        move = int(data['move'])
    except (KeyError, TypeError, ValueError):
        raise JsonError(description='Invalid value.')
    return {"gamestate": game_state.doMove(state, move)}


@app.route("/aimove", methods=['POST'])
@as_json
def aimove():
    """
    curl -X POST --data \
            '{"gamestate":[4,4,4,4,4,4,0,4,4,4,4,4,4,0,0],"ai-name":"luck"}' \
            http://localhost:5000/aimove
    """
    data = request.get_json(force=True)
    try:
        state = decodeState(data['gamestate'])
        ai = str(data['ai-name'])
    except (KeyError, TypeError, ValueError):
        raise JsonError(description='Invalid value.')
    move = aiMove(ai, state)
    return {
        "pre-state": state,
        "ai-name": ai,
        "move": move,
        "gamestate": game_state.doMove(state, move)
    }


@app.route("/new")
@as_json
def new():
    """
    Create a new game, return its state.
    """
    return {"gamestate": game_state.init()}


def main():
    app.run()
