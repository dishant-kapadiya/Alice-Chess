from enum import Enum
import sys
import random


class Position:
    def __init__(self, board, index):
        self.board = board
        self.index = index

    def __eq__(self, other):
        if not isinstance(other, Position):
            return False
        return self.board == other.board and self.index == other.index

    def __add__(self, other):
        if isinstance(other, int):
            Answer = Position(self.board, self.index + other)
            return Answer
        else:
            raise Exception("Value Error: "+str(other)+" cannot be added.")

    def __radd__(self, other):
        if isinstance(other, int):
            Answer = Position(self.board, self.index + other)
            return Answer
        else:
            raise Exception("Value Error: " + str(other) + " cannot be added.")

    def __repr__(self):
        return self.board.value + "(" + Position.int_to_alg(self.index) + ")"

    def same_position_in_next_board(self): #flip_board can be a name
        return Position(self.board.next_board(), self.index)

    @staticmethod
    def int_to_alg(num):
        chess_file = ["a", "b", "c", "d", "e", "f", "g", "h"]
        row = 8 - int(num / 8)
        column = chess_file[num % 8]
        return str(column) + str(row)

    @staticmethod
    def alg_to_int(notation):
        chess_file = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        return chess_file[notation[0]] + (8 - int(notation[1])) * 8


class BoardIndex(Enum):
    Board_One = "1"
    Board_Two = "2"

    def next_board(self):
        return BoardIndex.Board_One if self.value == "2" else BoardIndex.Board_Two

    def __str__(self):
        return BoardIndex.Board_One.value if self == BoardIndex.Board_One else BoardIndex.Board_Two.value


class PlayerColor(Enum):
    White = "white"
    Black = "black"

    @staticmethod
    def opponent(color, white_player, black_player):
        return black_player if color == PlayerColor.White else white_player


class BoardProperties:
    NUM_TILES = 64
    NUM_TILES_PER_ROW = 8
    NUM_BOARD = 2

    @staticmethod
    def init_column(column):
        grid = [False] * BoardProperties.NUM_TILES
        for i in range(0 + column, BoardProperties.NUM_TILES, BoardProperties.NUM_TILES_PER_ROW):
            grid[i] = True
        return grid

    @staticmethod
    def init_row(row):
        grid = [False] * BoardProperties.NUM_TILES
        for i in range(BoardProperties.NUM_TILES_PER_ROW * row,
                       BoardProperties.NUM_TILES_PER_ROW * (row + 1)):
            grid[i] = True
        return grid

    def __init__(self):
        self.FIRST_COLUMN = self.init_column(0)
        self.SECOND_COLUMN = self.init_column(1)
        self.SEVENTH_COLUMN = self.init_column(6)
        self.EIGHTH_COLUMN = self.init_column(7)
        self.SECOND_ROW = self.init_row(1)
        self.SEVENTH_ROW = self.init_row(6)

    @staticmethod
    def is_vaild_tile_coordinate(new_coordinate):
        return 0 <= new_coordinate.index < BoardProperties.NUM_TILES and \
               1 <= int(new_coordinate.board.value) <= BoardProperties.NUM_BOARD

BoardProperties = BoardProperties()


class Tile:
    def __init__(self, coordinate):
        self.coordinate = coordinate

    def is_occupied(self):
        pass

    def get_piece(self):
        pass

    @staticmethod
    def all_possible_tiles():
        temp = []
        for i in range(64):
            temp.append(EmptyTile(i))
        return dict(enumerate(temp))


class EmptyTile(Tile):
    def __init__(self, coordinate):
        Tile.__init__(self, coordinate)

    def is_occupied(self):
        return False

    def __str__(self):
        return "-"

    def get_piece(self):
        return None


class OccupiedTile(Tile):
    def __init__(self, coordinate, piece):
        Tile.__init__(self, coordinate)
        self.piece = piece

    def is_occupied(self):
        return True

    def __str__(self):
        return str(self.piece)

    def get_piece(self):
        return self.piece


