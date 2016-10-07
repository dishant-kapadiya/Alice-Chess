from piece import Piece

class Queen(Piece):

    def __init__(self, board, column, row):

        self.board = board
        self.column = column
        self.row = row
        self.type = "Queen"
        self.moves = moves

    def moves(self, board, column, row):
        
        return None