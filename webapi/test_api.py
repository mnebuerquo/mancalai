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

    postdata = {
        'gamestate': [0, 0, 0, 0, 0, 1, 0, 4, 4, 4, 4, 4, 4, 0, 0],
        'move': 5,
    }
    rv = client.post('/move', json=postdata)
    data = rv.json
    assert data['status'] == 200
    assert data['gamestate'] == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 24, 0]


def test_aimove(client):
    gamestate = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0, 0]
    postdata = {"gamestate": gamestate,
                "ai-name": "luck"}
    rv = client.post('/aimove', json=postdata)
    data = rv.json

    assert data['status'] == 200
    assert data['ai-name'] == 'luck'
    assert 'move' in data
    assert int(data['move']) in range(0, 6)
    assert 'gamestate' in data
    assert data['pre-state'] == gamestate

    gamestate = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0, 1]
    postdata = {"gamestate": gamestate,
                "ai-name": "luck"}
    rv = client.post('/aimove', json=postdata)
    data = rv.json
    assert data['status'] == 200
    assert data['ai-name'] == 'luck'
    assert 'move' in data
    assert int(data['move']) in range(7, 13)
    assert 'gamestate' in data
    assert data['pre-state'] == gamestate

    postdata = {
        'gamestate': [0, 0, 0, 0, 0, 1, 0, 4, 4, 4, 4, 4, 4, 0, 0],
        'ai-name': 'luck'
    }
    rv = client.post('/aimove', json=postdata)
    data = rv.json
    assert data['status'] == 200
    assert data['move'] == 5
    assert data['winner'] == 1
    assert data['gameOver'] is True
    assert data['gamestate'] == [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 24, 0]
