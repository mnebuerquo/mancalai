import importlib
import sys

modules = {}
players = {}


def aiMove(ainame, gamestate):
    """
    What move does the ai make at this game state?
    """
    global modules
    global players
    if ainame not in modules:
        sys.path.append('./mancala')  # Fix the path
        modules[ainame] = importlib.import_module('ai.' + ainame)
        sys.path.pop()                # Undo the path.append
    if ainame not in players:
        players[ainame] = modules[ainame].AI()
    return players[ainame].move(gamestate)
