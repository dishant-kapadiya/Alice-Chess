from piece import Piece

class Queen(Piece):

    def __init__(self, board, row, column):

        Piece.__init__(self, board, row, column)
        self.type = "Q"

    def valid_moves(self, my_color, game_rep):
        
        return []