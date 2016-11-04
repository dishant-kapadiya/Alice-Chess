from piece import Piece

class Queen(Piece):

    def __init__(self, board, row, column):

        Piece.__init__(self, board, row, column)

        self.type = "Q"

    def moves(self, board, column, row):
        
        return None