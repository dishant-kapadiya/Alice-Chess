from enum import Enum
import sys
import random
from aliceengine

########################################################################################################################

"""Generating sequence of meanigful messages"""

# """


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


def choose_move():
    player = game.current_player
    player_legal_moves = player.legal_moves
    #TODO: come up with better stratagies for choosing a move
    move_index = random.randrange(len(player_legal_moves))
    return player_legal_moves[move_index]


def make_move(move):
    move_transition = game.current_player.make_move(move)
    if not move_transition.move_status == MoveStatus.DONE:
        sys.stdout.write(my_team_color + " surrenders\n")
        sys.exit(0)
    return move_transition.transition_board


def text_to_move(moves, piece, board, source, destination):
    for move in moves:
        if str(move.piece).upper() == piece \
                and move.piece.position.board == board \
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
            my_team_color = PlayerColor.Black
            my_team = game.black_player
        else:
            my_team_color = PlayerColor.White
            my_team = game.white_player
            move = choose_move()
            game = make_move(move)
            sys.stdout.write(generate_move_sentence(move))

    elif "moves" in input_message:
        message = input_message.split()
        assert game.current_player.get_color() == message[0]
        move = text_to_move(game.current_player.legal_moves, message[2], message[4], message[5], message[7])
        game = make_move(move)
        # if game.current_player.get_color() == my_team.get_color():
        #     move = choose_move()
        #     game = make_move(move)
        #     sys.stdout.write(generate_move_sentence(move))
        # else:
        #     sys.stdout.write(my_team_color + " surrenders\n")
        print game
        message1 = raw_input()
        message1 = message1.split()
        assert game.current_player.get_color() == message1[0]
        move = text_to_move(game.current_player.legal_moves, message1[2], message1[4], message1[5], message1[7])
        game = make_move(move)

    elif "wins" in input_message or "loses" in input_message or "drawn" in input_message:
        end = True
        sys.exit(0)

    elif " offers draw" in input_message:
        sys.stdout.write(my_team_color + " accepts draw\n")
        end = True
        sys.exit(0)
    print game
    sys.stdin.flush()
    sys.stdout.flush()
