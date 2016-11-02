from piece import Piece

class Knight(Piece):

    def __init__(self, board, row, column):

        Piece.__init__(self, board, row, column)

        self.type = "Knight"

    def moves(self, board, column, row):
        
        return None