from game import Game
from player import Player, BasicPlayer

if __name__ == "__main__":

    players = [
        Player(), Player(), BasicPlayer(), BasicPlayer()
    ]


    game = Game(players)
    game.init_board()

    print(game.board)

    for i in range(10):
        game.make_turn()
        print(game.board)

    for i, player in enumerate(players):
        print(f"{i}: {player.get_penalty()}")