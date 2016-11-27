"""Entry point in the program and is used as a player"""
from enum import Enum
import sys
import random

class PlayerColor(Enum):
    White = "white"
    Black = "black"

    @staticmethod
    def opponent(color, white_player, black_player):
        return black_player if color == PlayerColor.White else white_player


class BoardUtils:
    NUM_TILES = 64
    NUM_TILES_PER_ROW = 8

    @staticmethod
    def init_column(column):
        grid = [False] * BoardUtils.NUM_TILES
        for i in range(0 + column, BoardUtils.NUM_TILES, BoardUtils.NUM_TILES_PER_ROW):
            grid[i] = True
        return grid

    @staticmethod
    def init_row(row):
        grid = [False] * BoardUtils.NUM_TILES
        for i in range(BoardUtils.NUM_TILES_PER_ROW * row,
                       BoardUtils.NUM_TILES_PER_ROW * (row + 1)):
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
        return 0 <= new_coordinate < BoardUtils.NUM_TILES

BoardUtils = BoardUtils()


class Board:
    def __init__(self, builder):
        self.game_board = Board.create_game_board(builder)
        self.white_piece = self.calculate_active_piece(self.game_board, PlayerColor.White)
        self.black_piece = self.calculate_active_piece(self.game_board, PlayerColor.Black)
        self.white_legal_moves = self.calculate_moves(self.white_piece)
        self.black_legal_moves = self.calculate_moves(self.black_piece)
        self.white_player = WhitePlayer(self, self.white_legal_moves,
                                        self.black_legal_moves)
        self.black_player = BlackPlayer(self, self.white_legal_moves,
                                        self.black_legal_moves)
        self.current_player = PlayerColor.opponent(builder.next_move_maker,
                                                   self.white_player,
                                                   self.black_player)

    @staticmethod
    def create_game_board(builder):
        board_tiles = [None] * BoardUtils.NUM_TILES
        for i in range(BoardUtils.NUM_TILES):
            if isinstance(builder.board_config[i], Piece):
                board_tiles[i] = OccupiedTile(i, builder.board_config[i])
            else:
                board_tiles[i] = EmptyTile(i)
        return board_tiles

    def get_tile(self, coordinate):
        return self.game_board[coordinate]

    def calculate_active_piece(self, gameboard, color):
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
        str_rep = ""
        for tile in self.game_board:
            str_rep += "{:3}".format(str(tile))
            if (tile.coordinate + 1) % BoardUtils.NUM_TILES_PER_ROW == 0:
                str_rep += "\n"

        return str_rep

    def get_all_legal_moves(self):
        return self.white_legal_moves + self.black_legal_moves

    @staticmethod
    def create_standard_board():
        builder = BoardBuilder()
        # Black Arsenal
        builder.set_piece(Rook(0, PlayerColor.Black))
        builder.set_piece(Knight(1, PlayerColor.Black))
        builder.set_piece(Bishop(2, PlayerColor.Black))
        builder.set_piece(Queen(3, PlayerColor.Black))
        builder.set_piece(King(4, PlayerColor.Black))
        builder.set_piece(Bishop(5, PlayerColor.Black))
        builder.set_piece(Knight(6, PlayerColor.Black))
        builder.set_piece(Rook(7, PlayerColor.Black))
        builder.set_piece(Pawn(8, PlayerColor.Black, is_first_move=True))
        builder.set_piece(Pawn(9, PlayerColor.Black, is_first_move=True))
        builder.set_piece(Pawn(10, PlayerColor.Black, is_first_move=True))
        builder.set_piece(Pawn(11, PlayerColor.Black, is_first_move=True))
        builder.set_piece(Pawn(12, PlayerColor.Black, is_first_move=True))
        builder.set_piece(Pawn(13, PlayerColor.Black, is_first_move=True))
        builder.set_piece(Pawn(14, PlayerColor.Black, is_first_move=True))
        builder.set_piece(Pawn(15, PlayerColor.Black, is_first_move=True))
        # White Arsenal
        builder.set_piece(Pawn(48, PlayerColor.White, is_first_move=True))
        builder.set_piece(Pawn(49, PlayerColor.White, is_first_move=True))
        builder.set_piece(Pawn(50, PlayerColor.White, is_first_move=True))
        builder.set_piece(Pawn(51, PlayerColor.White, is_first_move=True))
        builder.set_piece(Pawn(52, PlayerColor.White, is_first_move=True))
        builder.set_piece(Pawn(53, PlayerColor.White, is_first_move=True))
        builder.set_piece(Pawn(54, PlayerColor.White, is_first_move=True))
        builder.set_piece(Pawn(55, PlayerColor.White, is_first_move=True))
        builder.set_piece(Rook(56, PlayerColor.White))
        builder.set_piece(Knight(57, PlayerColor.White))
        builder.set_piece(Bishop(58, PlayerColor.White))
        builder.set_piece(Queen(59, PlayerColor.White))
        builder.set_piece(King(60, PlayerColor.White))
        builder.set_piece(Bishop(61, PlayerColor.White))
        builder.set_piece(Knight(62, PlayerColor.White))
        builder.set_piece(Rook(63, PlayerColor.White))

        builder.set_next_move_maker(PlayerColor.Black)

        return builder.build()


