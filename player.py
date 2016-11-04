from pawn import Pawn
from rook import Rook
from knight import Knight
from bishop import Bishop
from queen import Queen
from king import King

class Player:

    def __init__(self, color):

        self.color = color
        self.arsenal = []
        self.martyrs = []
        
        self.initialize_player()

    def initialize_player(self):

        columns = ["a", "b", "c", "d", "e", "f", "g", "h"]

        # Adding PAWNS
        for column in columns:
            if self.color == "White":
                self.add_piece(Pawn(1, 2, column))
            else:
                self.add_piece(Pawn(1, 7, column))
                
        # Adding ROOKS
        if self.color == "White":
            self.add_piece(Rook(1, 1, "a"))
            self.add_piece(Rook(1, 1, "h"))
        else:
            self.add_piece(Rook(1, 8, "a"))
            self.add_piece(Rook(1, 8, "h"))

        # Adding KNIGHTS
        if self.color == "White":
            self.add_piece(Knight(1, 1, "b"))
            self.add_piece(Knight(1, 1, "g"))
        else:
            self.add_piece(Knight(1, 8, "b"))
            self.add_piece(Knight(1, 8, "g"))

        # Adding BISHOPS
        if self.color == "White":
            self.add_piece(Bishop(1, 1, "c"))
            self.add_piece(Bishop(1, 1, "f"))
        else:
            self.add_piece(Bishop(1, 8, "c"))
            self.add_piece(Bishop(1, 8, "f"))

        # Adding QUEEN
        if self.color == "White":
            self.add_piece(Queen(1, 1, "d"))
        else:
            self.add_piece(Queen(1, 8, "d"))

        # Adding KING
        if self.color == "White":
            self.add_piece(King(1, 1, "e"))
        else:
            self.add_piece(King(1, 8, "e"))

    def add_piece(self, piece):

        self.arsenal.append(piece)

    def remove_peice(self, piece):

        self.arsenal.remove(piece)

    def get_valid_moves(self, game_rep):

        my_valid_moves = []

        for my_piece in self.arsenal:
            my_valid_moves = my_valid_moves + my_piece.valid_moves(self.color, game_rep)
            print my_valid_moves

        # print my_valid_moves