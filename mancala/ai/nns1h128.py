import random
from .lib import AiNNBase
from .lib.nn_lib import NetworkBase
import tensorflow as tf


class Network(NetworkBase):

    def initInputPlaceholder(self):
        self.input_size = 12
        self.x = tf.placeholder(
            tf.float32,
            shape=(None, 12),
            name="x")

    def makeInputVector(self, state):
        return state[0:6] + state[7:13]

    def __init__(self, name):
        super().__init__(name)
        with self.graph.as_default():
            self.initPlaceholders()
            self.addHiddenLayer(128)
            self.initOutputLayer()
            self.initCostFn()
            self.initSession()


class AI(AiNNBase):
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
