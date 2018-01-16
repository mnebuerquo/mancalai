import cmd
import game_state as s
import draw_game as d

class GameConsole(cmd.Cmd):
    intro = 'Welcome to Mancala!'
    prompt = 'Player 1'
    gamestate = []

    def setPrompt(self):
        names = ["Player 1", "Player 2"]
        promptlines = [
                d.getStateDrawing(range(15)),
                d.getStateDrawing(self.gamestate),
                d.getCommandOptionsLine(),
                names[s.getCurrentPlayer(self.gamestate)]+': '
                ]
        self.prompt = "\n".join(promptlines)

    def default(self, c):
        # c is the chosen move, else an error
        # c should be in the range A-F
        c = c.upper()
        opts = ['A','B','C','D','E','F']
        try:
            move = s.translateMove(self.gamestate, opts.index(c))
            self.gamestate = s.doMove(self.gamestate, move)
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
            print("You must choose one of the six bowls for your move (letters A-F).")
            return
        except Exception as e:
            raise e
            return
        self.setPrompt()
        pass

    def __init__(self):
        super(GameConsole,self).__init__()
        self.gamestate = s.init()
        self.setPrompt()

if __name__ == '__main__':
    GameConsole().cmdloop()
