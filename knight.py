from piece import Piece

class Knight(Piece):

    def __init__(self, board, row, column):

        Piece.__init__(self, board, row, column)
        self.type = "N"

    def valid_moves(self, my_color, game_rep):
        
        # TODO: Take into account moves that kill opponent piece
        
        # List of tuples indicating (Piece, board_position, start_position, end_position)
        my_moves = []
        columns_list = ["a", "b", "c", "d", "e", "f", "g", "h"]

        # Check maximum row
        if self.row < 7:
            # Check maximum column
            if columns_list.index(self.column) < 7:
                my_moves.append(("N", self.board, self.column + str(self.row), columns_list[columns_list.index(self.column) + 1] + str(self.row + 2)))
            
            # Check minimum column
            if columns_list.index(self.column) > 0:
                my_moves.append(("N", self.board, self.column + str(self.row), columns_list[columns_list.index(self.column) - 1] + str(self.row + 2)))

        # Check maximum column
        if columns_list.index(self.column) < 6:
            # Check maximum row
            if self.row < 8:
                my_moves.append(("N", self.board, self.column + str(self.row), columns_list[columns_list.index(self.column) + 2] + str(self.row + 1)))
            
            # Check minimum row
            if self.row > 1:
                my_moves.append(("N", self.board, self.column + str(self.row), columns_list[columns_list.index(self.column) + 2] + str(self.row - 1)))

        # Check minimum row
        if self.row > 2:
            # Check maximum column
            if columns_list.index(self.column) < 7:
                my_moves.append(("N", self.board, self.column + str(self.row), columns_list[columns_list.index(self.column) + 1] + str(self.row - 2)))
            
            # Check minimum column
            if columns_list.index(self.column) > 0:
                my_moves.append(("N", self.board, self.column + str(self.row), columns_list[columns_list.index(self.column) - 1] + str(self.row - 2)))

        # Check minimum column
        if columns_list.index(self.column) > 1:
            # Check maximum row
            if self.row < 8:
                my_moves.append(("N", self.board, self.column + str(self.row), columns_list[columns_list.index(self.column) - 2] + str(self.row + 1)))
            
            # Check minimum row
            if self.row > 1:
                my_moves.append(("N", self.board, self.column + str(self.row), columns_list[columns_list.index(self.column) - 2] + str(self.row - 1)))

        dest_board = self.board == 1 and 2 or 1
        my_final_moves = []

        # Check if opposite board is empty
        for move in my_moves:
            destination = move[-1]
            if game_rep[destination[1]][str(dest_board)][destination[0]] == "" and game_rep[destination[1]][str(self.board)][destination[0]] == "":
                my_final_moves.append(move)
                
        return my_final_moves