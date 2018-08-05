from . import AiBase
import game_state as s
import random


class AI(AiBase):

    taunts = [
        'How do you like those apples?',
        'I\'m the bomb!',
        'You\'re toast!',
        'I\'ve got you now!',
        'Hello. My name is Inigo Montoya. You killed my father. ' +
        'Prepare to die.',
        'Bonzai!',
        'You\'re welcome.',
    ]

    def move(self, state):
        moves = s.getLegalMoves(state)
        if not moves:
            raise s.NoMoves(state)
        return random.choice(moves)
