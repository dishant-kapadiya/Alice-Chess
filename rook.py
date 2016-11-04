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

        for i in range(1,8):
            if ((self.row + i) < 9):
                # If piece found going upwards, break from loop
                if game_rep[self.row + i][self.board][self.column] != "":
                    break

                u.append(("R", self.board, self.column + str(self.row), self.column + str(self.row + i)))

        d = []

        for i in range(1,8):
            if ((self.row - i) > 0):
                # If piece found going downwards, break from loop
                if game_rep[self.row - i][self.board][self.column] != "":
                    break

                u.append(("R", self.board, self.column + str(self.row), self.column + str(self.row - i)))

        # r = []

        # for i in range(1:8):
        #     if ((self.column - i) > 0):
        #         # If piece found going downwards, break from loop
        #         if game_rep[self.row - i][self.board][self.column] != "":
        #             break

        #         u.append(("R", self.board, self.column + str(self.row), self.column + str(self.row - i)))

        print u + d