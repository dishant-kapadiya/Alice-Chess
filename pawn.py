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
        
        if my_color == "White" and self.row < 8:

            try:
                # Check if the next row has a piece or not
                if game_rep[str(self.row + 1)][str(self.board)][self.column] == "":
                    # All pawns can move one step forward
                    my_moves.append(("P", self.board, self.column + str(self.row), self.column + str(self.row + 1)))

                    # Starting pawn position can move two steps forward
                    if self.board == 1 and self.row == 2:
                        my_moves.append(("P", self.board, self.column + str(self.row), self.column + str(self.row + 2)))

            except KeyError:
                pass

        elif my_color == "Black" and self.row > 1:

            try:
                # Check if the next row has a piece or not
                if game_rep[str(self.row - 1)][str(self.board)][self.column] == "":
                    # All pawns can move one step forward
                    my_moves.append(("P", self.board, self.column + str(self.row), self.column + str(self.row - 1)))

                    # Starting pawn position can move two steps forward
                    if self.board == 1 and self.row == 7:
                        my_moves.append(("P", self.board, self.column + str(self.row), self.column + str(self.row - 2)))

            except KeyError:
                pass

        dest_board = self.board == 1 and 2 or 1
        my_final_moves = []

        # Check if opposite board is empty
        for move in my_moves:
            destination = move[-1]
            if game_rep[destination[1]][str(dest_board)][destination[0]] == "":
                my_final_moves.append(move)

        return my_final_moves