class Board:
    def __init__(self, builder):
        self.game_board1 = Board.create_game_board(builder.board_config1)
        self.game_board2 = Board.create_game_board(builder.board_config2)
        self.white_piece = Board.calculate_active_piece(self.game_board1, PlayerColor.White) + \
                           Board.calculate_active_piece(self.game_board2, PlayerColor.White)
        self.black_piece = Board.calculate_active_piece(self.game_board1, PlayerColor.Black) + \
                           Board.calculate_active_piece(self.game_board2, PlayerColor.Black)
        self.white_legal_moves = self.calculate_moves(self.white_piece)
        self.black_legal_moves = self.calculate_moves(self.black_piece)
        self.white_player = WhitePlayer(self, self.white_legal_moves,
                                        self.black_legal_moves)
        self.black_player = BlackPlayer(self, self.black_legal_moves,
                                        self.white_legal_moves)
        self.current_player = PlayerColor.opponent(builder.next_move_maker,
                                                   self.white_player,
                                                   self.black_player)

    @staticmethod
    def create_game_board(builder):
        board_tiles = [None] * BoardProperties.NUM_TILES
        for i in range(BoardProperties.NUM_TILES):
            if isinstance(builder[i], Piece):
                board_tiles[i] = OccupiedTile(i, builder[i])
            else:
                board_tiles[i] = EmptyTile(i)
        return board_tiles

    def get_tile(self, coordinate):
        if coordinate.board == BoardIndex.Board_One:
            game_board = self.game_board1
        else:
            game_board = self.game_board2
        return game_board[coordinate.index]

    @staticmethod
    def create_standard_board():
        builder = BoardBuilder()
        # Black Arsenal
        builder.set_piece(Rook(Position(BoardIndex.Board_One, 0), PlayerColor.Black))
        builder.set_piece(Knight(Position(BoardIndex.Board_One, 1), PlayerColor.Black))
        builder.set_piece(Bishop(Position(BoardIndex.Board_One, 2), PlayerColor.Black))
        builder.set_piece(Queen(Position(BoardIndex.Board_One, 3), PlayerColor.Black))
        builder.set_piece(King(Position(BoardIndex.Board_One, 4), PlayerColor.Black))
        builder.set_piece(Bishop(Position(BoardIndex.Board_One, 5), PlayerColor.Black))
        builder.set_piece(Knight(Position(BoardIndex.Board_One, 6), PlayerColor.Black))
        builder.set_piece(Rook(Position(BoardIndex.Board_One, 7), PlayerColor.Black))
        builder.set_piece(Pawn(Position(BoardIndex.Board_One, 8), PlayerColor.Black, True))
        builder.set_piece(Pawn(Position(BoardIndex.Board_One, 9), PlayerColor.Black, True))
        builder.set_piece(Pawn(Position(BoardIndex.Board_One, 10), PlayerColor.Black, True))
        builder.set_piece(Pawn(Position(BoardIndex.Board_One, 11), PlayerColor.Black, True))
        builder.set_piece(Pawn(Position(BoardIndex.Board_One, 12), PlayerColor.Black, True))
        builder.set_piece(Pawn(Position(BoardIndex.Board_One, 13), PlayerColor.Black, True))
        builder.set_piece(Pawn(Position(BoardIndex.Board_One, 14), PlayerColor.Black, True))
        builder.set_piece(Pawn(Position(BoardIndex.Board_One, 15), PlayerColor.Black, True))
        # White Arsenal
        builder.set_piece(Pawn(Position(BoardIndex.Board_One, 48), PlayerColor.White, True))
        builder.set_piece(Pawn(Position(BoardIndex.Board_One, 49), PlayerColor.White, True))
        builder.set_piece(Pawn(Position(BoardIndex.Board_One, 50), PlayerColor.White, True))
        builder.set_piece(Pawn(Position(BoardIndex.Board_One, 51), PlayerColor.White, True))
        builder.set_piece(Pawn(Position(BoardIndex.Board_One, 52), PlayerColor.White, True))
        builder.set_piece(Pawn(Position(BoardIndex.Board_One, 53), PlayerColor.White, True))
        builder.set_piece(Pawn(Position(BoardIndex.Board_One, 54), PlayerColor.White, True))
        builder.set_piece(Pawn(Position(BoardIndex.Board_One, 55), PlayerColor.White, True))
        builder.set_piece(Rook(Position(BoardIndex.Board_One, 56), PlayerColor.White))
        builder.set_piece(Knight(Position(BoardIndex.Board_One, 57), PlayerColor.White))
        builder.set_piece(Bishop(Position(BoardIndex.Board_One, 58), PlayerColor.White))
        builder.set_piece(Queen(Position(BoardIndex.Board_One, 59), PlayerColor.White))
        builder.set_piece(King(Position(BoardIndex.Board_One, 60), PlayerColor.White))
        builder.set_piece(Bishop(Position(BoardIndex.Board_One, 61), PlayerColor.White))
        builder.set_piece(Knight(Position(BoardIndex.Board_One, 62), PlayerColor.White))
        builder.set_piece(Rook(Position(BoardIndex.Board_One, 63), PlayerColor.White))
        builder.set_next_move_maker(PlayerColor.Black)
        return builder.build()

    @staticmethod
    def calculate_active_piece(gameboard, color):
        pieces = []
        for tile in gameboard:
            if tile.is_occupied():
                piece = tile.get_piece()
                if piece.color == color:
                    pieces.append(piece)

        return pieces

    def calculate_moves(self, arsenal):
        list_of_moves = []
        for piece in arsenal:
            list_of_moves += piece.valid_moves(self)
        return list_of_moves

    def __repr__(self):
        str_rep = "8: "
        for tile in self.game_board1:
            str_rep += "{:3}".format(str(tile))
            if (tile.coordinate + 1) % BoardProperties.NUM_TILES_PER_ROW == 0:
                row = (tile.coordinate + 1) / BoardProperties.NUM_TILES_PER_ROW
                str_rep += "\n" + str(8 - row) + ": "
        list1 = str_rep.split("\n")[:-1]
        str_rep = ""
        for tile in self.game_board2:
            str_rep += "{:3}".format(str(tile))
            if (tile.coordinate + 1) % BoardProperties.NUM_TILES_PER_ROW == 0:
                str_rep += "\n"
        list2 = str_rep.split("\n")
        final_str = ""
        for temp in zip(list1, list2):
            final_str += "{0}| {1}".format(temp[0], temp[1])
            final_str += "\n"
        last_line = "   a  b  c  d  e  f  g  h  | a  b  c  d  e  f  g  h  "
        return final_str + last_line

    def get_all_legal_moves(self):
        return self.white_legal_moves + self.black_legal_moves


