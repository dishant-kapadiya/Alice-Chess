"""Implements an Alice Chess Engine"""
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
            answer = Position(self.board, self.index + other)
            return answer
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
    def valid_tile(new_coordinate):
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
        """
        returns None as EmptyTile is not Occupied
        :return:
        """
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
        self.builder = builder
        self.game_board1 = Board.create_game_board(builder.board_config1)
        self.game_board2 = Board.create_game_board(builder.board_config2)
        self.white_piece = Board.calculate_active_piece(self.game_board1,
                                                        PlayerColor.White) + \
                           Board.calculate_active_piece(self.game_board2,
                                                        PlayerColor.White)
        self.black_piece = Board.calculate_active_piece(self.game_board1,
                                                        PlayerColor.Black) + \
                           Board.calculate_active_piece(self.game_board2,
                                                        PlayerColor.Black)
        white_legal_moves = self.calculate_moves(self.white_piece)
        black_legal_moves = self.calculate_moves(self.black_piece)
        self.white_player = WhitePlayer(self, white_legal_moves,
                                        black_legal_moves)
        self.black_player = BlackPlayer(self, black_legal_moves,
                                        white_legal_moves)
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
        return "\n" + final_str + last_line

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
        """
        Initializes all the values to None and gets the basic structure ready
        """
        for i in range(BoardProperties.NUM_TILES):
            self.board_config1[i] = None
            self.board_config2[i] = None
        self.next_move_maker = None

    def set_piece(self, piece):
        """
        adds the piece at its position on board.
        :param piece: Piece which needs to be added on board
        """
        if piece.position.board == BoardIndex.Board_One:
            self.board_config1[piece.position.index] = piece
        else:
            self.board_config2[piece.position.index] = piece

    def set_next_move_maker(self, next_move_maker):
        """
        sets the next move make in this board configuration
        :param next_move_maker: instance of PlayerColor class
        """
        self.next_move_maker = next_move_maker

    def build(self):
        """
        Constucts the object of Board class which represents a suitable representation
        representated by dictionaries in this class
        :return: Instance of the Board class
        """
        return Board(self)


class Piece:
    __doc__ = "Abstract class for different pieces in the game. Implements methods for " \
              "generating valid moves in current gamestate."

    def __init__(self, position, color):
        """
        Initialize the properties of a piece.
        :param position: Position at which the piece is currently standing
        :param color: PlayerColor instance which represents the color of piece
        """
        self.position = position
        self.color = color
        self.is_first_move = False

    def valid_moves(self, game_config):
        pass

    def move_piece(self, move):
        pass

    def __mul__(self, other):
        """
        overloads the multiplication operator
        :param other:
        :return:
        """
        if isinstance(other, (int, float, long)):
            return self.value * other
        return other

    def __rmul__(self, other):
        """
        overloads the multiplication operator
        :param other:
        :return:
        """
        if isinstance(other, (int, float, long)):
            return self.value * other
        return other

    def __eq__(self, other):
        """
        overloaded operator of "==". used to compare value of other with the instance
        of this class
        :param other: an entity with which we compare this classes entity
        :return: True if the values match else False
        """
        if not (self.__class__ == other.__class__ and isinstance(other, Piece)):
            return False

        return self.position == other.position and self.color == other.color and \
               self.is_first_move == other.is_first_move


class King(Piece):
    __doc__ = "Implements a King class by inheriting Piece class."
    valid_move_offsets = [-9, -8, -7, -1, 1, 7, 8, 9]
    piece_square_table = [-30,-40,-40,-50,-50,-40,-40,-30,
                          -30,-40,-40,-50,-50,-40,-40,-30,
                          -30,-40,-40,-50,-50,-40,-40,-30,
                          -30,-40,-40,-50,-50,-40,-40,-30,
                          -20,-30,-30,-40,-40,-30,-30,-20,
                          -10,-20,-20,-20,-20,-20,-20,-10,
                           20, 20,  0,  0,  0,  0, 20, 20,
                           20, 30, 10,  0,  0, 10, 30, 20]

    def __init__(self, position, color):
        """
        calls __init__ of super class and sets value for this piece
        :param position: Position for this piece
        :param color: color for this piece
        """
        Piece.__init__(self, position, color)
        self.position_value = King.get_position_value(self.position.index, self.color)
        self.value = 200 + self.position_value

    @staticmethod
    def get_position_value(index, color):
        """
        returns the value of position Piece is standing at
        :param index: index of tile on Board
        :param color: PlayerColor
        :return:
        """
        if color == PlayerColor.Black:
            lookup_index = BoardProperties.NUM_TILES - index - 1
        else:
            lookup_index = index
        return King.piece_square_table[lookup_index]

    def __add__(self, other):
        """
            overloaded operator for forward addition
            :param other: an entity with which we add instance of this class
            :return: updated instance of this class
        """
        return self.value + other

    def __radd__(self, other):
        """
        overloaded operator for reverse addition
        :param other: an entity with which we add instance of this class
        :return: updated instance of this class
        """
        return self.value + other

    def __str__(self):
        """
        generates meaningful representation used for printing and debugging
        :return: string representation of this piece
        """
        return "K" if self.color == PlayerColor.White else "k"

    def move_piece(self, move):
        """
        creates a new instance of this Piece with updated Position
        :param move: Move due to which this piece is changed
        :return: Updated instance of the Piece
        """
        return King(move.destination, move.piece.color)

    def valid_moves(self, game_state):
        """
        Generates a list of all the valid moves this Piece can make on the game board.
        It uses the valid_move_offsets to generate all the moves
        :param game_state: the current state of the game
        :return: a list of Moves
        """
        moves = []
        for offset in King.valid_move_offsets:
            destination = Position(BoardIndex.next_board(self.position.board),
                                            self.position.index + offset)
            if BoardProperties.valid_tile(destination):
                if King.first_column_exception(offset, self.position.index) or \
                        King.eighth_column_exception(offset, self.position.index):
                    continue
                tile_in_next_board = game_state.get_tile(destination)
                position_in_same_board = Position.flip_board(destination)
                tile_in_this_board = game_state.get_tile(position_in_same_board)
                if not tile_in_next_board.is_occupied():
                    if not tile_in_this_board.is_occupied():
                        moves.append(SimpleMove(game_state, self, destination))
                    else:
                        piece_at_destination = tile_in_this_board.get_piece()
                        piece_color = piece_at_destination.color
                        if piece_color != self.color:
                            moves.append(AttackMove(game_state, self, destination,
                                                    piece_at_destination))
        return moves

    @staticmethod
    def first_column_exception(offset, position):
        """
        Detects the exception for First column
        :param offset: offset in picture
        :param position: current Position of the piece
        :return: True if it's in first column of the board
        """
        return BoardProperties.FIRST_COLUMN[position] and ((offset == -9) or
                                                           (offset == -1) or
                                                           (offset == 7))

    @staticmethod
    def eighth_column_exception(offset, position):
        """
        Detects the exception for Eighth column
        :param offset: offset in picture
        :param position: current Position of the piece
        :return: True if it's in eighth column of the board
        """
        return BoardProperties.EIGHTH_COLUMN[position] and ((offset == -7) or
                                                            (offset == 1) or
                                                            (offset == 9))


