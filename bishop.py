from piece import Piece

class Bishop(Piece):

    def __init__(self, board, row, column):

        Piece.__init__(self, board, row, column)

        self.type = "Bishop"

    def moves(self, board, column, row):
        
        return None