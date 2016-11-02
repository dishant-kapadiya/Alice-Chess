from player import *

class Game:

    def __init__(self):

        self.players = []
        self.board = []

        self.initialize_game()

    def initialize_game(self):

        player_1 = Player("Black")
        player_2 = Player("White")

        self.players.append(player_1)
        self.players.append(player_2)

    def receive_control(self, msg):

        return None

    def transfer_control(self, msg):

        return None

if __name__ == '__main__':
    """
    The main function called when game.py is run
    from the command line:

    > python game.py
    """

    game = Game()
    
    for player in game.players:
        print player.color
        for piece in player.arsenal:
            print piece.type, piece.board, piece.row, piece.column