class Queen(Piece):
    __doc__ = """Implements a Queen class by inheriting Piece class."""
    valid_move_offsets = [-9, -8, -7, -1, 1, 7, 8, 9]
    piece_square_table = [-20,-10,-10, -5, -5,-10,-10,-20,
                          -10,  0,  0,  0,  0,  0,  0,-10,
                          -10,  0,  5,  5,  5,  5,  0,-10,
                           -5,  0,  5,  5,  5,  5,  0, -5,
                            0,  0,  5,  5,  5,  5,  0, -5,
                          -10,  5,  5,  5,  5,  5,  0,-10,
                          -10,  0,  5,  0,  0,  0,  0,-10,
                          -20,-10,-10, -5, -5,-10,-10,-20]

    def __init__(self, position, color):
        """
        calls __init__ of super class and sets value for this piece
        :param position: Position for this piece
        :param color: color for this piece
        """
        Piece.__init__(self, position, color)
        self.position_value = Queen.get_position_value(self.position.index, self.color)
        self.value = 90 + self.position_value

    @staticmethod
    def get_position_value(index, color):
        """
        returns the value of position Piece is standing at
        :param index: index of tile on Board
        :param color: PlayerColor
        :return:
        """
        if color == PlayerColor.Black:
            lookup_index = BoardProperties.NUM_TILES - index - 1
        else:
            lookup_index = index
        return Queen.piece_square_table[lookup_index]

    def __add__(self, other):
        """
        overloaded operator for forward addition
        :param other: an entity with which we add instance of this class
        :return: updated instance of this class
        """
        return self.value + other

    def __radd__(self, other):
        """
        overloaded operator for reverse addition
        :param other: an entity with which we add instance of this class
        :return: updated instance of this class
        """
        return self.value + other

    def __str__(self):
        """
        generates meaningful representation used for printing and debugging
        :return: string representation of this piece
        """
        return "Q" if self.color == PlayerColor.White else "q"

    def move_piece(self, move):
        """
        creates a new instance of this Piece with updated Position
        :param move: Move due to which this piece is changed
        :return: Updated instance of the Piece
        """
        return Queen(move.destination, move.piece.color)

    def valid_moves(self, game_state):
        """
        Generates a list of all the valid moves this Piece can make on the game board.
        It uses the valid_move_offsets to generate all the moves
        :param game_state: the current state of the game
        :return: a list of Moves
        """
        moves = []
        for offset in Queen.valid_move_offsets:
            destination = Position.flip_board(self.position)
            while BoardProperties.valid_tile(destination):
                if Queen.first_column_exception(offset, destination.index) or \
                        Queen.eighth_column_exception(offset, destination.index):
                    break
                destination += offset
                if BoardProperties.valid_tile(destination):
                    tile_in_next_board = game_state.get_tile(destination)
                    position_in_same_board = Position.flip_board(destination)
                    tile_in_this_board = game_state.get_tile(position_in_same_board)
                    if not tile_in_next_board.is_occupied():
                        if not tile_in_this_board.is_occupied():
                            moves.append(SimpleMove(game_state, self, destination))
                        else:
                            piece_at_destination = tile_in_this_board.get_piece()
                            piece_color = piece_at_destination.color
                            if piece_color != self.color:
                                moves.append(AttackMove(game_state, self, destination,
                                                        piece_at_destination))
                            break
        return moves

    @staticmethod
    def first_column_exception(offset, position):
        """
        Detects the exception for First column
        :param offset: offset in picture
        :param position: current Position of the piece
        :return: True if it's in first column of the board
        """
        return BoardProperties.FIRST_COLUMN[position] and ((offset == -9) or
                                                           (offset == -1) or
                                                           (offset == 7))

    @staticmethod
    def eighth_column_exception(offset, position):
        """
        Detects the exception for Eighth column
        :param offset: offset in picture
        :param position: current Position of the piece
        :return: True if it's in eighth column of the board
        """
        return BoardProperties.EIGHTH_COLUMN[position] and ((offset == -7) or
                                                            (offset == 1) or
                                                            (offset == 9))