class BoardBuilder:
    board_config1 = {}
    board_config2 = {}
    next_move_maker = None

    def __init__(self):
        for i in range(BoardProperties.NUM_TILES):
            self.board_config1[i] = None
            self.board_config2[i] = None
        self.next_move_maker = None

    def set_piece(self, piece):
        if piece.position.board == BoardIndex.Board_One:
            self.board_config1[piece.position.index] = piece
        else:
            self.board_config2[piece.position.index] = piece

    def set_next_move_maker(self, next_move_maker):
        self.next_move_maker = next_move_maker

    def build(self):
        return Board(self)


class Piece:
    __doc__ = """Abstract class for different pieces in the game.
                 Implements methods for generating valid moves in current gamestate."""

    def __init__(self, position, color):
        self.position = position
        self.color = color
        self.is_first_move = False

    def valid_moves(self, game_config):
        pass

    def move_piece(self, move):
        pass

    def __eq__(self, other):
        if not (self.__class__ == other.__class__ and isinstance(other, Piece)):
            return False

        return self.position == other.position and \
               self.color == other.color and \
               self.is_first_move == other.is_first_move


class King(Piece):
    __doc__ = """Implements a King class by inheriting Piece class."""
    valid_move_offsets = [-9, -8, -7, -1, 1, 7, 8, 9]

    def __init__(self, position, color):
        Piece.__init__(self, position, color)
        self.value = 13

    def __add__(self, other):
        return self.value + other

    def __radd__(self, other):
        return self.value + other

    def __str__(self):
        return "K" if self.color == PlayerColor.White else "k"

    def move_piece(self, move):
        return King(move.destination, move.piece.color)

    def valid_moves(self, game_config):
        list_of_moves = []
        for offset in King.valid_move_offsets:
            destination_position = Position(self.position.board.next_board(),
                                            self.position.index + offset)
            if BoardProperties.is_vaild_tile_coordinate(destination_position):
                if King.in_first_column_exception(offset, self.position.index) or \
                        King.in_eighth_column_exception(offset, self.position.index):
                    continue
                tile_in_next_board = game_config.get_tile(destination_position)
                position_in_same_board = Position.same_position_in_next_board(destination_position)
                tile_in_this_board = game_config.get_tile(position_in_same_board)
                if not tile_in_next_board.is_occupied():
                    if not tile_in_this_board.is_occupied():
                        list_of_moves.append(
                            MajorMove(game_config, self, destination_position))
                    else:
                        piece_at_destination = tile_in_this_board.get_piece()
                        piece_color = piece_at_destination.color
                        if piece_color != self.color:
                            list_of_moves.append(AttackMove(game_config, self, destination_position, piece_at_destination))
                        break
        return list_of_moves

    @staticmethod
    def in_first_column_exception(offset, destination_position):
        return BoardProperties.FIRST_COLUMN[destination_position] and ((offset == -9) or
                                                                       (offset == -1) or
                                                                       (offset == 7))

    @staticmethod
    def in_eighth_column_exception(offset, destination_position):
        return BoardProperties.EIGHTH_COLUMN[destination_position] and ((offset == -7) or
                                                                        (offset == 1) or
                                                                        (offset == 9))


