import random
from .lib import AiBase
from .lib.nn_lib import NetworkBase, trainingStream
import tensorflow as tf


class Network(NetworkBase):

    def initInputPlaceholder(self):
        self.x = tf.placeholder(
            tf.float32,
            shape=(None, 6, 2, 1),
            name="x")

    def makeInputVector(self, state):
        return [state[0:6], state[7:13]]

    def __init__(self, name):
        super().__init__(name)
        with self.graph.as_default():
            self.initPlaceholders()
            self.addConvLayer()
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
            'I look at the board in a different way.',
            "I'll win this one for sure.",
            "You're not as good looking as I am.",
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