class Bishop(Piece):
    __doc__ = """Implements a Bishop class by inheriting Piece class."""
    valid_move_offsets = [-9, -7, 7, 9]
    piece_square_table = [-20,-10,-10,-10,-10,-10,-10,-20,
                          -10,  0,  0,  0,  0,  0,  0,-10,
                          -10,  0,  5, 10, 10,  5,  0,-10,
                          -10,  5,  5, 10, 10,  5,  5,-10,
                          -10,  0, 10, 10, 10, 10,  0,-10,
                          -10, 10, 10, 10, 10, 10, 10,-10,
                          -10,  5,  0,  0,  0,  0,  5,-10,
                          -20,-10,-10,-10,-10,-10,-10,-20,]

    def __init__(self, position, color):
        """
        calls __init__ of super class and sets value for this piece
        :param position: Position for this piece
        :param color: color for this piece
        """
        Piece.__init__(self, position, color)
        self.position_value = Bishop.get_position_value(self.position.index, self.color)
        self.value = 33 + self.position_value

    @staticmethod
    def get_position_value(index, color):
        """
        returns the value of position Piece is standing at
        :param index: index of tile on Board
        :param color: PlayerColor
        :return:
        """
        if color == PlayerColor.Black:
            lookup_index = BoardProperties.NUM_TILES - index - 1
        else:
            lookup_index = index
        return Bishop.piece_square_table[lookup_index]

    def __add__(self, other):
        """
        overloaded operator for forward addition
        :param other: an entity with which we add instance of this class
        :return: updated instance of this class
        """
        return self.value + other

    def __radd__(self, other):
        """
        overloaded operator for reverse addition
        :param other: an entity with which we add instance of this class
        :return: updated instance of this class
        """
        return self.value + other

    def __str__(self):
        """
        generates meaningful representation used for printing and debugging
        :return: string representation of this piece
        """
        return "B" if self.color == PlayerColor.White else "b"

    def move_piece(self, move):
        """
        creates a new instance of this Piece with updated Position
        :param move: Move due to which this piece is changed
        :return: Updated instance of the Piece
        """
        return Bishop(move.destination, move.piece.color)

    def valid_moves(self, game_state):
        """
        Generates a list of all the valid moves this Piece can make on the game board.
        It uses the valid_move_offsets to generate all the moves
        :param game_state: the current state of the game
        :return: a list of Moves
        """
        moves = []
        for offset in Bishop.valid_move_offsets:
            destination = Position.flip_board(self.position)
            while BoardProperties.valid_tile(destination):
                if Bishop.first_column_exception(offset, destination.index) or \
                        Bishop.eighth_column_exception(offset, destination.index):
                    break
                destination += offset
                if BoardProperties.valid_tile(destination):
                    tile_in_next_board = game_state.get_tile(destination)
                    position_in_same_board = Position.flip_board(destination)
                    tile_in_this_board = game_state.get_tile(position_in_same_board)
                    if not tile_in_next_board.is_occupied():
                        if not tile_in_this_board.is_occupied():
                            moves.append(SimpleMove(game_state, self, destination))
                        else:
                            piece_at_destination = tile_in_this_board.get_piece()
                            piece_color = piece_at_destination.color
                            if piece_color != self.color:
                                moves.append(AttackMove(game_state, self, destination,
                                                        piece_at_destination))
                            break
        return moves

    @staticmethod
    def first_column_exception(offset, position):
        """
        Detects the exception for First column
        :param offset: offset in picture
        :param position: current Position of the piece
        :return: True if it's in first column of the board
        """
        return BoardProperties.FIRST_COLUMN[position] and ((offset == -9) or
                                                           (offset == 7))

    @staticmethod
    def eighth_column_exception(offset, position):
        """
        Detects the exception for Eighth column
        :param offset: offset in picture
        :param position: current Position of the piece
        :return: True if it's in eighth column of the board
        """
        return BoardProperties.EIGHTH_COLUMN[position] and ((offset == -7) or
                                                            (offset == 9))