class Queen(Piece):
    __doc__ = """Implements a Queen class by inheriting Piece class."""
    valid_move_offsets = [-9, -8, -7, -1, 1, 7, 8, 9]

    def __init__(self, position, color):
        Piece.__init__(self, position, color)
        self.value = 12

    def __add__(self, other):
        return self.value + other

    def __radd__(self, other):
        return self.value + other

    def __str__(self):
        return "Q" if self.color == PlayerColor.White else "q"

    def move_piece(self, move):
        return Queen(move.destination, move.piece.color)

    def valid_moves(self, game_config):
        list_of_moves = []
        for offset in Queen.valid_move_offsets:
            destination_position = Position.same_position_in_next_board(self.position)
            while BoardProperties.is_vaild_tile_coordinate(destination_position):
                if Queen.in_first_column_exception(offset, destination_position.index) or \
                        Queen.in_eighth_column_exception(offset, destination_position.index):
                    break
                destination_position += offset
                if BoardProperties.is_vaild_tile_coordinate(destination_position):
                    # tile = game_config.get_tile(destination_position)
                    tile_in_next_board = game_config.get_tile(destination_position)
                    position_in_same_board = Position.same_position_in_next_board(destination_position)
                    tile_in_this_board = game_config.get_tile(position_in_same_board)
                    if not tile_in_next_board.is_occupied():
                        if not tile_in_this_board.is_occupied():
                            list_of_moves.append(
                                MajorMove(game_config, self, destination_position))
                        else:
                            piece_at_destination = tile_in_this_board.get_piece()
                            piece_color = piece_at_destination.color
                            if piece_color != self.color:
                                list_of_moves.append(
                                    AttackMove(game_config, self, destination_position,
                                               piece_at_destination))
                            break
        return list_of_moves

    @staticmethod
    def in_first_column_exception(offset, destination_position):
        return BoardProperties.FIRST_COLUMN[destination_position] and ((offset == -9) or
                                                                       (offset == -1) or
                                                                       (offset == 7))

    @staticmethod
    def in_eighth_column_exception(offset, destination_position):
        return BoardProperties.EIGHTH_COLUMN[destination_position] and ((offset == -7) or
                                                                        (offset == 1) or
                                                                        (offset == 9))


