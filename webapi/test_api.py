import pytest

import api


@pytest.fixture
def client():
    api.app.config['TESTING'] = True
    client = api.app.test_client()

    yield client

    # TODO: cleanup


def test_slash(client):
    rv = client.get('/')
    data = rv.json
    assert data['message'] == 'Welcome to Mancala!'


def test_new(client):
    gamestate = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0, 0]
    rv = client.get('/new')
    data = rv.json
    assert data['gamestate'] == gamestate


def test_move(client):
    gamestate = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0, 0]
    postdata = {"gamestate": gamestate,
                "move": 4}
    rv = client.post('/move', json=postdata)
    data = rv.json
    # {"gamestate":[4,4,4,4,0,5,1,5,5,4,4,4,4,0,1],"status":200}
    assert data['status'] == 200
    assert data['gamestate'] == [4, 4, 4, 4, 0, 5, 1, 5, 5, 4, 4, 4, 4, 0, 1]

    postdata = {
        'gamestate': [4, 4, 4, 4, 4, 0, 0, 4, 4, 4, 4, 4, 4, 0, 0],
        'move': 1,
    }
    rv = client.post('/move', json=postdata)
    data = rv.json
    assert data['status'] == 200
    assert data['gamestate'] == [4, 0, 5, 5, 5, 0, 5, 0, 4, 4, 4, 4, 4, 0, 1]

    """
    curl -X POST --data \
            '{"gamestate":[4,4,4,4,4,0,0,4,4,4,4,4,4,0,0],"move":1}' \
            http://localhost:5000/move
    """


def test_aimove(client):
    gamestate = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0, 0]
    postdata = {"gamestate": gamestate,
                "ai-name": "luck"}
    rv = client.post('/aimove', json=postdata)
    data = rv.json
    # {
    # "ai-name":"luck",
    # "gamestate":[0,5,5,5,5,4,0,4,4,4,4,4,4,0,1],
    # "move":0,
    # "pre-state":[4,4,4,4,4,4,0,4,4,4,4,4,4,0,0],
    # "status":200
    # }

    assert data['status'] == 200
    assert data['ai-name'] == 'luck'
    assert 'move' in data
    assert 'gamestate' in data
    assert data['pre-state'] == gamestate
