from . import AiBase
import random
from .nn_lib import NetworkBase, trainingStream


class Network(NetworkBase):

    def __init__(self, name):
        super().__init__(name)
        self.initPlaceholders()
        self.addHiddenLayer(128)
        self.initOutputLayer()
        self.initCostFn()
        self.initSession()


class AI(AiBase):
    def __init__(self):
        super().__init__()
        self.nn = Network(__name__)

    def taunt(self):
        taunts = [
            'I am learning from this game.',
            'I am learning your tells.',
            'How fast are you learning?',
            'Soon I will have learned everything you know.',
            'You are teaching me how not to play.',
        ]
        return random.choice(taunts)

    def train(self, data=None, datafile=None):
        if data:
            self.nn.train(data)
        if datafile is not None:
            with open(datafile, "r") as infile:
                self.nn.train(trainingStream(infile))

    def move(self, state):
        return self.nn.getMove(state)