class Bishop(Piece):
    __doc__ = """Implements a Bishop class by inheriting Piece class."""
    valid_move_offsets = [-9, -7, 7, 9]

    def __init__(self, position, color):
        Piece.__init__(self, position, color)
        self.value = 11

    def __str__(self):
        return "B" if self.color == PlayerColor.White else "b"

    def __add__(self, other):
        return self.value + other

    def __radd__(self, other):
        return self.value + other

    def valid_moves(self, game_config):
        list_of_moves = []
        for offset in Bishop.valid_move_offsets:
            destination_position = Position.same_position_in_next_board(self.position)
            while BoardProperties.is_vaild_tile_coordinate(destination_position):
                if Bishop.in_first_column_exception(offset, destination_position.index) or \
                        Bishop.in_eighth_column_exception(offset, destination_position.index):
                    break
                destination_position += offset
                if BoardProperties.is_vaild_tile_coordinate(destination_position):
                    # tile = game_config.get_tile(destination_position)
                    tile_in_next_board = game_config.get_tile(destination_position)
                    position_in_same_board = Position.same_position_in_next_board(
                        destination_position)
                    tile_in_this_board = game_config.get_tile(position_in_same_board)
                    if not tile_in_next_board.is_occupied():
                        if not tile_in_this_board.is_occupied():
                            list_of_moves.append(
                                MajorMove(game_config, self, destination_position))
                        else:
                            piece_at_destination = tile_in_this_board.get_piece()
                            piece_color = piece_at_destination.color
                            if piece_color != self.color:
                                list_of_moves.append(
                                    AttackMove(game_config, self, destination_position,
                                              piece_at_destination))
                            break
        return list_of_moves

    def move_piece(self, move):
        return Bishop(move.destination, move.piece.color)

    @staticmethod
    def in_first_column_exception(offset, destination_position):
        return BoardProperties.FIRST_COLUMN[destination_position] and ((offset == -9) or
                                                                       (offset == 7))

    @staticmethod
    def in_eighth_column_exception(offset, destination_position):
        return BoardProperties.EIGHTH_COLUMN[destination_position] and ((offset == -7) or
                                                                        (offset == 9))


class Knight(Piece):
    __doc__ = """Implements a Knight class by inheriting Piece class."""
    valid_move_offsets = [-17, -15, -10, -6, 6, 10, 15, 17]

    def __init__(self, position, color):
        Piece.__init__(self, position, color)
        self.value = 10

    def __add__(self, other):
        return self.value + other

    def __radd__(self, other):
        return self.value + other

    def __str__(self):
        return "N" if self.color == PlayerColor.White else "n"

    def valid_moves(self, game_config):
        list_of_moves = []
        for offset in Knight.valid_move_offsets:
            destination_position = Position(self.position.board.next_board(),
                                            self.position.index + offset)
            if BoardProperties.is_vaild_tile_coordinate(destination_position):
                if Knight.in_first_column_exception(offset, self.position.index) or \
                        Knight.in_second_column_exception(offset, self.position.index) or \
                        Knight.in_seventh_column_exception(offset, self.position.index) or \
                        Knight.in_eighth_column_exception(offset, self.position.index):
                    continue
                tile_in_next_board = game_config.get_tile(destination_position)
                position_in_same_board = Position.same_position_in_next_board(destination_position)
                tile_in_this_board = game_config.get_tile(position_in_same_board)
                if not tile_in_next_board.is_occupied():
                    if not tile_in_this_board.is_occupied():
                        list_of_moves.append(
                            MajorMove(game_config, self, destination_position))
                    else:
                        piece_at_destination = tile_in_this_board.get_piece()
                        piece_color = piece_at_destination.color
                        if piece_color != self.color:
                            list_of_moves.append(
                                AttackMove(game_config, self, destination_position,
                                           piece_at_destination))
        return list_of_moves

    def move_piece(self, move):
        return Knight(move.destination, move.piece.color)

    @staticmethod
    def in_first_column_exception(offset, destination_position):
        return BoardProperties.FIRST_COLUMN[destination_position] and ((offset == -17) or
                                                                       (offset == -10) or
                                                                       (offset == 6) or
                                                                       (offset == 15))

    @staticmethod
    def in_second_column_exception(offset, destination_position):
        return BoardProperties.SECOND_COLUMN[destination_position] and ((offset == -10) or
                                                                        (offset == 6))

    @staticmethod
    def in_seventh_column_exception(offset, destination_position):
        return BoardProperties.SEVENTH_COLUMN[destination_position] and ((offset == -6) or
                                                                         (offset == 10))

    @staticmethod
    def in_eighth_column_exception(offset, destination_position):
        return BoardProperties.EIGHTH_COLUMN[destination_position] and ((offset == -15) or
                                                                        (offset == -6) or
                                                                        (offset == 10) or
                                                                        (offset == 17))