class BoardBuilder:
    board_config = {}
    next_move_maker = None

    def __init__(self):
        for i in range(BoardUtils.NUM_TILES):
            self.board_config[i] = None
        self.next_move_maker = None

    def set_piece(self, piece):
        self.board_config[piece.position] = piece

    def set_next_move_maker(self, next_move_maker):
        self.next_move_maker = next_move_maker

    def build(self):
        return Board(self)


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
    def __init__(self, board, white_moves, black_moves):
        Player.__init__(self, board, white_moves, black_moves)

    def establish_king(self):
        for piece in self.get_active_pieces():
            if isinstance(piece, King):
                piece.__class__ = King
                return piece
        raise Exception("Should not reach here now!")

    def get_active_pieces(self):
        return self.board.white_piece

    def get_color(self):
        return PlayerColor.White

    def get_opponent(self):
        return self.board.black_player


class BlackPlayer(Player):
    def __init__(self, board, white_moves, black_moves):
        Player.__init__(self, board, black_moves, white_moves)

    def establish_king(self):
        for piece in self.get_active_pieces():
            if isinstance(piece, King):
                piece.__class__ = King
                return piece

        raise Exception("Should not reach here now!")

    def get_active_pieces(self):
        return self.board.black_piece

    def get_color(self):
        return PlayerColor.Black

    def get_opponent(self):
        return self.board.white_player


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

        if not self.__class__ == other.__class__:
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

    """
    def __add__(self, other):
        return self.value + other

    def __radd__(self, other):
        return self.value + other
    """

    def __str__(self):
        return "K" if self.color == PlayerColor.White else "k"

    def move_piece(self, move):
        return King(move.destination, move.piece.color)

    def valid_moves(self, game_config):
        list_of_moves = []
        for offset in Bishop.valid_move_offsets:
            destination_position = self.position + offset
            if BoardUtils.is_vaild_tile_coordinate(destination_position):
                if King.in_first_column_exception(offset, self.position) or \
                        King.in_eighth_column_exception(offset, self.position):
                    continue
                tile = game_config.get_tile(destination_position)
                if not tile.is_occupied():
                    list_of_moves.append(
                        MajorMove(game_config, self, destination_position))
                else:
                    piece_at_destination = tile.get_piece()
                    piece_color = piece_at_destination.color
                    if piece_color != self.color:
                        list_of_moves.append(
                            AttackMove(game_config, self, destination_position,
                                       piece_at_destination))
                    break
        return list_of_moves

    @staticmethod
    def in_first_column_exception(offset, destination_position):
        return BoardUtils.FIRST_COLUMN[destination_position] and ((offset == -9) or
                                                           (offset == -1) or
                                                           (offset == 7))

    @staticmethod
    def in_eighth_column_exception(offset, destination_position):
        return BoardUtils.EIGHTH_COLUMN[destination_position] and ((offset == -7) or
                                                            (offset == 1) or
                                                            (offset == 9))


