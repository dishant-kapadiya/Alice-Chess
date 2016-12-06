from copy import deepcopy


class Position:
    __doc__ = "A composite class for a position on board. Consists of a board and index."

    def __init__(self, board, index):
        """
        Initializer of this class
        :param board: an instance of BoardIndex class and keeps track of which board the
                      position is on.
        :param index: a non-negetive integer ranging from 0 to BoardProperties.NUM_TILES.
                      This represents an index of tile on board.
        """
        self.board = board
        self.index = index

    def __eq__(self, other):
        """
        overloaded operator of "==".
        :param other: an entity with which we compare instance of this class
        :return: boolean value. True if instance have same values else False
        """
        if not isinstance(other, Position):
            return False
        return self.board == other.board and self.index == other.index

    def __add__(self, other):
        """
        overloaded operator for forward addition
        :param other: an entity with which we add instance of this class
        :return: updated instance of this class
        """
        if isinstance(other, int):
            answer = Position(self.board, self.index + other)
            return answer
        else:
            return self

    def __radd__(self, other):
        """
        overloaded operator for reverse addition
        :param other: an entity with which we add instance of this class
        :return: updated instance of this class
        """
        if isinstance(other, int):
            Answer = Position(self.board, self.index + other)
            return Answer
        else:
            raise Exception("Value Error: " + str(other) + " cannot be added.")

    def __repr__(self):
        """
        generates meaningful representation used for printing and debugging
        :return: string representation of this position
        """
        return self.board + "(" + Position.int_to_alg(self.index) + ")"

    def flip_board(self):
        """
        flips board index for a given position
        :return: position with flipped instance
        """
        return Position(BoardIndex.next_board(self.board), self.index)

    @staticmethod
    def int_to_alg(num):
        """
        converts integer index to an algebraic representation of a chess tile
        For Example: 0 := a8, 62 := g0 etc.
        :param num: valid index i.e. 0 <= num <= BoardProperties.NUM_TILES
        :return: string consisting the algebraic representation
        """
        chess_file = ["a", "b", "c", "d", "e", "f", "g", "h"]
        row = 8 - int(num / 8)
        column = chess_file[num % 8]
        return str(column) + str(row)

    @staticmethod
    def alg_to_int(notation):
        """
        converts algebraic representation to index of the board tile
        :param notation: string of algebraic notation
        :return: integer index of the notation
        """
        chess_file = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        return chess_file[notation[0]] + (8 - int(notation[1])) * 8


class BoardIndex:
    __doc__ = "A wrapper class for board indexes and functions to manipulate them"
    Board_One = "1"
    Board_Two = "2"

    def __init__(self):
        pass

    @staticmethod
    def next_board(value):
        """
        Returns the next board in order.
        :param value: current board index
        :return: index of the next board in form of BoardIndex instance
        """
        return BoardIndex.Board_One if value == "2" else BoardIndex.Board_Two


class PlayerColor:
    __doc__ = "A wrapper class for Player colors and functions to manipulate them"
    White = "white"
    Black = "black"

    def __init__(self):
        pass

    @staticmethod
    def opponent(color, white_player, black_player):
        """
        returns opponent of the current player
        :param color: color of the current player
        :param white_player: Instance of WhitePlayer class
        :param black_player: Instance of BlackPlayer class
        :return: returns the opponent of player with current color
        """
        return black_player if color == PlayerColor.White else white_player

    @staticmethod
    def is_pawn_promotion_square(position, color):
        """
        checks if given position is suitable promotion square for given player color
        :param position: instance of Position class
        :param color: player color of the player
        :return: True if it is promotion square else False
        """
        if color == PlayerColor.Black:
            return BoardProperties.EIGHTH_ROW[position.index]
        else:
            return BoardProperties.FIRST_ROW[position.index]


