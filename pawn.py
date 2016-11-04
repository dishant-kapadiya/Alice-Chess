from piece import Piece

class Pawn(Piece):

    def __init__(self, board, row, column):

        Piece.__init__(self, board, row, column)
        self.type = "P"

    def valid_moves(self, my_color, game_rep):

        # TODO: Take into account moves that kill opponent piece
        
        # List of tuples indicating (Piece, board_position, start_position, end_position)
        my_moves = []
        columns_list = ["a", "b", "c", "d", "e", "f", "g", "h"]
        
        if my_color == "White" and self.row < 8 and game_rep[self.row + 1][self.board][self.column] != "":
            # All pawns can move one step forward
            my_moves.append(("P", self.board, self.column + str(self.row), self.column + str(self.row + 1)))

            # Starting pawn position can move two steps forward
            if self.board == 1 and self.row == 2:
                my_moves.append(("P", self.board, self.column + str(self.row), self.column + str(self.row + 2)))

        elif my_color == "Black" and self.row > 1:
            # All pawns can move one step forward
            my_moves.append(("P", self.board, self.column + str(self.row), self.column + str(self.row - 1)))

            # Starting pawn position can move two steps forward
            if self.board == 1 and self.row == 7:
                my_moves.append(("P", self.board, self.column + str(self.row), self.column + str(self.row - 2)))

        return my_moves