class Rook(Piece):
    __doc__ = """Implements a Rook class by inheriting Piece class."""
    valid_move_offsets = [-8, -1, 1, 8]

    def __init__(self, position, color):
        Piece.__init__(self, position, color)
        self.value = 11

    def __add__(self, other):
        return self.value + other

    def __radd__(self, other):
        return self.value + other

    def __str__(self):
        return "R" if self.color == PlayerColor.White else "r"

    def valid_moves(self, game_config):
        list_of_moves = []
        for offset in Rook.valid_move_offsets:
            destination_position = Position.same_position_in_next_board(self.position)
            while BoardProperties.is_vaild_tile_coordinate(destination_position):
                if Rook.in_first_column_exception(offset, destination_position.index) or \
                        Rook.in_eighth_column_exception(offset, destination_position.index):
                    break
                destination_position += offset
                if BoardProperties.is_vaild_tile_coordinate(destination_position):
                    # tile = game_config.get_tile(destination_position)
                    tile_in_next_board = game_config.get_tile(destination_position)
                    position_in_same_board = Position.same_position_in_next_board(destination_position)
                    tile_in_this_board = game_config.get_tile(position_in_same_board)
                    if not tile_in_next_board.is_occupied():
                        if not tile_in_this_board.is_occupied():
                            list_of_moves.append(MajorMove(game_config, self, destination_position))
                        else:
                            piece_at_destination = tile_in_this_board.get_piece()
                            piece_color = piece_at_destination.color
                            if piece_color != self.color:
                                list_of_moves.append(
                                    AttackMove(game_config, self, destination_position,
                                              piece_at_destination))
                            break
        return list_of_moves

    def move_piece(self, move):
        return Rook(move.destination, move.piece.color)

    @staticmethod
    def in_first_column_exception(offset, destination_position):
        return BoardProperties.FIRST_COLUMN[destination_position] and (offset == -1)

    @staticmethod
    def in_eighth_column_exception(offset, destination_position):
        return BoardProperties.EIGHTH_COLUMN[destination_position] and (offset == 1)


class Pawn(Piece):
    __doc__ = """Implements a Pawn class by inheriting Piece class."""
    valid_move_offsets = [8, 16, 7, 9]

    def __init__(self, position, color, is_first_move=False):
        Piece.__init__(self, position, color)
        self.value = 8
        self.is_first_move = is_first_move

    def __add__(self, other):
        return self.value + other

    def __radd__(self, other):
        return self.value + other

    def __str__(self):
        return "P" if self.color == PlayerColor.White else "p"

    def get_direction(self):
        return -1 if self.color == PlayerColor.White else 1

    def move_piece(self, move):
        return Pawn(move.destination, move.piece.color)

    def valid_moves(self, game_config):
        list_of_moves = []
        for offset in Pawn.valid_move_offsets:
            destination_position = Position(self.position.board.next_board(),
                                            self.position.index + (offset * self.get_direction()))
            if not BoardProperties.is_vaild_tile_coordinate(destination_position):
                continue
            if not game_config.get_tile(destination_position).is_occupied():
                tile_in_this_board = Position.same_position_in_next_board(destination_position)
                if offset == 8 and not game_config.get_tile(tile_in_this_board).is_occupied():
                    #TODO: Possibility of promotion. Needs better code(deal with Promotion)
                    list_of_moves.append(MajorMove(game_config, self, destination_position))
                elif offset == 16 and self.is_first_move:
                    if (self.color == PlayerColor.Black and
                            BoardProperties.SECOND_ROW[self.position.index]) \
                        or (self.color == PlayerColor.White and
                            BoardProperties.SEVENTH_ROW[self.position.index]):
                        first_tile_position = Position(self.position.board.next_board(),
                                                       self.position.index + (self.get_direction() * 8))
                        if not (game_config.get_tile(first_tile_position).is_occupied() or
                                game_config.get_tile(tile_in_this_board).is_occupied()):
                            list_of_moves.append(
                                MajorMove(game_config, self, destination_position))
                elif offset == 7 and not \
                        ((BoardProperties.EIGHTH_COLUMN[self.position.index] and self.color == PlayerColor.White) or
                        (BoardProperties.FIRST_COLUMN[self.position.index] and self.color == PlayerColor.Black)):
                    tile = game_config.get_tile(tile_in_this_board)
                    if tile.is_occupied():
                        piece_at_destination = tile.get_piece()
                        piece_color = piece_at_destination.color
                        if piece_color != self.color:
                            list_of_moves.append(
                                AttackMove(game_config, self, destination_position,
                                           piece_at_destination))

                elif offset == 9 and not \
                        ((BoardProperties.EIGHTH_COLUMN[self.position.index] and self.color == PlayerColor.Black) or
                        (BoardProperties.FIRST_COLUMN[self.position.index] and self.color == PlayerColor.White)):
                    tile = game_config.get_tile(tile_in_this_board)
                    if tile.is_occupied():
                        piece_at_destination = tile.get_piece()
                        piece_color = piece_at_destination.color
                        if piece_color != self.color:
                            list_of_moves.append(
                                AttackMove(game_config, self, destination_position,
                                           piece_at_destination))
        return list_of_moves