class Knight(Piece):
    __doc__ = """Implements a Knight class by inheriting Piece class."""
    valid_move_offsets = [-17, -15, -10, -6, 6, 10, 15, 17]
    piece_square_table = [-50,-40,-30,-30,-30,-30,-40,-50,
                          -40,-20,  0,  0,  0,  0,-20,-40,
                          -30,  0, 10, 15, 15, 10,  0,-30,
                          -30,  5, 15, 20, 20, 15,  5,-30,
                          -30,  0, 15, 20, 20, 15,  0,-30,
                          -30,  5, 10, 15, 15, 10,  5,-30,
                          -40,-20,  0,  5,  5,  0,-20,-40,
                          -50,-40,-30,-30,-30,-30,-40,-50,]

    def __init__(self, position, color):
        """
        calls __init__ of super class and sets value for this piece
        :param position: Position for this piece
        :param color: color for this piece
        """
        Piece.__init__(self, position, color)
        self.position_value = Knight.get_position_value(self.position.index, self.color)
        self.value = 32 + self.position_value

    @staticmethod
    def get_position_value(index, color):
        """
        returns the value of position Piece is standing at
        :param index: index of tile on Board
        :param color: PlayerColor
        :return:
        """
        if color == PlayerColor.Black:
            lookup_index = BoardProperties.NUM_TILES - index - 1
        else:
            lookup_index = index
        return Knight.piece_square_table[lookup_index]

    def __add__(self, other):
        """
        overloaded operator for forward addition
        :param other: an entity with which we add instance of this class
        :return: updated instance of this class
        """
        return self.value + other

    def __radd__(self, other):
        """
        overloaded operator for reverse addition
        :param other: an entity with which we add instance of this class
        :return: updated instance of this class
        """
        return self.value + other

    def __str__(self):
        """
        generates meaningful representation used for printing and debugging
        :return: string representation of this piece
        """
        return "N" if self.color == PlayerColor.White else "n"

    def move_piece(self, move):
        """
        creates a new instance of this Piece with updated Position
        :param move: Move due to which this piece is changed
        :return: Updated instance of the Piece
        """
        return Knight(move.destination, move.piece.color)

    def valid_moves(self, game_state):
        """
        Generates a list of all the valid moves this Piece can make on the game board.
        It uses the valid_move_offsets to generate all the moves
        :param game_state: the current state of the game
        :return: a list of Moves
        """
        moves = []
        for offset in Knight.valid_move_offsets:
            destination = Position(BoardIndex.next_board(self.position.board),
                                   self.position.index + offset)
            if BoardProperties.valid_tile(destination):
                if Knight.first_column_exception(offset, self.position.index) or \
                        Knight.second_column_exception(offset, self.position.index) or \
                        Knight.seventh_column_exception(offset, self.position.index) or \
                        Knight.eighth_column_exception(offset, self.position.index):
                    continue
                tile_in_next_board = game_state.get_tile(destination)
                position_in_same_board = Position.flip_board(destination)
                tile_in_this_board = game_state.get_tile(position_in_same_board)
                if not tile_in_next_board.is_occupied():
                    if not tile_in_this_board.is_occupied():
                        moves.append(SimpleMove(game_state, self, destination))
                    else:
                        piece_at_destination = tile_in_this_board.get_piece()
                        piece_color = piece_at_destination.color
                        if piece_color != self.color:
                            moves.append(AttackMove(game_state, self, destination,
                                                    piece_at_destination))
        return moves

    @staticmethod
    def first_column_exception(offset, position):
        """
        Detects the exception for First column
        :param offset: offset in picture
        :param position: current Position of the piece
        :return: True if it's in first column of the board
        """
        return BoardProperties.FIRST_COLUMN[position] and ((offset == -17) or
                                                           (offset == -10) or
                                                           (offset == 6) or
                                                           (offset == 15))

    @staticmethod
    def second_column_exception(offset, position):
        """
        Detects the exception for Second column
        :param offset: offset in picture
        :param position: current Position of the piece
        :return: True if it's in second column of the board
        """
        return BoardProperties.SECOND_COLUMN[position] and ((offset == -10) or
                                                            (offset == 6))

    @staticmethod
    def seventh_column_exception(offset, position):
        """
        Detects the exception for Seventh column
        :param offset: offset in picture
        :param position: current Position of the piece
        :return: True if it's in seventh column of the board
        """
        return BoardProperties.SEVENTH_COLUMN[position] and ((offset == -6) or
                                                             (offset == 10))

    @staticmethod
    def eighth_column_exception(offset, position):
        """
        Detects the exception for Eighth column
        :param offset: offset in picture
        :param position: current Position of the piece
        :return: True if it's in eighth column of the board
        """
        return BoardProperties.EIGHTH_COLUMN[position] and ((offset == -15) or
                                                            (offset == -6) or
                                                            (offset == 10) or
                                                            (offset == 17))


