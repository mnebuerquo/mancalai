import game_state as s
import random
import tensorflow as tf
import json

INPUT_SIZE = (s.NUM_PLAYERS * 7)
OUTPUT_SIZE = 6
HIDDEN_LAYER_SIZE = 128
LEARNING_RATE = 0.05


def variable(shape, name):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial, name=name)


class Network():

    def __init__(self):
        # placeholders for inputs and outputs
        self.x = tf.placeholder(tf.float32, shape=[None, INPUT_SIZE], name="x")
        self.y_ = tf.placeholder(
            tf.float32, shape=[
                None, OUTPUT_SIZE], name="y_")

        # Hidden layer
        self.W1 = variable([INPUT_SIZE, HIDDEN_LAYER_SIZE], "W1")
        self.b1 = variable([HIDDEN_LAYER_SIZE], "b1")
        self.h1 = tf.nn.relu(
            tf.matmul(self.x, self.W1) + self.b1, name="h1")  # h = a(W1x + b1)

        # Output layer
        self.W_out = variable([HIDDEN_LAYER_SIZE, OUTPUT_SIZE], "W_out")
        self.b_out = variable([OUTPUT_SIZE], "b_out")
        self.y = tf.nn.softmax(tf.matmul(self.h1, self.W_out) +
                               self.b_out, name="y")

        # Cost
        self.cross_entropy = tf.reduce_mean(
            -tf.reduce_sum(self.y_ * tf.log(self.y),
                           reduction_indices=[1]),
            name="cross_entropy")

        # Accuracy
        self.correct_prediction = tf.equal(tf.argmax(self.y, 1),
                                           tf.argmax(self.y_, 1))
        self.accuracy = tf.reduce_mean(
            tf.cast(self.correct_prediction, tf.float32),
            name="accuracy")

    def train(self, datafile):
        self.train_step = tf.train.GradientDescentOptimizer(
            LEARNING_RATE).minimize(self.cross_entropy)
        with open(datafile, "r") as infile:
            head = [json.loads(next(infile)) for x in xrange(N)]
            # https://github.com/shoreason/tensormnist/blob/master/examples/run_mnist_1.py


def taunt():
    taunts = ['I am learning from this game.']
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
