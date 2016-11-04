from piece import Piece

class King(Piece):

    def __init__(self, board, row, column):

        Piece.__init__(self, board, row, column)

        self.type = "K"

    def moves(self, board, column, row):
        
        return None