class Move:
    def __init__(self, board, piece, dest):
        self.board = board
        self.piece = piece
        self.destination = dest

    def __repr__(self):
        return str(self.piece) + " := " + str(self.piece.position) + "~>" + str(self.destination)

    def execute_move(self):
        builder = BoardBuilder()
        for piece in self.board.current_player.get_active_pieces():
            if not self.piece == piece:
                builder.set_piece(piece)
        for piece in self.board.current_player.get_opponent().get_active_pieces():
            builder.set_piece(piece)
        builder.set_piece(self.piece.move_piece(self))
        builder.set_next_move_maker(self.board.current_player.get_color())
        return builder.build()

    def __eq__(self, other):
        return self.destination == other.destination and self.piece == self.piece

    def current_coordinate(self):
        return self.piece.position

    def is_attack(self):
        pass

    def attacked_piece(self):
        pass


class MajorMove(Move):
    def __init__(self, board, piece, dest):
        Move.__init__(self, board, piece, dest)

    def is_attack(self):
        return False

    def attacked_piece(self):
        return None


class AttackMove(Move):
    def __init__(self, board, piece, dest, attacked_piece):
        Move.__init__(self, board, piece, dest)
        self.attacked_piece = attacked_piece

    def execute_move(self):
        builder = BoardBuilder()
        for piece in self.board.current_player.get_active_pieces():
            if not self.piece == piece:
                builder.set_piece(piece)
        for piece in self.board.current_player.get_opponent().get_active_pieces():
            if not piece.position.index == self.destination.index:
                builder.set_piece(piece)
        builder.set_piece(self.piece.move_piece(self))
        builder.set_next_move_maker(self.board.current_player.get_color())
        return builder.build()

    def is_attack(self):
        return True

    def attacked_piece(self):
        return self.attacked_piece

    def __eq__(self, other):
        return super.__eq__(other) and self.attacked_piece == other.attacked_piece


class MoveStatus(Enum):
    DONE = "Done"
    ILLEGAL_MOVE = "Illegal Move"
    LEAVES_KING_IN_CHECK = "Leaves King in check"


class MoveTransition:
    def __init__(self, board, move, move_status):
        self.transition_board = board
        self.move = move
        self.move_status = move_status


class Player:
    def __init__(self, board, legal_moves, opponent_moves):
        self.board = board
        self.player_king = self.establish_king()
        self.legal_moves = legal_moves
        self.opponents_moves = opponent_moves

    def establish_king(self):
        pass

    def is_legal_move(self, move):
        return move in self.legal_moves

    @staticmethod
    def calculate_attacks_on_tile(tile, opponents_moves):
        attacking_moves = []
        for move in opponents_moves:
            if tile == move.destination:
                attacking_moves.append(move)
        return attacking_moves

    def has_escape_moves(self):
        for move in self.legal_moves:
            transist = self.make_move(move)
            if transist.move_status == MoveStatus.DONE:
                return True
        return False

    def is_in_check(self):
        return not len(self.calculate_attacks_on_tile(self.player_king.position,
                                                      self.opponents_moves)) == 0

    def is_in_check_mate(self):
        return self.is_in_check() and not self.has_escape_moves()

    def is_in_stale_mate(self):
        return False

    def make_move(self, move):
        if not self.is_legal_move(move):
            return MoveTransition(self.board, move, MoveStatus.ILLEGAL_MOVE)
        transition_board = move.execute_move()
        king_attacks = Player.calculate_attacks_on_tile(transition_board.current_player.get_opponent().player_king.position,
                                                        transition_board.current_player.legal_moves)
        if len(king_attacks) != 0:
            return MoveTransition(self.board, move, MoveStatus.LEAVES_KING_IN_CHECK)
        return MoveTransition(transition_board, move, MoveStatus.DONE)


