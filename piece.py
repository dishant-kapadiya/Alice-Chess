class Piece:

    def __init__(self, board, row, column):

        self.board = board
        self.row = row
        self.column = column

    def make_move(self, destination):

        self.board = self.board == 1 and 2 or 1
        self.row = int(destination[1])
        self.column = destination[0]