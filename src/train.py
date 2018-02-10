import game_state as s
import importlib

def play_game(algorithm1, algorithm2):
    pass

def main(name1, name2, count):
    player1 = importlib.import_module('ai.'+name1)
    player2 = importlib.import_module('ai.'+name2)

    for i in range(count):
        result = play_game(player1, player2)

if __name__ == '__main__':
    main()
