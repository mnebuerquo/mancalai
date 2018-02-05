import cmd
import game_state as s
import draw_game as d
import ai


class NoAI(Exception):
    def __init__(self, ptype):
        Exception.__init__(self, "AI type not found: "+ptype)


class EndGame(Exception):
    def __init__(self, gamestate):
        Exception.__init__(self, "Game Over.")
        self.gamestate = gamestate


class GameConsole(cmd.Cmd):
    intro = 'Welcome to Mancala!'
    prompt = 'Player 1'
    gamestate = []

    def setPrompt(self):
        names = ["Player 1", "Player 2"]
        promptlines = [
                d.getStateDrawing(self.gamestate),
                d.getCommandOptionsLine(),
                names[s.getCurrentPlayer(self.gamestate)]+': '
                ]
        self.prompt = "\n".join(promptlines)

    def betweenMoves(self):
        current = s.getCurrentPlayer(self.gamestate)
        ptype = self.playertype[current]
        if 'h' == ptype:
            return
        elif 'r' == ptype:
            move = ai.luck.move(self.gamestate)
            self.gamestate = s.doMove(self.gamestate, move)
        else:
            raise NoAI(ptype)
        pass

    def default(self, c):
        # c is the chosen move, else an error
        # c should be in the range A-F
        c = c.upper()
        opts = ['A', 'B', 'C', 'D', 'E', 'F']
        try:
            move = s.translateMove(self.gamestate, opts.index(c))
            self.gamestate = s.doMove(self.gamestate, move)
            if s.isGameOver(self.gamestate):
                raise EndGame(self.gamestate)
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
        self.betweenMoves()
        self.setPrompt()

    def choosePlayer(self, player):
        print("Who is player {}?".format(player+1))
        playertype = ''
        while playertype not in ['h', 'r']:
            playertype = input("(H)uman or (R)andom: ").lower()
        self.playertype[player] = playertype

    def __init__(self, gamestate=None):
        super(GameConsole, self).__init__()
        self.playertype = (['h']*2)[:]
        for player in range(s.NUM_PLAYERS):
            self.choosePlayer(player)
        self.gamestate = gamestate or s.init()
        self.setPrompt()


def gameOver(state):
    winner = s.getWinner(s.scoreGame(state))
    print("Congratulations to Player {}".format(winner+1))


def run(gamestate=None):
    try:
        GameConsole(gamestate).cmdloop()
    except EndGame as e:
        gameOver(e.gamestate)


if __name__ == '__main__':
    run()
