from . import AiBase
import random
from .nn_lib import NetworkBase, trainingStream


class Network(NetworkBase):

    def __init__(self, name):
        super().__init__(name)
        self.initPlaceholders()
        self.addHiddenLayer(80)
        self.addHiddenLayer(80)
        self.addHiddenLayer(80)
        self.initOutputLayer()
        self.initCostFn()
        self.initSession()


class AI(AiBase):
    def __init__(self):
        super().__init__()
        self.nn = Network(__name__)

    def taunt(self):
        taunts = [
            'I have three hidden layers. How many do you have?',
            'I might be three times as smart as you.',
            'I could beat you in like three seconds if I want to.',
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
