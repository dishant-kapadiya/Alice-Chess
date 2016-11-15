from piece import Piece

class Rook(Piece):

    def __init__(self, board, row, column):

        Piece.__init__(self, board, row, column)
        self.type = "R"

    def valid_moves(self, my_color, game_rep):
        
        # TODO: Take into account moves that kill opponent piece
        
        # List of tuples indicating (Piece, board_position, start_position, end_position)
        my_moves = []
        columns_list = ["a", "b", "c", "d", "e", "f", "g", "h"]

        u = []

        for i in range(1,7):
            if ((self.row + i) < 8):
                # If piece found going upwards, break from loop
                if game_rep[str(self.row + i)][str(self.board)][self.column] != "":
                    break

                u.append(("R", self.board, self.column + str(self.row), self.column + str(self.row + i)))

        d = []

        for i in range(1,7):
            if ((self.row - i) > 1):
                # If piece found going downwards, break from loop
                if game_rep[str(self.row - i)][str(self.board)][self.column] != "":
                    break

                u.append(("R", self.board, self.column + str(self.row), self.column + str(self.row - i)))

        r = []

        for i in range(1,7):
            if (columns_list.index(self.column) + i) < 7 :
                # If piece found going right, break from loop
                if game_rep[str(self.row)][str(self.board)][columns_list[columns_list.index(self.column) + 1]] != "":
                    break

                u.append(("R", self.board, self.column + str(self.row), columns_list[columns_list.index(self.column) + 1] + str(self.row)))

        l = []

        for i in range(1,7):
            if (columns_list.index(self.column) - i) > 0 :
                # If piece found going left, break from loop
                if game_rep[str(self.row)][str(self.board)][columns_list[columns_list.index(self.column) - 1]] != "":
                    break

                u.append(("R", self.board, self.column + str(self.row), columns_list[columns_list.index(self.column) - 1] + str(self.row)))
        
        my_moves = u + d + r + l
        
        dest_board = self.board == 1 and 2 or 1
        my_final_moves = []

        # Check if opposite board is empty
        for move in my_moves:
            destination = move[-1]
            if game_rep[destination[1]][str(dest_board)][destination[0]] == "":
                my_final_moves.append(move)
        
        return my_final_moves