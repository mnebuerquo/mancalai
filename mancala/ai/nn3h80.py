import random
from .lib import AiNNBase
from .lib.nn_lib import NetworkBase


class Network(NetworkBase):

    def __init__(self, name):
        super().__init__(name)
        with self.graph.as_default():
            self.initPlaceholders()
            self.addHiddenLayer(80)
            self.addHiddenLayer(80)
            self.addHiddenLayer(80)
            self.initOutputLayer()
            self.initCostFn()
            self.initSession()


class AI(AiNNBase):
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
