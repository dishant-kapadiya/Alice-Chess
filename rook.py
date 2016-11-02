from piece import Piece

class Rook(Piece):

    def __init__(self, board, row, column):

        Piece.__init__(self, board, row, column)

        self.type = "Rook"

    def moves(self, board, column, row):
        
        return None