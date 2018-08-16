import random
from .lib import AiBase
from .lib.nn_lib import NetworkBase, trainingStream
import tensorflow as tf

class Network(NetworkBase):

    def initInputPlaceholder(self):
        self.x = tf.placeholder(
            tf.float32,
            shape=(None, 2, 6, 1),
            name="x")

    def conv2d(self, x, W, b, strides=1):
        # Conv2D wrapper, with bias and relu activation
        x = tf.nn.conv2d(x, W, strides=[1, strides, strides, 1],
                padding='SAME', name="conv_Wx")
        x = tf.nn.bias_add(x, b, name="conv_Wx_b")
        return tf.nn.relu(x, name="conv_Wx_b_relu")

    def maxpool2d(self, x, k=2):
        return tf.nn.max_pool(x,
                ksize=[1, k, k, 1],
                strides=[1, k, k, 1],
                padding='SAME',
                name="mp")

    def addConvLayer(self):
        '''
        https://www.datacamp.com/community/tutorials/cnn-tensorflow-python
        '''
        self.Wc = self.variable([2,2,1,32], "Wc")
        self.bc = self.variable([32], "bc")

        self.conv = self.conv2d(self.x, self.Wc, self.bc)
        self.mp = self.maxpool2d(self.conv, k=2)

        self.reshaped = tf.reshape(self.mp, [-1, 12], name="r")
        self.input_size = 12

        self.hiddenSizes.append(self.input_size)
        self.hiddenParams.append((self.Wc, self.bc, self.mp, self.reshaped))


    def makeInputVector(self, state):
        return [
                [[x] for x in state[0:6]],
                [[x] for x in state[7:13]]
                ]

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