class Queen(Piece):
    __doc__ = """Implements a Queen class by inheriting Piece class."""
    valid_move_offsets = [-9, -8, -7, -1, 1, 7, 8, 9]

    def __init__(self, position, color):
        Piece.__init__(self, position, color)
        self.value = 12
    """
    def __add__(self, other):
        return self.value + other

    def __radd__(self, other):
        return self.value + other
    """

    def __str__(self):
        return "Q" if self.color == PlayerColor.White else "q"

    def move_piece(self, move):
        return Queen(move.destination, move.piece.color)

    def valid_moves(self, game_config):
        list_of_moves = []
        for offset in Bishop.valid_move_offsets:
            destination_position = self.position
            while BoardUtils.is_vaild_tile_coordinate(destination_position):
                if Queen.in_first_column_exception(offset, destination_position) or \
                        Queen.in_eighth_column_exception(offset, destination_position):
                    break
                destination_position += offset
                if BoardUtils.is_vaild_tile_coordinate(destination_position):
                    tile = game_config.get_tile(destination_position)
                    if not tile.is_occupied():
                        list_of_moves.append(
                            MajorMove(game_config, self, destination_position))
                    else:
                        piece_at_destination = tile.get_piece()
                        piece_color = piece_at_destination.color
                        if piece_color != self.color:
                            list_of_moves.append(
                                AttackMove(game_config, self, destination_position,
                                           piece_at_destination))
                        break
        return list_of_moves

    @staticmethod
    def in_first_column_exception(offset, destination_position):
        return BoardUtils.FIRST_COLUMN[destination_position] and ((offset == -9) or
                                                           (offset == -1) or
                                                           (offset == 7))

    @staticmethod
    def in_eighth_column_exception(offset, destination_position):
        return BoardUtils.EIGHTH_COLUMN[destination_position] and ((offset == -7) or
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

    """
    def __add__(self, other):
        return self.value + other

    def __radd__(self, other):
        return self.value + other
    """

    def valid_moves(self, game_config):
        list_of_moves = []
        for offset in Bishop.valid_move_offsets:
            destination_position = self.position
            while BoardUtils.is_vaild_tile_coordinate(destination_position):
                if Bishop.in_first_column_exception(offset, destination_position) or \
                        Bishop.in_eighth_column_exception(offset, destination_position):
                    break
                destination_position += offset
                if BoardUtils.is_vaild_tile_coordinate(destination_position):
                    tile = game_config.get_tile(destination_position)
                    if not tile.is_occupied():
                        list_of_moves.append(
                            MajorMove(game_config, self, destination_position))
                    else:
                        piece_at_destination = tile.get_piece()
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
        return BoardUtils.FIRST_COLUMN[destination_position] and ((offset == -9) or
                                                           (offset == 7))

    @staticmethod
    def in_eighth_column_exception(offset, destination_position):
        return BoardUtils.EIGHTH_COLUMN[destination_position] and ((offset == -7) or
                                                            (offset == 9))


class Knight(Piece):
    __doc__ = """Implements a Knight class by inheriting Piece class."""
    valid_move_offsets = [-17, -15, -10, -6, 6, 10, 15, 17]
    def __init__(self, position, color):
        Piece.__init__(self, position, color)
        self.value = 10

    """
    def __add__(self, other):
        return self.value + other

    def __radd__(self, other):
        return self.value + other
    """

    def __str__(self):
        return "N" if self.color == PlayerColor.White else "n"

    def valid_moves(self, game_config):
        list_of_moves = []
        for offset in Knight.valid_move_offsets:
            destination_position = self.position + offset
            if BoardUtils.is_vaild_tile_coordinate(destination_position):
                if Knight.in_first_column_exception(offset, self.position) or \
                        Knight.in_second_column_exception(offset, self.position) or \
                        Knight.in_seventh_column_exception(offset, self.position) or \
                        Knight.in_eighth_column_exception(offset, self.position):
                    continue
                tile = game_config.get_tile(destination_position)
                if not tile.is_occupied():
                    list_of_moves.append(
                        MajorMove(game_config, self, destination_position))
                else:
                    piece_at_destination = tile.get_piece()
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
         return BoardUtils.FIRST_COLUMN[destination_position] and ((offset == -17) or
                                                            (offset == -10) or
                                                            (offset == 6) or
                                                            (offset == 15))

    @staticmethod
    def in_second_column_exception(offset, destination_position):
        return BoardUtils.SECOND_COLUMN[destination_position] and ((offset == -10) or
                                                           (offset == 6))

    @staticmethod
    def in_seventh_column_exception(offset, destination_position):
        return BoardUtils.SEVENTH_COLUMN[destination_position] and ((offset == -6) or
                                                            (offset == 10))

    @staticmethod
    def in_eighth_column_exception(offset, destination_position):
        return BoardUtils.EIGHTH_COLUMN[destination_position] and ((offset == -15) or
                                                           (offset == -6) or
                                                           (offset == 10) or
                                                           (offset == 17))


class Rook(Piece):
    __doc__ = """Implements a Rook class by inheriting Piece class."""
    valid_move_offsets = [-8, -1, 1, 8]

    def __init__(self, position, color):
        Piece.__init__(self, position, color)
        self.value = 11


    """
    def __add__(self, other):
        return self.value + other

    def __radd__(self, other):
        return self.value + other
    """

    def __str__(self):
        return "R" if self.color == PlayerColor.White else "r"

    def valid_moves(self, game_config):
        list_of_moves = []
        for offset in Rook.valid_move_offsets:
            destination_position = self.position
            while BoardUtils.is_vaild_tile_coordinate(destination_position):
                if Rook.in_first_column_exception(offset, destination_position) or \
                        Rook.in_eighth_column_exception(offset, destination_position):
                    break
                destination_position += offset
                if BoardUtils.is_vaild_tile_coordinate(destination_position):
                    tile = game_config.get_tile(destination_position)
                    if not tile.is_occupied():
                        list_of_moves.append(
                            MajorMove(game_config, self, destination_position))
                    else:
                        piece_at_destination = tile.get_piece()
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
        return BoardUtils.FIRST_COLUMN[destination_position] and (offset == -1)

    @staticmethod
    def in_eighth_column_exception(offset, destination_position):
        return BoardUtils.EIGHTH_COLUMN[destination_position] and (offset == 1)





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
            destination_position = self.position + (offset * self.get_direction())
            if not BoardUtils.is_vaild_tile_coordinate(destination_position):
                continue
            if offset == 8 and not game_config.get_tile(destination_position).is_occupied():
                #TODO: Possibility of promotion. Needs better code(deal with Promotion)
                list_of_moves.append(PawnMove(game_config, self, destination_position))
            elif offset == 16 and self.is_first_move:
                if (self.color == PlayerColor.Black and
                        BoardUtils.SECOND_ROW[self.position]) \
                    or (self.color == PlayerColor.White and
                        BoardUtils.SEVENTH_ROW[self.position]):
                    first_tile = self.position + (self.get_direction() * 8)
                    if not (game_config.get_tile(first_tile).is_occupied() or
                            game_config.get_tile(destination_position).is_occupied()):
                        list_of_moves.append(
                            PawnMove(game_config, self, destination_position))
            elif offset == 7 and not \
                    ((BoardUtils.EIGHTH_COLUMN[self.position] and self.color == PlayerColor.White) or
                    (BoardUtils.FIRST_COLUMN[self.position] and self.color == PlayerColor.Black)):
                tile = game_config.get_tile(destination_position)
                if tile.is_occupied():
                    piece_at_destination = tile.get_piece()
                    piece_color = piece_at_destination.color
                    if piece_color != self.color:
                        list_of_moves.append(
                            AttackMove(game_config, self, destination_position,
                                       piece_at_destination))

            elif offset == 9 and not \
                    ((BoardUtils.EIGHTH_COLUMN[self.position] and self.color == PlayerColor.Black) or
                    (BoardUtils.FIRST_COLUMN[self.position] and self.color == PlayerColor.White)):
                tile = game_config.get_tile(destination_position)
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
        return False

    def attacked_piece(self):
        return None


class MajorMove(Move):
    def __init__(self, board, piece, dest):
        Move.__init__(self, board, piece, dest)


class AttackMove(Move):
    def __init__(self, board, piece, dest, attacked_piece):
        Move.__init__(self, board, piece, dest)
        self.attacked_piece = attacked_piece

    def is_attack(self):
        return True

    def attacked_piece(self):
        return self.attacked_piece

    def __eq__(self, other):
        return super.__eq__(other) and self.attacked_piece == other.attacked_piece


class PawnMove(Move):
    def __init__(self, board, piece, dest):
        Move.__init__(self, board, piece, dest)


class PawnAttackMove(AttackMove):
    def __init__(self, board, piece, dest, attacked_piece):
        AttackMove.__init__(self, board, piece, dest, attacked_piece)


class NullMove(Move):
    def __init__(self):
        Move.__init__(self, None, None, -1)

    def execute_move(self):
        raise Exception("Cannot execute Null Move")


class MoveTransition:
    def __init__(self, board, move, move_status):
        self.transition_board = board
        self.move = move
        self.move_status = move_status


class MoveFactory:
    def __init__(self):
        raise Exception("cannot Instantiate")

    def create_move(self, board, current_coordinates, destination_coordinates):
        for move in board.get_all_legal_moves():
            if move.current_coordinate() == current_coordinates \
                    and move.destination == destination_coordinates:
                return move


class MoveStatus(Enum):
    DONE = "Done"
    ILLEGAL_MOVE = "Illegal Move"
    LEAVES_KING_IN_CHECK = "Leaves King in check"


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


def generate_move_sentence(param):
    return "{0} moves {1} from {2} {3} to {4}\n".format(param[0],
                                                        param[1],
                                                        str(param[2]),
                                                        param[3],
                                                        param[4])


def int_to_alg(num):
    file = ["a", "b", "c", "d", "e", "f", "g", "h"]
    row = 8 - int(num / 8)
    column = file[num % 8]
    return str(column) + str(row)

def alg_to_int(notation):
    file = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    return file[notation[0]] + (8 - int(notation[1])) * 8

def find_move(moves, piece, source, destination):
    for move in moves:
        if str(move.piece).upper() == piece \
                and move.piece.position == alg_to_int(source) \
                and move.destination == alg_to_int(destination):
            return move


# for i in range(64):
#     print "{0} := {1} := {2}".format(i, int_to_alg(i), alg_to_int(int_to_alg(i)))

if __name__ == '__main__':
    end = False
    board = Board.create_standard_board()
    my_team_color = None
    # msg_count = 0
    while not end:
        input_message = raw_input()
        # if msg_count > 8:
        #     sys.stdout.write(my_team_color + " surrenders\n")
        #     end = True
        #     sys.exit(0)

        if "you are " in input_message:
            # set color and skip outputting a message if necessary
            if "black" in input_message:
                my_team_color = PlayerColor.Black
                my_team = board.black_player
                continue
            else:
                # print "reached here"
                my_team_color = PlayerColor.White
                my_team = board.white_player
                # game_rep = game.get_game_state()
                valid_moves = my_team.legal_moves
                move = valid_moves[random.randrange(len(valid_moves))]
                # print move
                board = my_team.make_move(move).transition_board
                sys.stdout.write(generate_move_sentence([my_team_color.value, str(move.piece), 1, int_to_alg(move.piece.position), int_to_alg(move.destination)]))

        elif "moves" in input_message:
        # else:
            message = input_message.split()
            if board.current_player.get_color().value == message[0]:
                move = find_move(board.current_player.legal_moves, message[2], message[5], message[7])
                # move = board.current_player.legal_moves[random.randrange(len(board.current_player.legal_moves))]
                # sys.stdout.write(generate_move_sentence(
                #     [board.current_player.get_color().value, str(move.piece), 1, int_to_alg(move.piece.position),
                #      int_to_alg(move.destination)]))
                move_transition = board.current_player.make_move(move)
                opponents_board = move_transition.transition_board
                if opponents_board.current_player.get_color() == my_team.get_color():
                    my_team = opponents_board.current_player
                    available_moves = opponents_board.current_player.legal_moves
                    # print available_moves
                    move = available_moves[random.randrange(len(available_moves))]
                    move_transition = my_team.make_move(move)
                    board = move_transition.transition_board
                    sys.stdout.write(generate_move_sentence(
                        [my_team_color.value, str(move.piece), 1,
                         int_to_alg(move.piece.position), int_to_alg(move.destination)]))
                else:
                    sys.stdout.write(my_team_color.value + " surrenders\n")

        print board

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