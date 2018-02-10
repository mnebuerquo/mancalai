import game_state as s
import random


def taunt():
    taunts = [
            'How do you like those apples?',
            'I\'m the bomb!',
            'You\'re toast!',
            'I\'ve got you now!',
            'Hello. My name is Inigo Montoya. You killed my father. ' +
            'Prepare to die.',
            'Bonzai!',
            'You\'re welcome.'
            ]
    return random.choice(taunts)


def youWin():
    pass


def youLose():
    pass


def move(state):
    moves = s.getLegalMoves(state)
    if not moves:
        raise s.NoMoves(state)
    return random.choice(moves)
