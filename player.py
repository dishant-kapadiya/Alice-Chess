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

        # Adding PAWNS
        for pawn in range(0, 8):
            if self.color == "White":
                self.add_piece(Pawn(1, 1, pawn))
            else:
                self.add_piece(Pawn(1, 6, pawn))
                
        # Adding ROOKS
        if self.color == "White":
            self.add_piece(Rook(1, 0, 0))
            self.add_piece(Rook(1, 0, 7))
        else:
            self.add_piece(Rook(1, 7, 0))
            self.add_piece(Rook(1, 7, 7))

        # Adding KNIGHTS
        if self.color == "White":
            self.add_piece(Knight(1, 0, 1))
            self.add_piece(Knight(1, 0, 6))
        else:
            self.add_piece(Knight(1, 7, 1))
            self.add_piece(Knight(1, 7, 6))

        # Adding BISHOPS
        if self.color == "White":
            self.add_piece(Bishop(1, 0, 2))
            self.add_piece(Bishop(1, 0, 5))
        else:
            self.add_piece(Bishop(1, 7, 2))
            self.add_piece(Bishop(1, 7, 5))

        # Adding QUEEN
        if self.color == "White":
            self.add_piece(Queen(1, 0, 3))
        else:
            self.add_piece(Queen(1, 7, 3))

        # Adding KING
        if self.color == "White":
            self.add_piece(King(1, 0, 4))
        else:
            self.add_piece(King(1, 7, 4))

    def add_piece(self, piece):

        self.arsenal.append(piece)

    def remove_peice(self, piece):

        self.arsenal.remove(piece)

    def make_move(self, move):

        return None