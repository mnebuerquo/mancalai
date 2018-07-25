from . import AiBase
import game_state as s
import random
import tensorflow as tf
import json

INPUT_SIZE = (s.NUM_PLAYERS * 7)
OUTPUT_SIZE = 6
HIDDEN_LAYER_SIZE = 128
LEARNING_RATE = 0.05
BATCH_SIZE = 50
SAVE_PATH = "./data/model.ckpt"
BETTER_MOVE = 0.5
WINNING_MOVE = 1
LOSING_MOVE = 0


def variable(shape, name):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial, name=name)


def losingVector(m):
    """
    Return vector of moves with losing move score set low, and others higher.
    >>> losingVector(3) == [BETTER_MOVE, BETTER_MOVE, BETTER_MOVE, \
                            LOSING_MOVE, BETTER_MOVE, BETTER_MOVE]
    True
    >>> losingVector(1) == [BETTER_MOVE, LOSING_MOVE, BETTER_MOVE, \
                            BETTER_MOVE, BETTER_MOVE, BETTER_MOVE]
    True
    """
    z = [BETTER_MOVE] * 6
    return z[:m] + [LOSING_MOVE] + z[m + 1:]


def winningVector(m):
    """
    Return vector of moves with winning move score set high, and others low.
    >>> winningVector(3) == [LOSING_MOVE, LOSING_MOVE, LOSING_MOVE, \
                            WINNING_MOVE, LOSING_MOVE, LOSING_MOVE]
    True
    >>> winningVector(1) == [LOSING_MOVE, WINNING_MOVE, LOSING_MOVE, \
                            LOSING_MOVE, LOSING_MOVE, LOSING_MOVE]
    True
    """
    z = [LOSING_MOVE] * 6
    return z[:m] + [WINNING_MOVE] + z[m + 1:]


def legalVector(state, vector):
    """
    >>> state = [1, 2, 3, 0, 5, 6, 0, 12, 11, 10, 9, 8, 7, 0, 0]
    >>> expected = [WINNING_MOVE, WINNING_MOVE, WINNING_MOVE, \
            LOSING_MOVE, WINNING_MOVE, WINNING_MOVE]
    >>> legalVector(state, [WINNING_MOVE]*6) == expected
    True
    """
    return [vector[m] if s.isLegalMove(
        state, m) else LOSING_MOVE for m in range(6)]


def moveToVector(state, m, iswinner):
    """
    Create a vector of scores for winning moves and losing moves. Treat any
    illegal move as a losing move.

    >>> state = [1, 2, 3, 4, 5, 6, 0, 12, 11, 10, 9, 8, 7, 0, 0]
    >>> moveToVector(state, 0, 1) == [WINNING_MOVE, LOSING_MOVE, LOSING_MOVE, \
                            LOSING_MOVE, LOSING_MOVE, LOSING_MOVE]
    True
    >>> state = [1, 2, 3, 0, 5, 6, 0, 12, 11, 10, 9, 8, 7, 0, 0]
    >>> moveToVector(state, 2, 0) == [BETTER_MOVE, BETTER_MOVE, LOSING_MOVE, \
                            LOSING_MOVE, BETTER_MOVE, BETTER_MOVE]
    True
    """
    vector = winningVector(m) if iswinner else losingVector(m)
    return legalVector(state, vector)


class Network():

    # https://github.com/shoreason/tensormnist/blob/master/examples/run_mnist_1.py

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

        self.saver = tf.train.Saver()

        self.sess = tf.InteractiveSession()
        try:
            if tf.train.checkpoint_exists(
                    tf.train.latest_checkpoint(SAVE_PATH)):
                self.saver.restore(self.sess, SAVE_PATH)
                loaded = True
        except Exception:
            loaded = False
        if not loaded:
            self.sess.run(tf.global_variables_initializer())

    def getMove(self, state):
        # get output of neural network
        y = self.sess.run(self.y, {self.x: [state[:14]]})
        # y is a list containing a single output vector
        # y == [[0.0108906 0.1377293 0.370027 0.2287382 0.0950692 0.1575449]]
        scores = list(y[0])
        bestmove = -1
        bestscore = -1
        # we only want to pick from legal moves (the nn will learn these
        # eventually, but we're helping him with this constraint)
        moves = s.getLegalMoves(state)
        for m in moves:
            if bestscore < scores[m]:
                bestmove = m
                bestscore = scores[m]
        if bestmove < 0:
            bestmove = moves[0]
        return bestmove

    def train_batch(self, batch):
        train_step = tf.train.GradientDescentOptimizer(
            LEARNING_RATE).minimize(self.cross_entropy)
        dfx = [s[:14] for s, m, w in batch]
        dfy_ = [moveToVector(s, m, w) for s, m, w in batch]
        train_step.run(feed_dict={self.x: dfx, self.y_: dfy_})
        self.saver.save(self.sess, SAVE_PATH)

    def train(self, data=None, datafile=None):
        rows = 0
        if datafile is not None:
            with open(datafile, "r") as infile:
                head = []
                for row in infile:
                    head.append(json.loads(row))
                    if len(head) >= BATCH_SIZE:
                        self.train_batch(head)
                        rows += len(head)
                        head = []
                        print(" Trained batch...")
                if head:
                    self.train_batch(head)
                    rows += len(head)
                    head = []
        if data is not None:
            self.train_batch(data)
            rows += len(data)
        print("Trained {} moves.".format(rows))


class AI(AiBase):
    def __init__(self):
        super().__init__()
        self.nn = Network()

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
        self.nn.train(data=data, datafile=datafile)

    def move(self, state):
        player = s.getCurrentPlayer(state)
        if player != 0:
            flip = True
            board = s.flipBoard(state)
        else:
            flip = False
            board = state
        move = self.nn.getMove(board)
        if flip:
            move = s.flipMove(move, player)
        return move