class Rook(Piece):
    __doc__ = """Implements a Rook class by inheriting Piece class."""
    valid_move_offsets = [-8, -1, 1, 8]
    piece_square_table = [0,  0,  0,  0,  0,  0,  0,  0,
                          5, 10, 10, 10, 10, 10, 10,  5,
                         -5,  0,  0,  0,  0,  0,  0, -5,
                         -5,  0,  0,  0,  0,  0,  0, -5,
                         -5,  0,  0,  0,  0,  0,  0, -5,
                         -5,  0,  0,  0,  0,  0,  0, -5,
                         -5,  0,  0,  0,  0,  0,  0, -5,
                          0,  0,  0,  5,  5,  0,  0,  0]

    def __init__(self, position, color):
        """
        calls __init__ of super class and sets value for this piece
        :param position: Position for this piece
        :param color: color for this piece
        """
        Piece.__init__(self, position, color)
        self.position_value = Rook.get_position_value(self.position.index, self.color)
        self.value = 50 + self.position_value

    @staticmethod
    def get_position_value(index, color):
        """
        returns the value of position Piece is standing at
        :param index: index of tile on Board
        :param color: PlayerColor
        :return:
        """
        if color == PlayerColor.Black:
            lookup_index = BoardProperties.NUM_TILES - index - 1
        else:
            lookup_index = index
        return Rook.piece_square_table[lookup_index]

    def __add__(self, other):
        """
        overloaded operator for forward addition
        :param other: an entity with which we add instance of this class
        :return: updated instance of this class
        """
        return self.value + other

    def __radd__(self, other):
        """
        overloaded operator for reverse addition
        :param other: an entity with which we add instance of this class
        :return: updated instance of this class
        """
        return self.value + other

    def __str__(self):
        """
        generates meaningful representation used for printing and debugging
        :return: string representation of this piece
        """
        return "R" if self.color == PlayerColor.White else "r"

    def move_piece(self, move):
        """
        creates a new instance of this Piece with updated Position
        :param move: Move due to which this piece is changed
        :return: Updated instance of the Piece
        """
        return Rook(move.destination, move.piece.color)

    def valid_moves(self, game_state):
        """
        Generates a list of all the valid moves this Piece can make on the game board.
        It uses the valid_move_offsets to generate all the moves
        :param game_state: the current state of the game
        :return: a list of Moves
        """
        moves = []
        for offset in Rook.valid_move_offsets:
            destination = Position.flip_board(self.position)
            while BoardProperties.valid_tile(destination):
                if Rook.in_first_column_exception(offset, destination.index) or \
                        Rook.in_eighth_column_exception(offset, destination.index):
                    break
                destination += offset
                if BoardProperties.valid_tile(destination):
                    tile_in_next_board = game_state.get_tile(destination)
                    position_in_same_board = Position.flip_board(destination)
                    tile_in_this_board = game_state.get_tile(position_in_same_board)
                    if not tile_in_next_board.is_occupied():
                        if not tile_in_this_board.is_occupied():
                            moves.append(SimpleMove(game_state, self, destination))
                        else:
                            piece_at_destination = tile_in_this_board.get_piece()
                            piece_color = piece_at_destination.color
                            if piece_color != self.color:
                                moves.append(AttackMove(game_state, self, destination,
                                                        piece_at_destination))
                            break
        return moves

    @staticmethod
    def in_first_column_exception(offset, position):
        """
        Detects the exception for First column
        :param offset: offset in picture
        :param position: current Position of the piece
        :return: True if it's in first column of the board
        """
        return BoardProperties.FIRST_COLUMN[position] and (offset == -1)

    @staticmethod
    def in_eighth_column_exception(offset, position):
        """
        Detects the exception for Eighth column
        :param offset: offset in picture
        :param position: current Position of the piece
        :return: True if it's in eighth column of the board
        """
        return BoardProperties.EIGHTH_COLUMN[position] and (offset == 1)


class Pawn(Piece):
    __doc__ = """Implements a Pawn class by inheriting Piece class."""
    valid_move_offsets = [8, 16, 7, 9]
    piece_square_table = [60, 60, 60, 60, 60, 60, 60, 60,
                          50, 50, 50, 50, 50, 50, 50, 50,
                          10, 10, 20, 30, 30, 20, 10, 10,
                           5,  5, 10, 25, 25, 10,  5,  5,
                           0,  0,  0, 20, 20,  0,  0,  0,
                           5, -5,-10,  0,  0,-10, -5,  5,
                           5, 10, 10,-20,-20, 10, 10,  5,
                           0,  0,  0,  0,  0,  0,  0,  0]

    def __init__(self, position, color, is_first_move=False):
        """
        calls __init__ of super class and sets value for this piece
        :param position: Position for this piece
        :param color: color for this piece
        :param is_first_move: True if this Pawn has not made any moves yet
        """
        Piece.__init__(self, position, color)
        self.position_value = Pawn.get_position_value(self.position.index, self.color)
        self.value = 10 + self.position_value
        self.is_first_move = is_first_move

    @staticmethod
    def get_position_value(index, color):
        """
        returns the value of position Piece is standing at
        :param index: index of tile on Board
        :param color: PlayerColor
        :return:
        """
        if color == PlayerColor.Black:
            lookup_index = BoardProperties.NUM_TILES - index - 1
        else:
            lookup_index = index
        return Pawn.piece_square_table[lookup_index]

    def __add__(self, other):
        """
        overloaded operator for forward addition
        :param other: an entity with which we add instance of this class
        :return: updated instance of this class
        """
        return self.value + other

    def __radd__(self, other):
        """
        overloaded operator for reverse addition
        :param other: an entity with which we add instance of this class
        :return: updated instance of this class
        """
        return self.value + other

    def __str__(self):
        """
        generates meaningful representation used for printing and debugging
        :return: string representation of this piece
        """
        return "P" if self.color == PlayerColor.White else "p"

    def get_direction(self):
        """
        returns a coefficient which is used to manipulate offsets according the Pawn color
        :return: -1 if it in White Player's arsenal else 1
        """
        return -1 if self.color == PlayerColor.White else 1

    def move_piece(self, move):
        """
        creates a new instance of this Piece with updated Position
        :param move: Move due to which this piece is changed
        :return: Updated instance of the Piece
        """
        return Pawn(move.destination, move.piece.color)

    def valid_moves(self, game_state):
        """
        Generates a list of all the valid moves this Piece can make on the game board.
        It uses the valid_move_offsets to generate all the moves
        :param game_state: the current state of the game
        :return: a list of Moves
        """
        moves = []
        for offset in Pawn.valid_move_offsets:
            next_index = self.position.index + (offset * self.get_direction())
            dest = Position(BoardIndex.next_board(self.position.board), next_index)
            if not BoardProperties.valid_tile(dest):
                continue
            if not game_state.get_tile(dest).is_occupied():
                flipped_pos = Position.flip_board(dest)
                if offset == 8 and not game_state.get_tile(flipped_pos).is_occupied():
                    if PlayerColor.is_pawn_promotion_square(dest, self.color):
                        moves.append(PawnPromotion(SimpleMove(game_state, self, dest)))
                    else:
                        moves.append(SimpleMove(game_state, self, dest))
                elif offset == 16 and self.is_first_move and self.first_move_config():
                    next_pos = Position(BoardIndex.next_board(self.position.board),
                                        self.position.index + (self.get_direction() * 8))
                    if not (game_state.get_tile(next_pos).is_occupied() or
                            game_state.get_tile(flipped_pos).is_occupied()):
                        moves.append(SimpleMove(game_state, self, dest))
                elif offset == 7 and not self.kill_on_left_exception():
                    tile = game_state.get_tile(flipped_pos)
                    if tile.is_occupied():
                        dest_piece = tile.get_piece()
                        piece_color = dest_piece.color
                        if piece_color != self.color:
                            if PlayerColor.is_pawn_promotion_square(dest, self.color):
                                moves.append(PawnPromotion(AttackMove(game_state, self,
                                                                      dest, dest_piece)))
                            else:
                                moves.append(AttackMove(game_state, self, dest, dest_piece))
                elif offset == 9 and not self.kill_on_right_exception():
                    tile = game_state.get_tile(flipped_pos)
                    if tile.is_occupied():
                        dest_piece = tile.get_piece()
                        piece_color = dest_piece.color
                        if piece_color != self.color:
                            if PlayerColor.is_pawn_promotion_square(dest, self.color):
                                moves.append(PawnPromotion(AttackMove(game_state, self,
                                                                      dest, dest_piece)))
                            else:
                                moves.append(AttackMove(game_state, self, dest, dest_piece))
        return moves

    def first_move_config(self):
        """
        checks if is configuration supports first move of Pawn
        :return: True if possible else False
        """
        black = self.color == PlayerColor.Black and\
                BoardProperties.SECOND_ROW[self.position.index]
        white = self.color == PlayerColor.White and\
                BoardProperties.SEVENTH_ROW[self.position.index]
        return black or white

    def kill_on_right_exception(self):
        """
        checks for exception of First and Eighth column when killing on right
        :return: True is Exception holds True else False
        """
        white = BoardProperties.EIGHTH_COLUMN[self.position.index] and\
                self.color == PlayerColor.Black
        black = BoardProperties.FIRST_COLUMN[self.position.index] and\
                self.color == PlayerColor.White
        return white or black

    def kill_on_left_exception(self):
        """
        checks for exception of First and Eighth column when killing on left
        :return: True is Exception holds True else False
        """
        white = BoardProperties.EIGHTH_COLUMN[self.position.index] and\
                self.color == PlayerColor.White
        black = BoardProperties.FIRST_COLUMN[self.position.index] and\
                self.color == PlayerColor.Black
        return white or black

    def promotion_piece(self):
        """
        Defines the Piece, Pawn can promote to.
        NOTE: Currently it promotes to only Queen
        TODO: Add more functionality to this to offer more options for promotion
        :return: Instance of Piece class at current position of piece
        """
        return Queen(self.position, self.color)


