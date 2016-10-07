from piece import Piece

class Knight(Piece):

    def __init__(self, board, column, row):

        self.board = board
        self.column = column
        self.row = row
        self.type = "Knight"
        self.moves = moves

    def moves(self, board, column, row):
        
        return None