class BoardProperties:
    __doc__ = "A wrapper class for Board Properties and functions to manipulate them"
    NUM_TILES = 64
    NUM_TILES_PER_ROW = 8
    NUM_BOARD = 2

    @staticmethod
    def init_column(column):
        """
        Creates a list of size BoardProperties.NUM_TILES with boolean values. True if
        the index is in given column
        :param column: non negative integer
        :return: list of boolean values
        """
        grid = [False] * BoardProperties.NUM_TILES
        for i in range(0 + column, BoardProperties.NUM_TILES,
                       BoardProperties.NUM_TILES_PER_ROW):
            grid[i] = True
        return grid

    @staticmethod
    def init_row(row):
        """
        Creates a list of size BoardProperties.NUM_TILES with boolean values. True if
        the index is in given row
        :param row: non negative integer
        :return: list of boolean values
        """
        grid = [False] * BoardProperties.NUM_TILES
        for i in range(BoardProperties.NUM_TILES_PER_ROW * row,
                       BoardProperties.NUM_TILES_PER_ROW * (row + 1)):
            grid[i] = True
        return grid

    def __init__(self):
        """
        Initializer of this class. Creates several properties which come handy in later
        classes.
        """
        self.FIRST_COLUMN = self.init_column(0)
        self.SECOND_COLUMN = self.init_column(1)
        self.SEVENTH_COLUMN = self.init_column(6)
        self.EIGHTH_COLUMN = self.init_column(7)
        self.FIRST_ROW = self.init_row(0)
        self.SECOND_ROW = self.init_row(1)
        self.SEVENTH_ROW = self.init_row(6)
        self.EIGHTH_ROW = self.init_row(7)

    @staticmethod
    def is_valid_tile_coordinate(new_coordinate):
        """
        checks if a given Position is a valid coordinate according BoardProperties
        :param new_coordinate: Position class instance
        :return: True if valid else False
        """
        return 0 <= new_coordinate.index < BoardProperties.NUM_TILES and \
               1 <= int(new_coordinate.board) <= BoardProperties.NUM_BOARD
BoardProperties = BoardProperties()


class Tile:
    __doc__ = "Abstract class for a tile on board configuration"

    def __init__(self, coordinate):
        """Initalize the coordinate of tile.
        :param coordinate: a non negative integer
        """
        self.coordinate = coordinate

    def is_occupied(self):
        pass

    def get_piece(self):
        pass

    @staticmethod
    def all_possible_tiles():
        """
        generates all possible tiles on a board
        :return: list of EmptyTiles
        """
        temp = []
        for i in range(BoardProperties.NUM_TILES):
            temp.append(EmptyTile(i))
        return dict(enumerate(temp))


class EmptyTile(Tile):
    __doc__ = "Class representing an Empty Tile. Inherits from Tile"

    def __init__(self, coordinate):
        """
        Initalize the coordinate of tile. Calls superclass's initializer
        :param coordinate: a non negative integer
        """
        Tile.__init__(self, coordinate)

    def is_occupied(self):
        """
        returns False as an EmptyTile cannot be occupied
        :return: False
        """
        return False

    def __str__(self):
        """
        generates string representation of this tile. Used in printing and debugging
        :return: String of a suitable representation
        """
        return "-"

    def get_piece(self):
        return None


class OccupiedTile(Tile):
    def __init__(self, coordinate, piece):
        """
        Initalize the coordinate of tile. Calls superclass's initializer and sets own
        properties
        :param coordinate: a non negative integer
        :param piece: Instance of Piece which occupies this Tile
        """
        Tile.__init__(self, coordinate)
        self.piece = piece

    def is_occupied(self):
        """
        returns True as an OccupiedTile should be occupied
        :return: True
        """
        return True

    def __str__(self):
        """
        generates string representation of this tile. Used in printing and debugging
        :return: String of a suitable representation
        """
        return str(self.piece)

    def get_piece(self):
        """
        returns the piece occupying this tile
        :return: Piece
        """
        return self.piece