class Move:
    __doc__ = "Class to represent a move."

    def __init__(self, board, piece, destination):
        """
        Initialize the class with its properties passed in parameters
        :param board: Board(can also be called Board state) on which this move occurs
        :param piece: Piece which participate in the move
        :param destination: destination Position at which the Piece tends to move
        """
        self.board = board
        self.piece = piece
        self.destination = destination

    def __repr__(self):
        """
        Suitable representation of this move in string. Used in printing and debugging
        :return: A string representation of this move
        """
        return str(self.piece) + " := " +\
               str(self.piece.position) + "~>" +\
               str(self.destination)

    def __eq__(self, other):
        """
        overloaded operator of "==". Used to compare an entity with this object of this
        class
        :param other: an entity with which we want to compare this class's object
        :return: True if the values match else False
        """
        return self.destination == other.destination and self.piece == self.piece

    def execute_move(self):
        """
        Executes this move and generates a new representation of Board.
        :return: new/same(depends on condition) Board wrapped in MoveTransition class
                 instance
        """
        builder = BoardBuilder()
        for piece in self.board.current_player.get_active_pieces():
            if not self.piece == piece:
                builder.set_piece(piece)
        for piece in self.board.current_player.get_opponent().get_active_pieces():
            builder.set_piece(piece)
        builder.set_piece(self.piece.move_piece(self))
        builder.set_next_move_maker(self.board.current_player.get_color())
        return builder.build()

    def current_coordinate(self):
        """
        gives current Position of the piece
        :return: Position of piece before making move
        """
        return self.piece.position


class SimpleMove(Move):
    __doc__ = "Represents a normal move made by a Piece"

    def __init__(self, board, piece, destination):
        """
        initialises the class by calling __init__ of super class
        :param board: Board on which move is made
        :param piece: Piece which tends to move
        :param destination: destination Position of this Move
        """
        Move.__init__(self, board, piece, destination)
        self.value = self.piece.get_position_value(self.piece.position.index,
                                                   self.piece.color)

    def __add__(self, other):
        """
        overloaded operator for forward addition
        :param other: an entity with which we add instance of this class
        :return: updated instance of this class
        """
        return self.value + other

    def __radd__(self, other):
        """
        overloaded operator for reverse addition
        :param other: an entity with which we add instance of this class
        :return: updated instance of this class
        """
        return self.value + other

    def is_attack(self):
        """
        returns False as it is not a Attack Move
        :return: False
        """
        return False

    def attacked_piece(self):
        """
        returns None as the move is not attacking any Piece
        :return: None
        """
        return None


