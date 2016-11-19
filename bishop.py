from piece import Piece

class Bishop(Piece):

    def __init__(self, board, row, column):

        Piece.__init__(self, board, row, column)
        self.type = "B"

    def valid_moves(self, my_color, game_rep):
        
        # TODO: Take into account moves that kill opponent piece
        
        # List of tuples indicating (Piece, board_position, start_position, end_position)
        my_moves = []
        columns_list = ["a", "b", "c", "d", "e", "f", "g", "h"]

        ur = []
        for i in range(1,8):
            if ((self.row + i) <= 8 and (columns_list.index(self.column) + i) <= 7):
                # If piece found going upward right, break from loop
                if game_rep[str(self.row + i)][str(self.board)][columns_list[columns_list.index(self.column) + i]] != "":
                    break

                ur.append(("B", self.board, self.column + str(self.row), columns_list[columns_list.index(self.column) + i] + str(self.row + i)))

        ul = []

        for i in range(1,8):
            if ((self.row + i) <= 8 and (columns_list.index(self.column) - i) >= 0):
                # If piece found going upward left, break from loop
                if game_rep[str(self.row + i)][str(self.board)][columns_list[columns_list.index(self.column) - i]] != "":
                    break

                ul.append(("B", self.board, self.column + str(self.row), columns_list[columns_list.index(self.column) - i] + str(self.row + i)))

        dr = []

        for i in range(1,8):
            if ((self.row - i) >= 1 and (columns_list.index(self.column) + i) <= 7):
                # If piece found going upward right, break from loop
                if game_rep[str(self.row - i)][str(self.board)][columns_list[columns_list.index(self.column) + i]] != "":
                    break

                dr.append(("B", self.board, self.column + str(self.row), columns_list[columns_list.index(self.column) + i] + str(self.row - i)))

        dl = []

        for i in range(1,8):
            if ((self.row - i) >= 1 and (columns_list.index(self.column) - i) >= 0):
                # If piece found going upward right, break from loop
                if game_rep[str(self.row - i)][str(self.board)][columns_list[columns_list.index(self.column) - i]] != "":
                    break

                dl.append(("B", self.board, self.column + str(self.row), columns_list[columns_list.index(self.column) - i] + str(self.row - i)))

        my_moves = ur + ul + dr + dl
        
        dest_board = self.board == 1 and 2 or 1
        my_final_moves = []

        # Check if opposite board is empty
        for move in my_moves:
            destination = move[-1]
            if game_rep[destination[1]][str(dest_board)][destination[0]] == "":
                my_final_moves.append(move)

        # print my_final_moves
        return my_final_moves