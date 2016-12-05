import sys
import random
from aliceengine import *

########################################################################################################################

"""Generating sequence of meanigful messages"""


def generate_move_sentence(move):
    list_of_values = list()
    list_of_values.append(my_team_color)
    list_of_values.append("moves")
    list_of_values.append(str(move.piece).upper())
    list_of_values.append("from")
    list_of_values.append(move.piece.position.board)
    list_of_values.append(Position.int_to_alg(move.piece.position.index))
    list_of_values.append("to")
    list_of_values.append(Position.int_to_alg(move.destination.index))
    return " ".join(list_of_values) + "\n"


def does_this_move_creates_check(move):
    partial_move_transition = game.current_player.make_move_without_changing_board(move)
    if partial_move_transition.move_status == MoveStatus.LEAVES_KING_IN_CHECK:
        return True
    return False


def analyse_state():
    player = game.current_player
    player_legal_moves = []
    for move in player.legal_moves:
        if not does_this_move_creates_check(move):
            player_legal_moves.append(move)
    player.legal_moves = player_legal_moves


def choose_move():
    player_legal_moves = game.current_player.legal_moves
    if len(player_legal_moves) == 0:
        sys.stdout.write(my_team_color + " surrenders\n")
        sys.exit(0)
    # TODO: move choosing strategy; currently random
    move_index = random.randrange(len(player_legal_moves))
    return player_legal_moves[move_index]


def make_move(move):
    move_transition = game.current_player.make_move(move)
    if not move_transition.move_status == MoveStatus.DONE:
        sys.stdout.write(my_team_color + " surrenders\n")
        debug_file.write("move_transition.move_status != MoveStatus.DONE")
        sys.exit(0)
    return move_transition.transition_board


def text_to_move(moves, piece, board, source, destination):
    for move in moves:
        if str(move.piece).upper() == piece \
                and move.piece.position.board == board \
                and move.piece.position.index == Position.alg_to_int(source) \
                and move.destination.index == Position.alg_to_int(destination):
            return move


def create_custom_board():
    game_builder = BoardBuilder()
    game_builder.set_piece(Pawn(Position(BoardIndex.Board_One, 14), PlayerColor.White))
    game_builder.set_piece(King(Position(BoardIndex.Board_One, 4), PlayerColor.White))
    game_builder.set_piece(King(Position(BoardIndex.Board_One, 50), PlayerColor.Black))
    return game_builder.build()


end = False
# game = Board.create_standard_board()
game = create_custom_board()
my_team_color = None
my_team = None
debug_file = open('debug.txt', 'w')
while not end:
    input_message = raw_input()

    if "you are " in input_message:
        if "black" in input_message:
            my_team_color = PlayerColor.Black
            my_team = game.black_player
        else:
            my_team_color = PlayerColor.White
            my_team = game.white_player
            analyse_state()
            move = choose_move()
            game = make_move(move)
            sys.stdout.write(generate_move_sentence(move))

    elif "moves" in input_message:
        message = input_message.split()
        assert game.current_player.get_color() == message[0]
        move = text_to_move(game.current_player.legal_moves, message[2], message[4], message[5], message[7])
        choose_move()
        game = make_move(move)
        if game.current_player.get_color() == my_team.get_color():
            analyse_state()
            print game.current_player.legal_moves
            move = choose_move()
            game = make_move(move)
            sys.stdout.write(generate_move_sentence(move))
            debug_file.write("move occured\n")
        else:
            sys.stdout.write(my_team_color + " surrenders\n")
            debug_file.write("because game.current_player.get_color() != my_team.get_color()")
        """
        print game
        message1 = raw_input()
        message1 = message1.split()
        assert game.current_player.get_color() == message1[0]
        move = text_to_move(game.current_player.legal_moves, message1[2], message1[4], message1[5], message1[7])
        game = make_move(move)
        """

    elif "wins" in input_message or "loses" in input_message or "drawn" in input_message:
        end = True
        sys.exit(0)

    elif " offers draw" in input_message:
        sys.stdout.write(my_team_color + " accepts draw\n")
        end = True
        sys.exit(0)
    # print choose_move()
    print game
    sys.stdin.flush()
    sys.stdout.flush()
