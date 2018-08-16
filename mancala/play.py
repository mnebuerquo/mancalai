import sys
import cmd
import game_state as s
import draw_game as d
import importlib
from termcolor import cprint


PLAYER_COLORS = ['yellow', 'magenta']


class NoAI(Exception):
    def __init__(self, ptype):
        Exception.__init__(self, "AI type not found: " + str(ptype))


class EndGame(Exception):
    def __init__(self, gamestate):
        Exception.__init__(self, "Game Over.")
        self.gamestate = gamestate
        self.priorstate = gamestate[:]


class Game():

    def setPlayerType(self, player, choice):
        algo = None
        if choice == 'l':
            algo = importlib.import_module('ai.luck')
        elif choice == 'm':
            algo = importlib.import_module('ai.abpwm')
        elif choice == 'n':
            algo = importlib.import_module('ai.nn1h128')
        elif choice == 'h':
            algo = None
        else:
            try:
                algo = importlib.import_module('ai.' + choice)
            except BaseException:
                return False
        if algo:
            cprint("player {} is AI".format(player + 1), PLAYER_COLORS[player])
            self.player_algorithm[player] = algo.AI()
        return True

    def choosePlayer(self, player, opponent=None):
        playertype = ''
        if opponent is not None:
            playertype = opponent
            if not self.setPlayerType(player, opponent):
                playertype = ''
        while playertype == '':
            cprint(
                "Who is player {}?".format(
                    player + 1),
                PLAYER_COLORS[player])
            prompt = "(H)uman or (L)uck or (M)inimax or (N)eural network?: "
            playertype = input(prompt).lower()
            if not self.setPlayerType(player, playertype):
                playertype = ''

    def betweenMoves(self):
        current = s.getCurrentPlayer(self.gamestate)
        module = self.player_algorithm.get(current)
        isHumanNext = True if module is None else False
        while not isHumanNext:
            if s.isGameOver(self.gamestate):
                raise EndGame(self.gamestate)
            current = s.getCurrentPlayer(self.gamestate)
            module = self.player_algorithm.get(current)
            isHumanNext = True if module is None else False
            if not isHumanNext:
                try:
                    d.drawState(self.gamestate, self.priorstate)
                    cprint("My move!", PLAYER_COLORS[current])
                    move = module.move(self.gamestate)
                    self.priorstate = self.gamestate[:]
                    self.gamestate = s.doMove(self.gamestate, move)
                    cprint(module.taunt(), PLAYER_COLORS[current])
                except s.NoMoves as n:
                    cprint("Oops! I have no moves!", PLAYER_COLORS[current])
                    raise EndGame(self.gamestate)
                except Exception:
                    raise NoAI(current)
        pass

    def __init__(self, opponent):
        self.player_algorithm = {}
        cprint("Player 1 is human.", PLAYER_COLORS[0])
        for player in range(1, s.NUM_PLAYERS):
            self.choosePlayer(player, opponent)
        self.gamestate = s.init()
        self.priorstate = self.gamestate[:]
        self.betweenMoves()


class GameConsole(cmd.Cmd):
    intro = 'Welcome to Mancala!'

    def setPrompt(self):
        names = ["Player 1", "Player 2"]
        promptlines = [
            d.getStateDrawing(self.game.gamestate, self.game.priorstate),
            d.getCommandOptionsLine(),
            names[s.getCurrentPlayer(self.game.gamestate)] + ': '
        ]
        self.prompt = "\n".join(promptlines)

    def default(self, c):
        # c is the chosen move, else an error
        # c should be in the range A-F
        c = c.upper()
        opts = ['A', 'B', 'C', 'D', 'E', 'F']
        try:
            move = s.translateMove(self.game.gamestate, opts.index(c))
            self.game.priorstate = self.game.gamestate[:]
            self.game.gamestate = s.doMove(self.game.gamestate, move)
            if s.isGameOver(self.game.gamestate):
                raise EndGame(self.game.gamestate)
        except s.InvalidMove:
            print("That is not a legal move.")
            return
        except s.InvalidPlayer:
            print("You're not valid.")
            return
        except s.InvalidIndex as e:
            print("That index is invalid.")
            raise e
            return
        except ValueError:
            print("You must choose one of the six bowls for your move "
                  "(letters A-F).")
            return
        except Exception as e:
            raise e
            return
        self.game.betweenMoves()
        self.setPrompt()

    def __init__(self, opponent=None):
        super(GameConsole, self).__init__(opponent)
        self.game = Game(opponent)
        self.game.betweenMoves()
        self.setPrompt()


def gameOver(state):
    winner = s.getWinner(s.scoreGame(state))
    print("Congratulations to Player {}".format(winner + 1))
    print(d.getStateDrawing(state))


def run(opponent):
    try:
        GameConsole(opponent).cmdloop()
    except EndGame as e:
        gameOver(e.gamestate)


if __name__ == '__main__':
    run(*sys.argv[1:])