class AttackMove(Move):
    __doc__ = "Represents an attack move made by a Piece"

    def __init__(self, board, piece, destination, attacked_piece):
        """
        initialises the class by calling __init__ of super class
        :param board: Board on which move is made
        :param piece: Piece which tends to move
        :param destination: destination Position of this Move
        :param attacked_piece: Piece under attack
        """
        Move.__init__(self, board, piece, destination)
        self.attacked_piece = attacked_piece
        self.value = self.piece.get_position_value(self.piece.position.index,
                                                   self.piece.color) + self.attacked_piece

    def __eq__(self, other):
        """
        overloading "==" operator to compare other entity with entity of this class
        :param other: an entity which needs to be compared with this class's entity
        :return: True if values match else False
        """
        return super.__eq__(other) and self.attacked_piece == other.attacked_piece

    def __add__(self, other):
        """
        overloaded operator for forward addition
        :param other: an entity with which we add instance of this class
        :return: updated instance of this class
        """
        return self.value + other

    def __radd__(self, other):
        """
        overloaded operator for reverse addition
        :param other: an entity with which we add instance of this class
        :return: updated instance of this class
        """
        return self.value + other

    def execute_move(self):
        """
        Executes this move and generates a new representation of Board.
        :return: new/same(depends on condition) Board wrapped in MoveTransition class
                 instance
        """
        builder = BoardBuilder()
        for piece in self.board.current_player.get_active_pieces():
            if not self.piece == piece:
                builder.set_piece(piece)
        for piece in self.board.current_player.get_opponent().get_active_pieces():
            if not piece == self.attacked_piece:
                builder.set_piece(piece)
        builder.set_piece(self.piece.move_piece(self))
        builder.set_next_move_maker(self.board.current_player.get_color())
        return builder.build()

    def is_attack(self):
        """
        returns True as this is an Attack Move
        :return: True
        """
        return True

    def attacked_piece(self):
        """
        returns the Piece under attack
        :return: Piece under attack
        """
        return self.attacked_piece


class PawnPromotion(Move):
    __doc__ = "Represents the Pawn Promotion class"

    def __init__(self, move):
        """
        Initialize the class with the move getting made and the Promoted Piece
        :param move: Move which causes PawnPromotion
        """
        Move.__init__(self, move.board, move.piece, move.destination)
        self.move = move
        self.promotedPawn = move.piece
        self.value = 2 * move.value

    def __add__(self, other):
        """
        overloaded operator for forward addition
        :param other: an entity with which we add instance of this class
        :return: updated instance of this class
        """
        return self.value + other

    def __radd__(self, other):
        """
        overloaded operator for reverse addition
        :param other: an entity with which we add instance of this class
        :return: updated instance of this class
        """
        return self.value + other

    def __repr__(self):
        """
        Suitable representation of this move in string. Used in printing and debugging
        :return: A string representation of this move
        """
        return str(self.promotedPawn.promotion_piece()) + "(" + str(self.move) + ")"

    def __eq__(self, other):
        """
        overloading "==" operator to compare other entity with entity of this class
        :param other: an entity which needs to be compared with this class's entity
        :return: True if values match else False
        """
        if isinstance(other, PawnPromotion):
            return self.move == other.move
        return False

    def is_attack(self):
        """
        returns True if the enclosed move is an AttackMove
        :return: True if enclosed move is AttackMove else False
        """
        return self.move.is_attack()

    def attacked_piece(self):
        """
        used to retrieve attacked piece
        :return: the Piece under attack in case its an AttackMove else None
        """
        return self.move.attacked_piece()

    def execute_move(self):
        """
        Executes this move and generates a new representation of Board.
        :return: new/same(depends on condition) Board wrapped in MoveTransition class
                 instance
        """
        board = self.move.execute_move()
        board_builder = BoardBuilder()
        for piece in board.current_player.get_active_pieces():
            if not self.promotedPawn == piece:
                board_builder.set_piece(piece)
        for piece in board.current_player.get_opponent().get_active_pieces():
            board_builder.set_piece(piece)
        board_builder.set_piece(self.promotedPawn.promotion_piece().move_piece(self))
        board_builder.next_move_maker = board.current_player.get_opponent().get_color()
        return board_builder.build()


class MoveStatus():
    __doc__ = "A wrapper class which consists of all the status game can be"
    DONE = "Done"
    ILLEGAL_MOVE = "Illegal Move"
    LEAVES_KING_IN_CHECK = "Leaves King in check"


class MoveTransition:
    __doc__ = "a representation of the transition after a move is executed"

    def __init__(self, board, move, move_status):
        """
        set all board, move and status after executing that move
        :param board: Board after executing given Move. It will be same as before if
                      the Move was Illegal
        :param move: Move which got executed on a board
        :param move_status: Status of move on current state of the game.
        NOTE: If MoveStatus.ILLEGAL_MOVE or MOVE_STATUS.LEAVES_KING_IN_CHECK is
              encountered, the transition_board would be same as last state on which the
              move was made
        """
        self.transition_board = board
        self.move = move
        self.move_status = move_status


