import game_state as s
import tensorflow as tf
import os
import json
from timeit import default_timer as timer
from .move_scoring import moveToVector
import logging

logger = logging.getLogger(__name__)

INPUT_SIZE = (s.NUM_PLAYERS * 7)
OUTPUT_SIZE = 6

LEARNING_RATE = 0.001
BATCH_SIZE = 10000
EPOCHS = 10
SAVE_PATH = "./data/"
DROPOUT_PROBABILITY = 0.10

# example code
# https://github.com/shoreason/tensormnist/blob/master/examples/run_mnist_1.py


def trainingStream(f):
    for jsonline in f:
        yield json.loads(jsonline)


class NetworkBase():

    def __init__(self, name):
        self.graph = tf.Graph()
        self.name = name
        self.learn_rate = LEARNING_RATE
        self.batch_size = BATCH_SIZE
        self.old_save_path = SAVE_PATH + self.name
        self.save_path = SAVE_PATH + 'models/' + self.name
        self.save_name = self.save_path + '/model'
        self.hiddenSizes = []
        self.hiddenParams = []
        self.dropout_prob = DROPOUT_PROBABILITY
        self.epochs = EPOCHS

    def variable(self, shape, name):
        initial = tf.truncated_normal(shape, stddev=0.1)
        return tf.Variable(initial, name=name)

    def initInputPlaceholder(self):
        self.x = tf.placeholder(tf.float32, shape=[None, INPUT_SIZE], name="x")
        self.input_size = INPUT_SIZE

    def initPlaceholders(self):
        # placeholders for inputs and outputs
        self.initInputPlaceholder()
        self.y_ = tf.placeholder(
            tf.float32, shape=[None, OUTPUT_SIZE], name="y_")
        self.keep_prob = tf.placeholder(tf.float32, name="keep_prob")

    def _lastLayer(self):
        if self.hiddenSizes:
            layernum = len(self.hiddenSizes) + 1
            lastSize = self.hiddenSizes[-1]
            lastLayer = self.hiddenParams[-1][-1]
        else:
            layernum = 1
            lastSize = self.input_size
            lastLayer = self.x
        return (layernum, lastSize, lastLayer)

    def addHiddenLayer(self, layer_size):
        (layernum, lastSize, lastLayer) = self._lastLayer()
        wname = "W" + str(layernum)
        bname = "b" + str(layernum)
        hname = "h" + str(layernum)
        logger.debug('hidden layer: {}, {}'.format(wname, bname))
        W = self.variable([int(lastLayer.shape[-1]), layer_size], wname)
        b = self.variable([layer_size], bname)
        # layer fulfills equation: h = a(Wx + b)
        # a is activation function (relu)
        # x is prior layer output
        # W is weight
        # b is bias
        h = tf.nn.relu(tf.matmul(lastLayer, W) + b, name=hname)
        d = tf.nn.dropout(h, self.keep_prob)
        self.hiddenSizes.append(layer_size)
        self.hiddenParams.append((W, b, h, d))

    def initOutputLayer(self):
        (layernum, lastSize, lastLayer) = self._lastLayer()
        self.W_out = self.variable([int(lastLayer.shape[-1]), OUTPUT_SIZE], "W_out")
        self.b_out = self.variable([OUTPUT_SIZE], "b_out")
        self.y = tf.nn.softmax(tf.matmul(lastLayer, self.W_out) +
                               self.b_out, name="y")

    def initCostFn(self):
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

        # Train step
        self.train_step = tf.train.GradientDescentOptimizer(
            LEARNING_RATE).minimize(self.cross_entropy)

    def initSession(self):
        # use a saver to save/restore with a file
        self.saver = tf.train.Saver(tf.trainable_variables())

        # don't need an interactive session here
        # https://stackoverflow.com/q/41791469/5114
        self.sess = tf.Session(graph=self.graph)
        try:
            logger.info("loading nn weights from {}".format(self.save_name))
            self.saver.restore(self.sess, self.save_name)
            loaded = True
        except Exception as e:
            # could not load
            loaded = False
        if not loaded:
            # start from scratch
            logger.warning(
                "Could not load checkpoint for {}".format(
                    self.name))
            self.sess.run(tf.global_variables_initializer())

    def makeInputVector(self, state):
        return state[:14]

    def train_batch(self, batch):
        start = timer()
        dfx = [self.makeInputVector(row[0]) for row in batch] * self.epochs
        dfy_ = [moveToVector(*row) for row in batch] * self.epochs
        fd = {
            self.x: dfx,
            self.y_: dfy_,
            self.keep_prob: 1 - self.dropout_prob
        }
        self.train_step.run(session=self.sess, feed_dict=fd)
        os.makedirs(self.save_path, exist_ok=True)
        self.saver.save(self.sess, self.save_name)
        end = timer()
        count = len(batch)
        diff = end - start
        rate = self.epochs * count / diff
        msg = "{} trained {} epochs of {} moves in {} sec, at rate {} m/s"
        print(
            msg.format(
                self.name,
                self.epochs,
                count,
                int(diff * 1000) / 1000,
                int(rate * 1000) / 1000
            ))

    def train(self, datastream):
        rows = 0
        head = []
        for row in datastream:
            head.append(row)
            if len(head) >= self.batch_size:
                self.train_batch(head)
                rows += len(head)
                head = []
        if head:
            self.train_batch(head)
            rows += len(head)
            head = []
        print("Trained {} moves.".format(rows))

    def getMove(self, state):
        # rotate the board for current player
        player = s.getCurrentPlayer(state)
        if player != 0:
            flip = True
            board = s.flipBoard(state)
        else:
            flip = False
            board = state
        # get output of neural network
        fd = {self.x: [self.makeInputVector(board[:14])], self.keep_prob: 1.0}
        y = self.sess.run(self.y, fd)
        # y is a list containing a single output vector
        # y == [[0.0108906 0.1377293 0.370027 0.2287382 0.0950692 0.1575449]]
        scores = list(y[0])
        bestmove = -1
        bestscore = -1
        # we only want to pick from legal moves (the nn will learn these
        # eventually, but we're helping him with this constraint)
        legalMoves = s.getLegalMoves(board)
        for m in legalMoves:
            if bestscore < scores[m]:
                bestmove = m
                bestscore = scores[m]
        if bestmove < 0:
            bestmove = legalMoves[0]
        move = bestmove
        # if we rotated the board before, rotate it back
        if flip:
            move = s.flipMove(move, player)
        return move
