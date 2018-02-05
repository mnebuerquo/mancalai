import cmd
import game_state as s
import draw_game as d
import importlib


class NoAI(Exception):
    def __init__(self, ptype):
        Exception.__init__(self, "AI type not found: " + str(ptype))


class EndGame(Exception):
    def __init__(self, gamestate):
        Exception.__init__(self, "Game Over.")
        self.gamestate = gamestate


class Game():

    def setPlayerType(self, player, choice):
        if choice == 'l':
            self.player_algorithm[player] = importlib.import_module('ai.luck')
        else:
            self.player_algorithm[player] = None

    def choosePlayer(self, player):
        print("Who is player {}?".format(player+1))
        playertype = ''
        while playertype not in ['h', 'l']:
            playertype = input("(H)uman or (L)uck: ").lower()
            self.setPlayerType(player, playertype)

    def betweenMoves(self):
        isHumanNext = False
        while not isHumanNext:
            current = s.getCurrentPlayer(self.gamestate)
            module = self.player_algorithm.get(current)
            if module is None:
                isHumanNext = True
                return
            try:
                isHumanNext = False
                print("My move!")
                print(dir(module))
                move = module.move(self.gamestate)
                self.gamestate = s.doMove(self.gamestate, move)
                print(module.taunt())
            except Exception:
                raise NoAI(current)
        pass

    def __init__(self, gamestate):
        self.player_algorithm = {}
        for player in range(s.NUM_PLAYERS):
            self.choosePlayer(player)
        self.gamestate = gamestate or s.init()


class GameConsole(cmd.Cmd):
    intro = 'Welcome to Mancala!'
    prompt = 'Player 1'

    def setPrompt(self):
        names = ["Player 1", "Player 2"]
        promptlines = [
                d.getStateDrawing(self.game.gamestate),
                d.getCommandOptionsLine(),
                names[s.getCurrentPlayer(self.game.gamestate)]+': '
                ]
        self.prompt = "\n".join(promptlines)

    def default(self, c):
        # c is the chosen move, else an error
        # c should be in the range A-F
        c = c.upper()
        opts = ['A', 'B', 'C', 'D', 'E', 'F']
        try:
            move = s.translateMove(self.game.gamestate, opts.index(c))
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

    def __init__(self, gamestate=None):
        super(GameConsole, self).__init__()
        self.game = Game(gamestate)
        self.setPrompt()


def gameOver(state):
    winner = s.getWinner(s.scoreGame(state))
    print("Congratulations to Player {}".format(winner+1))
    print(d.getStateDrawing(self.game.gamestate))


def run(gamestate=None):
    try:
        GameConsole(gamestate).cmdloop()
    except EndGame as e:
        gameOver(e.gamestate)


if __name__ == '__main__':
    run()