class Board:
    __doc__ = "Represents a full game on the table. Consists of all the information " \
              "necessary to represent a game of Alice Chess."

    def __init__(self, builder):
        """
        Initializes the class properties like game boards, pieces in arsenal of each
        player, players, current players etc.
        NOTE: Shouldn't be initialised by anyone else then builder class for this
        class. This class follows Builder Pattern for construction and can be build
        using the BoardBuilder class.
        :param builder: Instance of the BoardBuilder class
        """
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
    def create_game_board(board_config):
        """
        creates a list of all the tiles on given game board
        :param board_config: dictionary of configuration on this board
        :return: list of suitable tiles on this board
        """
        board_tiles = [None] * BoardProperties.NUM_TILES
        for i in range(BoardProperties.NUM_TILES):
            if isinstance(board_config[i], Piece):
                board_tiles[i] = OccupiedTile(i, board_config[i])
            else:
                board_tiles[i] = EmptyTile(i)
        return board_tiles

    def get_tile(self, coordinate):
        """
        gets the tile at a given non negative integer index
        :param coordinate: non negative integer
        :return: instance of Tile class
        """
        if coordinate.board == BoardIndex.Board_One:
            game_board = self.game_board1
        else:
            game_board = self.game_board2
        return game_board[coordinate.index]

    @staticmethod
    def create_standard_board():
        """
        Creates a standard board configuration in Alice Chess
        :return: instance of Board class with the properties set to standard starting
                 point in the game
        """
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
        """
        generates a list of all the active pieces of a given player
        :param gameboard: list of all the tiles on a game board
        :param color: color of the player
        :return: list of all the active(non-dead) pieces
        """
        pieces = []
        for tile in gameboard:
            if tile.is_occupied():
                piece = tile.get_piece()
                if piece.color == color:
                    pieces.append(piece)

        return pieces

    def calculate_moves(self, arsenal):
        """
        generates a list of all the moves possible for a player current this condition
        :param arsenal: list of pieces a player has
        :return: list of Moves that player can make
        """
        list_of_moves = []
        for piece in arsenal:
            list_of_moves += piece.valid_moves(self)
        return list_of_moves

    def __repr__(self):
        """
        generates string representation of this game. suitable for printing and debugging
        :return: string representation of this game
        """
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
        """
        generates all the legal moves possible by both the players in this configuration
        :return: list of Moves
        """
        return self.white_legal_moves + self.black_legal_moves


