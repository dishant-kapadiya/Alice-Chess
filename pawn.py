from piece import Piece

class Pawn(Piece):

    def __init__(self, board, row, column):

        Piece.__init__(self, board, row, column)
        self.type = "Pawn"

    def moves(self, board, column, row):
        
        return None