import sys
import random
import time
from aliceengine import *

########################################################################################################################

"""Generating sequence of meanigful messages"""

max_depth = 2


def does_this_move_creates_check(state, move):
    partial_move_transition = state.current_player.make_move_without_changing_board(move)
    if partial_move_transition.move_status == MoveStatus.LEAVES_KING_IN_CHECK:
        return True
    return False


def analyse_state(state):
    player = state.current_player
    player_legal_moves = []
    for move in player.legal_moves:
        if not does_this_move_creates_check(state, move):
            player_legal_moves.append(move)
    player.legal_moves = player_legal_moves


def get_current_and_opponent_players(state):
    if my_team_color == PlayerColor.White:
        return [state.white_player, state.black_player]
    else:
        return [state.black_player, state.white_player]


def evaluate_state(my_player, other_player):
    evaluation = sum(my_player.get_active_pieces()) - sum(other_player.get_active_pieces())
    my_pawn_score = my_player.pawn_score()
    other_pawn_score = other_player.pawn_score()
    my_mobility = len(my_player.legal_moves) + float(1 / len(other_player.legal_moves))
    other_mobility = len(other_player.legal_moves) + float(1 / len(my_player.legal_moves))
    return evaluation + 0.5 * (my_pawn_score - other_pawn_score) + 0.1 * (my_mobility - other_mobility)


"""#####################################################################################################################
############################################### Alpha-Beta Pruning ##################################################"""


def alpha_beta_pruning(state):
    legal_moves = state.current_player.legal_moves
    best_move = legal_moves[0]
    possible_score = float("-inf")
    alpha = float("-inf")
    beta = float("inf")
    for move in legal_moves:
        old_score = possible_score
        next_state = state.current_player.make_move(move)
        if next_state.move_status == MoveStatus.DONE:
            analyse_state(next_state.transition_board)
            possible_score = max(possible_score, alpha_beta_minimizer(next_state.transition_board, alpha, beta))
            if old_score < possible_score:
                best_move = move
            alpha = max(alpha, possible_score)
    return best_move


def alpha_beta_minimizer(state, alpha, beta, depth=1):
    my_player, other_player = get_current_and_opponent_players(state)
    if depth == max_depth:
        return (5 / depth) * evaluate_state(my_player, other_player)
    legal_moves = state.current_player.legal_moves
    val = float("inf")
    for move in legal_moves:
        next_state = state.current_player.make_move(move)
        if next_state.move_status == MoveStatus.DONE:
            analyse_state(next_state.transition_board)
            val = min(val, alpha_beta_maximizer(next_state.transition_board, alpha, beta, depth + 1))
            if val < alpha:
                return val
            beta = min(beta, val)
    return val


def alpha_beta_maximizer(state, alpha, beta, depth=1):
    my_player, other_player = get_current_and_opponent_players(state)
    if depth == max_depth:
        return (5 / depth) * evaluate_state(my_player, other_player)
    legal_moves = state.current_player.legal_moves
    val = float("-inf")
    for move in legal_moves:
        next_state = state.current_player.make_move(move)
        if next_state.move_status == MoveStatus.DONE:
            analyse_state(next_state.transition_board)
            val = max(val, alpha_beta_minimizer(next_state.transition_board, alpha, beta, depth + 1))
            if val > beta:
                return val
            alpha = max(alpha, val)
    return val


"""#####################################################################################################################
#################################################### MIN MAX ########################################################"""


def min_max(state):
    legal_moves = state.current_player.legal_moves
    best_move = legal_moves[0]
    best_score = float("-inf")
    for move in legal_moves:
        next_state = state.current_player.make_move(move)
        if next_state.move_status == MoveStatus.DONE:
            analyse_state(next_state.transition_board)
            score = minimizer(next_state.transition_board)
            if score > best_score:
                best_score = score
                best_move = move
    return best_move


def minimizer(state, depth=1):
    my_piece, other_piece = get_current_and_opponent_players(state)
    if depth == max_depth:
        return (5 / depth) * evaluate_state(my_piece, other_piece)
    legal_moves = state.current_player.legal_moves
    best_score = float("inf")
    for move in legal_moves:
        next_state = state.current_player.make_move(move)
        if next_state.move_status == MoveStatus.DONE:
            analyse_state(next_state.transition_board)
            score = maximizer(next_state.transition_board, depth + 1)
            if score < best_score:
                best_score = score
    return best_score


def maximizer(state, depth=1):
    my_piece, other_piece = get_current_and_opponent_players(state)
    if depth == max_depth:
        return (5 / depth) * evaluate_state(my_piece, other_piece)
    legal_moves = state.current_player.legal_moves
    best_score = float("-inf")
    for move in legal_moves:
        next_state = state.current_player.make_move(move)
        if next_state.move_status == MoveStatus.DONE:
            analyse_state(next_state.transition_board)
            score = minimizer(next_state.transition_board, depth + 1)
            if score > best_score:
                best_score = score
    return best_score


"""#####################################################################################################################
#####################################################################################################################"""


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
    player_legal_moves = game.current_player.legal_moves
    if len(player_legal_moves) == 0:
        sys.stdout.write(my_team_color + " surrenders\n")
        sys.exit(0)
    # move = min_max(game)
    t0 = time.time()
    move = alpha_beta_pruning(game)
    t1 = time.time()
    times.append(t1 - t0)
    # move_index = random.randrange(len(player_legal_moves))
    return move


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
game = Board.create_standard_board()
# game = create_custom_board()
evaluate_state(game.white_player, game.black_player)
analyse_state(game)
my_team_color = None
my_team = None
# print min_max(game)
debug_file = open('debug.txt', 'w')
times = []
while not end:
    input_message = raw_input()

    if "you are " in input_message:
        if "black" in input_message:
            my_team_color = PlayerColor.Black
            my_team = game.black_player
        else:
            my_team_color = PlayerColor.White
            my_team = game.white_player
            analyse_state(game)
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
            analyse_state(game)
            # print game.current_player.legal_moves
            move = choose_move()
            game = make_move(move)
            sys.stdout.write(generate_move_sentence(move))
            debug_file.write("move occured\n")
        else:
            sys.stdout.write(my_team_color + " surrenders\n")
            debug_file.write("because game.current_player.get_color() != my_team.get_color()")
        """
        print game.current_player.legal_moves
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
    # print game.current_player.legal_moves
    print game
    sys.stdin.flush()
    sys.stdout.flush()