class WhitePlayer(Player):
    def __init__(self, board, my_moves, other_moves):
        Player.__init__(self, board, my_moves, other_moves)

    def establish_king(self):
        for piece in self.get_active_pieces():
            if isinstance(piece, King):
                piece.__class__ = King
                return piece
        raise Exception("Should not reach here now!")

    def get_active_pieces(self):
        return self.board.white_piece

    @staticmethod
    def get_color():
        return PlayerColor.White

    def get_opponent(self):
        return self.board.black_player


class BlackPlayer(Player):
    def __init__(self, board, my_moves, other_moves):
        Player.__init__(self, board, my_moves, other_moves)

    def establish_king(self):
        for piece in self.get_active_pieces():
            if isinstance(piece, King):
                piece.__class__ = King
                return piece
        raise Exception("Should not reach here now!")

    def get_active_pieces(self):
        return self.board.black_piece

    @staticmethod
    def get_color():
        return PlayerColor.Black

    def get_opponent(self):
        return self.board.white_player

########################################################################################################################

"""Generating sequence of meanigful messages"""

# """


def generate_move_sentence(move):
    list_of_values = list()
    list_of_values.append(my_team_color)
    list_of_values.append("moves")
    list_of_values.append(str(move.piece).upper())
    list_of_values.append("from")
    list_of_values.append(move.piece.position.board.value)
    list_of_values.append(Position.int_to_alg(move.piece.position.index))
    list_of_values.append("to")
    list_of_values.append(Position.int_to_alg(move.destination.index))
    return " ".join(list_of_values) + "\n"


def choose_move():
    player = game.current_player
    player_legal_moves = player.legal_moves
    #TODO: come up with better stratagies for choosing a move
    move_index = random.randrange(len(player_legal_moves))
    return player_legal_moves[move_index]


def make_move(move):
    move_transition = game.current_player.make_move(move)
    if not move_transition.move_status == MoveStatus.DONE:
        sys.stdout.write(my_team + " surrenders\n")
        sys.exit(0)
    return move_transition.transition_board


def find_move(moves, piece, board, source, destination):
    for move in moves:
        if str(move.piece).upper() == piece \
                and move.piece.position.board.value == board \
                and move.piece.position.index == Position.alg_to_int(source) \
                and move.destination.index == Position.alg_to_int(destination):
            return move









end = False
game = Board.create_standard_board()
my_team_color = None
my_team = None
while not end:
    input_message = raw_input()

    if "you are " in input_message:
        # set color and skip outputting a message if necessary
        if "black" in input_message:
            my_team_color = PlayerColor.Black.value
            my_team = game.black_player
            continue
        else:
            my_team_color = PlayerColor.White.value
            my_team = game.white_player
            move = choose_move()
            game = make_move(move)
            sys.stdout.write(generate_move_sentence(move))

    elif "moves" in input_message:
        message = input_message.split()
        assert game.current_player.get_color().value == message[0]
        move = find_move(game.current_player.legal_moves, message[2], message[4], message[5], message[7])
        game = make_move(move)
        if game.current_player.get_color() == my_team.get_color():
            move = choose_move()
            game = make_move(move)
            sys.stdout.write(generate_move_sentence(move))
        else:
            sys.stdout.write(my_team_color.value + " surrenders\n")
    print game

    # elif "wins" in input_message or "loses" in input_message or "drawn" in input_message:
    #     end = True
    #     sys.exit(0)
    #
    # elif " offers draw" in input_message:
    #     sys.stdout.write(my_team_color + " accepts draw\n")
    #     end = True
    #     sys.exit(0)
    #
    # # msg_count += 1
    # # other_team = game.players[0] if my_team != game.players[0] else game.players[1]
    # # print evaluate_game_state(my_team, other_team)
    # sys.stdin.flush()
    # sys.stdout.flush()

# """
