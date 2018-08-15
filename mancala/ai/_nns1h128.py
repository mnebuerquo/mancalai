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

    def conv2d(self, x, W, b, strides=1):
        # Conv2D wrapper, with bias and relu activation
        x = tf.nn.conv2d(x, W, strides=[1, strides, strides, 1], padding='SAME')
        x = tf.nn.bias_add(x, b)
        return tf.nn.relu(x)

    def maxpool2d(self, x, k=2):
        return tf.nn.max_pool(x, ksize=[1, k, k, 1], strides=[1, k, k, 1],padding='SAME')

    def addConvLayer(self, width, height):
        W = self.variable([2,2,1,32], "Wc")
        b = self.variable([32], "bc")

        conv = conv2d(self.x, W, b)
        mp = maxpool2d(conv, k=2)

        reshaped = ???

        '''
        https://www.datacamp.com/community/tutorials/cnn-tensorflow-python

        def weight_variable(shape):
          initial = tf.truncated_normal(shape, stddev=0.1)
          return tf.Variable(initial)

        def bias_variable(shape):
          initial = tf.constant(0.1, shape=shape)
          return tf.Variable(initial)

        def conv2d(x, W):
          return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

        def max_pool_2x2(x):
          return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                                strides=[1, 2, 2, 1], padding='SAME')

        W_conv1 = weight_variable([5, 5, 1, 32])
        b_conv1 = bias_variable([32])

        x = tf.placeholder(tf.float32, [None, 784])
        x_image = tf.reshape(x, [-1,28,28,1])

        h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
        h_pool1 = max_pool_2x2(h_conv1)


        W_conv2 = weight_variable([5, 5, 32, 64])
        b_conv2 = bias_variable([64])

        h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
        h_pool2 = max_pool_2x2(h_conv2)


        W_fc1 = weight_variable([7 * 7 * 64, 1024])
        b_fc1 = bias_variable([1024])

        h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
        h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
        '''

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
