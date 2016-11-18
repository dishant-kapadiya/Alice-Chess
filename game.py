from player import *

class Game:

    def __init__(self):

        self.players = []

        self.initialize_game()

    def initialize_game(self):

        player_1 = Player("Black")
        player_2 = Player("White")

        self.players.append(player_1)
        self.players.append(player_2)

    def get_game_state(self):

        """ Returns the current state of the game as a unicode string when printed shows
            the board and all the pieces according to the current state of the game.
        """

        pieces = u''.join(unichr(9812 + x) for x in range(12))
        pieces = u' ' + pieces
        allbox = u''.join(unichr(9472 + x) for x in range(200))
        box = [ allbox[i] for i in (2, 0, 12, 16, 20, 24, 44, 52, 28, 36, 60) ]
        (vbar, hbar, ul, ur, ll, lr, nt, st, wt, et, plus) = box
        h3 = hbar * 3

        topline = (ul + (h3 + nt) * 7 + h3 + ur) + " " + (ul + (h3 + nt) * 7 + h3 + ur)
        midline = (wt + (h3 + plus) * 7 + h3 + et) + " " + (wt + (h3 + plus) * 7 + h3 + et)
        botline = (ll + (h3 + st) * 7 + h3 + lr) + " " + (ll + (h3 + st) * 7 + h3 + lr)

        tpl = u' {0} ' + vbar

        def inter(*args):
            """ Return a unicode string with a line of the chessboard.
                args are 16 integers with the values
                0 : empty square
                1 : White King Black : 7
                2 : White Queen Black : 8
                3 : White Rook Black : 9
                4 : White Bishop Black : 10
                5 : White Knight Black : 11
                6 : White Pawn Black : 12
            """
            assert len(args) == 16
            line = vbar + u''.join((tpl.format(pieces[a]) for a in args[:8]))
            line = line + " " + vbar + u''.join((tpl.format(pieces[a]) for a in args[8:]))
            return line

        def _game(position):
            yield topline
            yield inter(*position[-1])
            for row in position[6::-1]:
                yield midline
                yield inter(*row)
            yield botline

        game = lambda squares: "\n".join(_game(squares))
        game.__doc__ = """Return the chessboard as a string for a given position.
            position is a list of 8 lists or tuples of length 8 containing integers
        """

        game_list = []
        # Alice chess board representation as a dictionary: alice_board[row][board][column]
        alice_board = {}

        for row in range(1,9):

            piece_list = []
            piece_tuple = ()

            alice_board[str(row)] = {}

            for board in range(1,3):

                alice_board[str(row)][str(board)] = {}

                for column in ["a", "b", "c", "d", "e", "f", "g", "h"]:

                    flag_piece = False

                    for player in self.players:

                        if player.color == "White":
                            indent_no = 0
                            alice_board_color = "w"
                        else:
                            indent_no = 6
                            alice_board_color = "b"

                        for piece in player.arsenal:
                            if (piece.type == "P" and piece.row == row and piece.board == board and piece.column == column):
                                piece_list.append(indent_no + 6)
                                alice_board[str(row)][str(board)][column] = alice_board_color + piece.type
                                flag_piece = True
                            elif (piece.type == "R" and piece.row == row and piece.board == board and piece.column == column):
                                piece_list.append(indent_no + 3)
                                alice_board[str(row)][str(board)][column] = alice_board_color + piece.type
                                flag_piece = True
                            elif (piece.type == "N" and piece.row == row and piece.board == board and piece.column == column):
                                piece_list.append(indent_no + 5)
                                alice_board[str(row)][str(board)][column] = alice_board_color + piece.type
                                flag_piece = True
                            elif (piece.type == "B" and piece.row == row and piece.board == board and piece.column == column):
                                piece_list.append(indent_no + 4)
                                alice_board[str(row)][str(board)][column] = alice_board_color + piece.type
                                flag_piece = True
                            elif (piece.type == "Q" and piece.row == row and piece.board == board and piece.column == column):
                                piece_list.append(indent_no + 2)
                                alice_board[str(row)][str(board)][column] = alice_board_color + piece.type
                                flag_piece = True
                            elif (piece.type == "K" and piece.row == row and piece.board == board and piece.column == column):
                                piece_list.append(indent_no + 1)
                                alice_board[str(row)][str(board)][column] = alice_board_color + piece.type
                                flag_piece = True
                            else:
                                continue

                    if flag_piece == False:
                        piece_list.append(0)
                        alice_board[str(row)][str(board)][column] = ""
            
            piece_tuple = tuple(piece_list)
            game_list.append(piece_tuple)

        print game(game_list)
        return alice_board

    def receive_move(self, msg):

        msg_list = msg.split()

        len(msg_list) == 8
        
        move_color = msg_list[0]
        move_piece = msg_list[2]
        move_board = msg_list[4]
        move_from = msg_list[5]
        move_to = msg_list[7]

        dest_board = move_board == "1" and 2 or 1
        opponent_color = move_color == "white" and "b" or "w"

        for player in self.players:
            if player.color != move_color.capitalize():
                for piece in player.arsenal:
                    if piece.board == int(move_board) and piece.row == int(move_to[1]) and piece.column == move_to[0]:
                        player.kill_peice(piece)

            else:
                for piece in player.arsenal:
                    if piece.type == move_piece and piece.board == int(move_board) and piece.column == move_from[0] and piece.row == int(move_from[1]):
                        piece.make_move(move_to)