class BoardBuilder:
    __doc__ = "Builder class for the Board. Used to construct the Board representation."
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
            destination_position = Position(BoardIndex.next_board(self.position.board),
                                            self.position.index + offset)
            if BoardProperties.is_valid_tile_coordinate(destination_position):
                if King.in_first_column_exception(offset, self.position.index) or \
                        King.in_eighth_column_exception(offset, self.position.index):
                    continue
                tile_in_next_board = game_config.get_tile(destination_position)
                position_in_same_board = Position.flip_board(destination_position)
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
                                AttackMove(game_config, self, destination_position, piece_at_destination))
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
            destination_position = Position.flip_board(self.position)
            while BoardProperties.is_valid_tile_coordinate(destination_position):
                if Queen.in_first_column_exception(offset, destination_position.index) or \
                        Queen.in_eighth_column_exception(offset, destination_position.index):
                    break
                destination_position += offset
                if BoardProperties.is_valid_tile_coordinate(destination_position):
                    # tile = game_config.get_tile(destination_position)
                    tile_in_next_board = game_config.get_tile(destination_position)
                    position_in_same_board = Position.flip_board(destination_position)
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
            destination_position = Position.flip_board(self.position)
            while BoardProperties.is_valid_tile_coordinate(destination_position):
                if Bishop.in_first_column_exception(offset, destination_position.index) or \
                        Bishop.in_eighth_column_exception(offset, destination_position.index):
                    break
                destination_position += offset
                if BoardProperties.is_valid_tile_coordinate(destination_position):
                    # tile = game_config.get_tile(destination_position)
                    tile_in_next_board = game_config.get_tile(destination_position)
                    position_in_same_board = Position.flip_board(
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
            destination_position = Position(BoardIndex.next_board(self.position.board),
                                            self.position.index + offset)
            if BoardProperties.is_valid_tile_coordinate(destination_position):
                if Knight.in_first_column_exception(offset, self.position.index) or \
                        Knight.in_second_column_exception(offset, self.position.index) or \
                        Knight.in_seventh_column_exception(offset, self.position.index) or \
                        Knight.in_eighth_column_exception(offset, self.position.index):
                    continue
                tile_in_next_board = game_config.get_tile(destination_position)
                position_in_same_board = Position.flip_board(destination_position)
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
            destination_position = Position.flip_board(self.position)
            while BoardProperties.is_valid_tile_coordinate(destination_position):
                if Rook.in_first_column_exception(offset, destination_position.index) or \
                        Rook.in_eighth_column_exception(offset, destination_position.index):
                    break
                destination_position += offset
                if BoardProperties.is_valid_tile_coordinate(destination_position):
                    # tile = game_config.get_tile(destination_position)
                    tile_in_next_board = game_config.get_tile(destination_position)
                    position_in_same_board = Position.flip_board(destination_position)
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
            destination_position = Position(BoardIndex.next_board(self.position.board),
                                            self.position.index + (offset * self.get_direction()))
            if not BoardProperties.is_valid_tile_coordinate(destination_position):
                continue
            if not game_config.get_tile(destination_position).is_occupied():
                tile_in_this_board = Position.flip_board(destination_position)
                if offset == 8 and not game_config.get_tile(tile_in_this_board).is_occupied():
                    if PlayerColor.is_pawn_promotion_square(destination_position, self.color):
                        list_of_moves.append(PawnPromotion(MajorMove(game_config, self, destination_position)))
                    else:
                        list_of_moves.append(MajorMove(game_config, self, destination_position))
                elif offset == 16 and self.is_first_move:
                    if (self.color == PlayerColor.Black and
                            BoardProperties.SECOND_ROW[self.position.index]) \
                            or (self.color == PlayerColor.White and
                                    BoardProperties.SEVENTH_ROW[self.position.index]):
                        first_tile_position = Position(BoardIndex.next_board(self.position.board),
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
                            if PlayerColor.is_pawn_promotion_square(destination_position, self.color):
                                list_of_moves.append(PawnPromotion(
                                    AttackMove(game_config, self, destination_position, piece_at_destination)))
                            else:
                                list_of_moves.append(
                                    AttackMove(game_config, self, destination_position, piece_at_destination))

                elif offset == 9 and not \
                        ((BoardProperties.EIGHTH_COLUMN[self.position.index] and self.color == PlayerColor.Black) or
                             (BoardProperties.FIRST_COLUMN[self.position.index] and self.color == PlayerColor.White)):
                    tile = game_config.get_tile(tile_in_this_board)
                    if tile.is_occupied():
                        piece_at_destination = tile.get_piece()
                        piece_color = piece_at_destination.color
                        if piece_color != self.color:
                            if PlayerColor.is_pawn_promotion_square(destination_position, self.color):
                                list_of_moves.append(PawnPromotion(
                                    AttackMove(game_config, self, destination_position, piece_at_destination)))
                            else:
                                list_of_moves.append(
                                    AttackMove(game_config, self, destination_position, piece_at_destination))
        return list_of_moves

    def promotion_piece(self):
        return Queen(self.position, self.color)


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


class PawnPromotion(Move):
    def __init__(self, move):
        Move.__init__(self, move.board, move.piece, move.destination)
        self.move = move
        self.promotedPawn = move.piece

    def is_attack(self):
        return self.move.is_attack()

    def attacked_piece(self):
        return self.move.attacked_piece()

    def __repr__(self):
        return "Q(" + str(self.move) + ")"

    def __eq__(self, other):
        if isinstance(other, PawnPromotion):
            return self.move == other.move
        return False

    def execute_move(self):
        board = self.move.execute_move()
        boardbuilder = BoardBuilder()
        for piece in board.current_player.get_active_pieces():
            if not self.promotedPawn == piece:
                boardbuilder.set_piece(piece)
        for piece in board.current_player.get_opponent().get_active_pieces():
            boardbuilder.set_piece(piece)

        boardbuilder.set_piece(self.promotedPawn.promotion_piece().move_piece(self))
        boardbuilder.next_move_maker = board.current_player.get_opponent().get_color()
        return boardbuilder.build()


class MoveStatus():
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
            if tile == Position.flip_board(move.destination):
                attacking_moves.append(move)
        return attacking_moves

    def has_escape_moves(self):
        for move in self.legal_moves:
            transit = self.make_move(move)
            if transit.move_status == MoveStatus.DONE:
                return True
        return False

    def is_in_check(self):
        return not len(self.calculate_attacks_on_tile(self.player_king.position,
                                                      self.opponents_moves)) == 0

    def get_escape_moves(self):
        escape_moves = []
        for move in self.legal_moves:
            transit = self.make_move(move)
            if transit.move_status == MoveStatus.DONE:
                escape_moves.append(move)
        return escape_moves

    def pawn_score(self):
        pieces = self.get_active_pieces()
        offsets = [7, 8, 9]
        double_pawns = {}
        double_pawn_count = 0
        isolated_pawn_count = 0
        # blocked_pawn_count = 0
        # calculating double pawns and isolated pawns
        for piece in pieces:
            if isinstance(piece, Pawn):
                index = str(piece.position.board) + Position.int_to_alg(piece.position.index)[0]
                double_pawns[index] = double_pawns.get(index, 0) + 1

                def position_generator(num):
                    return Position.flip_board(piece.position + piece.get_direction() * num)
                positions = [position_generator(i) for i in offsets]
                piece_at_positions = [self.board.get_tile(position).get_piece() for position in positions]
                if not (isinstance(piece_at_positions[0], Pawn) and piece_at_positions[0].color == piece.color or
                        isinstance(piece_at_positions[2], Pawn) and piece_at_positions[2].color == piece.color):
                    isolated_pawn_count += 1
                # if self.board.get_tile(Position.flip_board(positions[1])).get_piece().color != piece.color or \
                #                 piece.color != piece_at_positions[1].color:
                #     blocked_pawn_count += 1
        for val in double_pawns.values():
            if val > 1:
                double_pawn_count += 1
        # blocked pawn
        return 0.5 * float(double_pawn_count) + isolated_pawn_count

    def is_in_check_mate(self):
        return self.is_in_check() and not self.has_escape_moves()

    def is_in_stale_mate(self):
        return (not self.is_in_check()) and (not self.has_escape_moves())

    def make_move(self, move):
        if not self.is_legal_move(move):
            return MoveTransition(self.board, move, MoveStatus.ILLEGAL_MOVE)
        transition_board = move.execute_move()
        king_attacks = Player.calculate_attacks_on_tile(
            transition_board.current_player.get_opponent().player_king.position,
            transition_board.current_player.legal_moves)
        if len(king_attacks) != 0:
            return MoveTransition(self.board, move, MoveStatus.LEAVES_KING_IN_CHECK)
        return MoveTransition(transition_board, move, MoveStatus.DONE)

    def make_move_without_changing_board(self, move):
        if not self.is_legal_move(move):
            return MoveTransition(self.board, move, MoveStatus.ILLEGAL_MOVE)
        new_move = deepcopy(move)
        new_move.destination = new_move.destination.flip_board()
        transition_board = new_move.execute_move()
        king_attacks = Player.calculate_attacks_on_tile(
            transition_board.current_player.get_opponent().player_king.position,
            transition_board.current_player.legal_moves)
        if len(king_attacks) != 0:
            return MoveTransition(self.board, new_move, MoveStatus.LEAVES_KING_IN_CHECK)
        return MoveTransition(transition_board, new_move, MoveStatus.DONE)


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