class Player:
    __doc__ = "Represents a player in the game and encloses all the properties related " \
              "to it"

    def __init__(self, board, legal_moves, opponent_moves):
        """
        Initialises with board, moves and opponent moves
        :param board: Board on which this Player is playing
        :param legal_moves: list moves valid in this state, for this player
        :param opponent_moves: list moves valid in this state, for other player
        """
        self.board = board
        self.player_king = self.establish_king()
        self.legal_moves = legal_moves
        self.opponents_moves = opponent_moves

    def establish_king(self):
        pass

    def is_legal_move(self, move):
        """
        checks if the given move is legal
        :param move: Move instance
        :return: True if the Player has that Move in his strategy else False
        """
        return move in self.legal_moves

    @staticmethod
    def calculate_attacks_on_tile(tile, opponents_moves):
        """
        Calculates attacks on a given tile
        :param tile: Tile on which attacks are to be determined
        :param opponents_moves: Moves this Player's opponent can make in current state
        :return: list of all the AttackMoves on the given Tile
        """
        attacking_moves = []
        for move in opponents_moves:
            if tile == Position.flip_board(move.destination):
                attacking_moves.append(move)
        return attacking_moves

    def has_escape_moves(self):
        """
        Checks if there any moves to escape check
        :return: True if there exists escaping moves
        """
        for move in self.legal_moves:
            transit = self.make_move(move)
            if transit.move_status == MoveStatus.DONE:
                return True
        return False

    def get_escape_moves(self):
        """
        gets all the moves which can avoid check
        :return: list of moves this Player can make to avoid or escape from a check
        """
        escape_moves = []
        for move in self.legal_moves:
            transit_here = self.make_move_without_changing_board(move)
            transit_there = self.make_move(move)
            if transit_here.move_status == MoveStatus.DONE and \
                    transit_there.move_status == MoveStatus.DONE:
                escape_moves.append(move)
        return escape_moves

    def is_in_check(self):
        """
        looks for a check on this Player's King
        :return: True there is a check else False
        """
        return not len(self.calculate_attacks_on_tile(self.player_king.position,
                                                      self.opponents_moves)) == 0

    def is_in_check_mate(self):
        """
        looks for a checkmate situation
        :return: True if the Player is in checkmate else False
        """
        return self.is_in_check() and not self.has_escape_moves()

    def is_in_stale_mate(self):
        """
        looks for a checkmate situation
        :return: True if the Player is in stalemate situation else False
        """
        return (not self.is_in_check()) and (not self.has_escape_moves())

    def make_move(self, move):
        """
        makes a Move if the Move is legal
        :param move: Move to be made
        :return: MoveTransition after making given Move
        """
        move_trans = self.make_move_without_changing_board(move)
        if move_trans.move_status == MoveStatus.DONE:
            transition_board = move.execute_move()
            king_attacks = Player.calculate_attacks_on_tile(
                transition_board.current_player.get_opponent().player_king.position,
                transition_board.current_player.legal_moves)
            if len(king_attacks) != 0:
                return MoveTransition(self.board, move, MoveStatus.LEAVES_KING_IN_CHECK)
            return MoveTransition(transition_board, move, MoveStatus.DONE)
        else:
            return move_trans

    def make_move_without_changing_board(self, move):
        """
        makes a Move on same board if the Move is legal
        :param move: Move to be made
        :return: MoveTransition after making given Move
        """
        if not self.is_legal_move(move):
            return MoveTransition(self.board, move, MoveStatus.ILLEGAL_MOVE)
        new_move = deepcopy(move)
        new_move.destination = new_move.destination.flip_board()
        transition_board = new_move.execute_move()
        king_attacks = Player.calculate_attacks_on_tile(
                transition_board.current_player.get_opponent().player_king.position,
                transition_board.current_player.legal_moves)
        if len(king_attacks) != 0:
            return MoveTransition(self.board, move, MoveStatus.LEAVES_KING_IN_CHECK)
        return MoveTransition(transition_board, move, MoveStatus.DONE)


class WhitePlayer(Player):
    __doc__ = "represents WhitePlayer inherits from Player class"

    def __init__(self, board, my_moves, other_moves):
        """
        calls the __init__ of super class
        :param board: Board on which this player plays
        :param my_moves: moves for this Player
        :param other_moves: moves with Opponent
        """
        Player.__init__(self, board, my_moves, other_moves)

    def establish_king(self):
        """
        ensure the King is present else raise an Exception
        :return: King class instance
        """
        for piece in self.get_active_pieces():
            if isinstance(piece, King):
                piece.__class__ = King
                return piece
        raise Exception("White King missing")

    def get_active_pieces(self):
        """
        gets the current arsenal of this Player
        :return: list of all Pieces in this Player's arsenal
        """
        return self.board.white_piece

    def get_opponent(self):
        """
        gets opponent of this Player
        :return: BlackPlayer instance
        """
        return self.board.black_player

    @staticmethod
    def get_color():
        """
        gets color of the current color
        :return: PlayerColor of the current player
        """
        return PlayerColor.White


class BlackPlayer(Player):
    __doc__ = "represents BlackPlayer inherits from Player class"

    def __init__(self, board, my_moves, other_moves):
        """
        calls the __init__ of super class
        :param board: Board on which this player plays
        :param my_moves: moves for this Player
        :param other_moves: moves with Opponent
        """
        Player.__init__(self, board, my_moves, other_moves)

    def establish_king(self):
        """
        ensure the King is present else raise an Exception
        :return: King class instance
        """
        for piece in self.get_active_pieces():
            if isinstance(piece, King):
                piece.__class__ = King
                return piece
        raise Exception("Black King missing")

    def get_active_pieces(self):
        """
        gets the current arsenal of this Player
        :return: list of all Pieces in this Player's arsenal
        """
        return self.board.black_piece

    def get_opponent(self):
        """
        gets opponent of this Player
        :return: WhitePlayer instance
        """
        return self.board.white_player

    @staticmethod
    def get_color():
        """
        gets color of the current color
        :return: PlayerColor of the current player
        """
        return PlayerColor.Black
