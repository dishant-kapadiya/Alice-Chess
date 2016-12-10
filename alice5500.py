import sys
import time
from aliceengine import *
import operator
import random

print_msgs = False
common_threshold = 0.25

def get_current_and_opponent_players(state):
    """
    identifies which team color the program is playing as and the opponent
    :param state: instance of Board representing a state of the game
    :return: a list where 1st element is our team and 2nd element is the opponent
    """
    if my_team_color == PlayerColor.White:
        return [state.white_player, state.black_player]
    else:
        return [state.black_player, state.white_player]


def evaluate_state(my_player, other_player):
    """
    calculates and evaluates a score for the state
    :param my_player: an instance of the Player class representing our team
    :param other_player: an instance of the Player class representing the opponent
    :return: an integer score that evaluates the state
    """
    evaluation = sum(my_player.get_active_pieces()) - sum(other_player.get_active_pieces())
    my_mobility = sum(my_player.legal_moves)
    other_mobility = sum(other_player.legal_moves)
    check_bonus = 0
    if my_player.is_in_check():
        check_bonus = -50
    if other_player.is_in_check():
        check_bonus = 50
    return evaluation + 0.1 * (my_mobility - other_mobility) + check_bonus


"""#######################################################################################
################################## Alpha-Beta Pruning ####################################
#######################################################################################"""


def alpha_beta_pruning(state):
    """
    implements alpha-beta pruning algorithm on the given state
    :param state: instance of Board representing a state of the game
    :return: an instance of Move
    """
    legal_moves = state.current_player.legal_moves
    best_move = legal_moves[0]
    possible_score = float("-inf")
    alpha = float("-inf")
    beta = float("inf")
    legal_moves.sort(key=operator.attrgetter('value'), reverse=True)
    avg_time = sum(times)/len(times)
    diff = avg_time_constant - avg_time
    threshold = 0.1
    avail_time = avg_time_constant + diff
    current_depth = 1
    while avail_time > threshold:
        start_time = time.time()
        for move in legal_moves:
            old_score = possible_score
            next_state = state.current_player.make_move(move)
            if next_state.move_status == MoveStatus.DONE:
                if print_msgs:
                    print "Trying ", str(move)
                # analyse_state(next_state.transition_board)
                t0 = time.time()
                possible_score = max(possible_score, alpha_beta_min(next_state.transition_board,
                                                                    alpha, beta,
                                                                    avail_time,
                                                                    depth=current_depth))
                t1 = time.time()
                avail_time -= (t1 - t0)
                if avail_time <= common_threshold:
                    break
                if old_score < possible_score:
                    best_move = move
                alpha = max(alpha, possible_score)
        end_time = time.time()
        times.append(end_time - start_time)
        avail_time -= times[-1]
        debug.write("(" + str(current_depth) + " , " + str(times[-1]) + ")\n")
        threshold += times[-1] ** current_depth
        current_depth += 1
    return best_move


def alpha_beta_min(state, alpha, beta, avail_time, depth):
    """
    minimizer node analyzing the opponents moves
    :param state: instance of Board representing a state of the game
    :param alpha: an integer value representing the lower bound for apb
    :param beta: an integer value representing the upper bound for apb
    :param depth: an integer value representing how deep into the search tree apb goes
    :return: an integer value that chooses the minimum from the child nodes
    """
    my_player, other_player = get_current_and_opponent_players(state)
    if depth == 0 or avail_time <= common_threshold:
        score = depth * evaluate_state(my_player, other_player)
        if print_msgs:
            print "\t"*depth, "(MIN)Returned = ", score
        return score
    legal_moves = state.current_player.legal_moves
    val = float("inf")
    legal_moves.sort(key=operator.attrgetter('value'), reverse=True)
    for move in legal_moves:
        next_state = state.current_player.make_move(move)
        if next_state.move_status == MoveStatus.DONE:
            if print_msgs:
                print "\t" * depth, depth, ": Trying ", str(move)
            t0 = time.time()
            # analyse_state(next_state.transition_board)
            val = min(val, alpha_beta_max(next_state.transition_board, alpha, beta,
                                          avail_time, depth - 1))
            t1 = time.time()
            difference = t1 - t0
            avail_time -= difference
            if avail_time <= common_threshold:
                return val

            if val < alpha:
                if print_msgs:
                    print depth, " : PRUNED!"
                return val
            beta = min(beta, val)
    return val


def alpha_beta_max(state, alpha, beta, avail_time, depth=1):
    """
    maximizer node analyzing our teams' moves
    :param state: instance of Board representing a state of the game
    :param alpha: an integer value representing the lower bound for apb
    :param beta: an integer value representing the upper bound for apb
    :param depth: an integer value representing how deep into the search tree apb goes
    :return: an integer value that chooses the maximum from the child nodes
    """
    my_player, other_player = get_current_and_opponent_players(state)
    if depth == 0 or avail_time <= common_threshold:
        score = depth * evaluate_state(my_player, other_player)
        if print_msgs:
            print "\t" * depth, "(MAX)Returned = ", score
        return score
    legal_moves = state.current_player.legal_moves
    val = float("-inf")
    legal_moves.sort(key=operator.attrgetter('value'), reverse=True)
    for move in legal_moves:
        next_state = state.current_player.make_move(move)
        if next_state.move_status == MoveStatus.DONE:
            if print_msgs:
                print "\t" * depth, depth, ": Trying ", str(move)
            # analyse_state(next_state.transition_board)
            t0 = time.time()
            val = max(val, alpha_beta_min(next_state.transition_board, alpha, beta,
                                          avail_time, depth - 1))
            t1 = time.time()
            difference = t1 - t0
            avail_time -= difference
            if avail_time <= common_threshold:
                return val

            if val > beta:
                if print_msgs:
                    print depth, " : PRUNED!"
                return val
            alpha = max(alpha, val)
    return val

"""#######################################################################################
########################################## MIN-MAX #######################################
#######################################################################################"""


def min_max(state):
    """
    implements mini-max algorithm on the given state
    :param state: instance of Board representing a state of the game
    :return: an instance of Move
    """
    legal_moves = state.current_player.legal_moves
    best_move = legal_moves[0]
    best_score = float("-inf")
    for move in legal_moves:
        next_state = state.current_player.make_move(move)
        if next_state.move_status == MoveStatus.DONE:
            # analyse_state(next_state.transition_board)
            score = minimizer(next_state.transition_board)
            if score > best_score:
                best_score = score
                best_move = move
    return best_move


def minimizer(state, depth=1):
    """
    minimizer node analyzing the opponents moves
    :param state: instance of Board representing a state of the game
    :param depth: an integer value representing how deep into the search tree minimax goes
    :return: an integer value that chooses the minimum from the child nodes
    """
    my_piece, other_piece = get_current_and_opponent_players(state)
    if depth == max_depth:
        return (5 / depth) * evaluate_state(my_piece, other_piece)
    legal_moves = state.current_player.legal_moves
    best_score = float("inf")
    for move in legal_moves:
        next_state = state.current_player.make_move(move)
        if next_state.move_status == MoveStatus.DONE:
            # analyse_state(next_state.transition_board)
            score = maximizer(next_state.transition_board, depth + 1)
            if score < best_score:
                best_score = score
    return best_score


def maximizer(state, depth=1):
    """
    maximizer node analyzing the opponents moves
    :param state: instance of Board representing a state of the game
    :param depth: an integer value representing how deep into the search tree minimax goes
    :return: an integer value that chooses the maximum from the child nodes
    """
    my_piece, other_piece = get_current_and_opponent_players(state)
    if depth == max_depth:
        return (5 / depth) * evaluate_state(my_piece, other_piece)
    legal_moves = state.current_player.legal_moves
    best_score = float("-inf")
    for move in legal_moves:
        next_state = state.current_player.make_move(move)
        if next_state.move_status == MoveStatus.DONE:
            # analyse_state(next_state.transition_board)
            score = minimizer(next_state.transition_board, depth + 1)
            if score > best_score:
                best_score = score
    return best_score


"""#######################################################################################
#######################################################################################"""


def generate_move_sentence(move):
    """
    generates a syntaxually valid move sentence
    :param move: an instance of Move
    :return: a string value with a valid move to communicate to referee
    """
    if isinstance(move, PawnPromotion):
        move = move.move
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
    """
    looks at all legal moves and implements a search algorithm to find best move
    :return: an instance of Move
    """
    player_legal_moves = game.current_player.legal_moves
    if len(player_legal_moves) == 0:
        sys.stdout.write(my_team_color + " surrenders\n")
        sys.exit(0)
    t0 = time.time()
    # move = min_max(game)
    move = alpha_beta_pruning(game)
    t1 = time.time()
    times.append(t1 - t0)
    if print_msgs:
        print times[-1]
    # move_index = random.randrange(len(player_legal_moves))
    # move = player_legal_moves[move_index]
    return move


def make_move(move):
    """
    implements a move on the current game state
    :param move: an instance of Move
    :return: an updated instance of Board after implementing Move
    """
    move_transition = game.current_player.make_move(move)
    if not move_transition.move_status == MoveStatus.DONE:
        sys.stdout.write(my_team_color + " surrenders\n")
        # debug.write("move_transition.move_status != MoveStatus.DONE")
        sys.exit(0)
    return move_transition.transition_board


def choose_random_move(game):
    """
    chooses a random doable move
    :param game: game instance
    :return: Move
    """
    player = game.current_player
    moves = player.legal_moves
    for i in range(len(moves)):
        index = random.randrange(len(moves))
        move_temp = moves[index]
        trans = player.make_move(move_temp)
        if trans.move_status == MoveStatus.DONE:
            return move_temp
        else:
            moves.remove(move_temp)

def text_to_move(moves, piece, board, source, destination):
    """
    searches the given list of moves and finds the move with the characteristics
    of the other parameters
    :param moves: list of instances of Move
    :param piece: a string character representing a piece
    :param board: a string character representing the board
    :param source: a string representing the start position of move
    :param destination: a string representing the destination of move
    :return: an instance of Move
    """
    for move in moves:
        if str(move.piece).upper() == piece \
                and move.piece.position.board == board \
                and move.piece.position.index == Position.alg_to_int(source) \
                and move.destination.index == Position.alg_to_int(destination):
            return move


def create_custom_board():
    """
    creates a custom board for testing purposes
    :return: an instance of Board
    """
    builder = BoardBuilder()
    # Black Arsenal
    builder.set_piece(Rook(Position(BoardIndex.Board_Two, 24), PlayerColor.Black))
    builder.set_piece(Knight(Position(BoardIndex.Board_Two, 25), PlayerColor.Black))
    builder.set_piece(Bishop(Position(BoardIndex.Board_Two, 26), PlayerColor.Black))
    builder.set_piece(Queen(Position(BoardIndex.Board_Two, 27), PlayerColor.Black))
    builder.set_piece(King(Position(BoardIndex.Board_Two, 28), PlayerColor.Black))
    builder.set_piece(Bishop(Position(BoardIndex.Board_Two, 29), PlayerColor.Black))
    builder.set_piece(Knight(Position(BoardIndex.Board_Two, 30), PlayerColor.Black))
    builder.set_piece(Rook(Position(BoardIndex.Board_Two, 31), PlayerColor.Black))
    # White Arsenal
    builder.set_piece(Rook(Position(BoardIndex.Board_One, 32), PlayerColor.White))
    builder.set_piece(Knight(Position(BoardIndex.Board_One, 33), PlayerColor.White))
    builder.set_piece(Bishop(Position(BoardIndex.Board_One, 34), PlayerColor.White))
    builder.set_piece(Queen(Position(BoardIndex.Board_One, 35), PlayerColor.White))
    builder.set_piece(King(Position(BoardIndex.Board_One, 36), PlayerColor.White))
    builder.set_piece(Bishop(Position(BoardIndex.Board_One, 37), PlayerColor.White))
    builder.set_piece(Knight(Position(BoardIndex.Board_One, 38), PlayerColor.White))
    builder.set_piece(Rook(Position(BoardIndex.Board_One, 39), PlayerColor.White))
    builder.set_piece(Pawn(Position(BoardIndex.Board_One, 8), PlayerColor.White))
    builder.set_next_move_maker(PlayerColor.Black)
    return builder.build()


end = False
game = Board.create_standard_board()
# game = create_custom_board()
my_team_color = None
my_team = None
debug = open('debug.txt', 'w')
max_depth = 2
times = [1]
avg_time_constant = 1
while not end:
    input_message = raw_input()
    if "you are " in input_message:
        if "black" in input_message:
            my_team_color = PlayerColor.Black
            my_team = game.black_player
        else:
            my_team_color = PlayerColor.White
            my_team = game.white_player
            # analyse_state(game)
            move = choose_move()
            game = make_move(move)
            sys.stdout.write(generate_move_sentence(move))

    elif "moves" in input_message:
        message = input_message.split()
        assert game.current_player.get_color() == message[0]
        move = text_to_move(game.current_player.legal_moves, message[2], message[4],
                            message[5], message[7])
        game = make_move(move)
        if game.current_player.get_color() == my_team.get_color():
            move = choose_move()
            game = make_move(move)
            sys.stdout.write(generate_move_sentence(move))
            # debug.write("move occured\n")
        else:
            sys.stdout.write(my_team_color + " surrenders\n")
            # debug.write("because game.current_player.get_color() != my_team.get_color()")
        """
        analyse_state(game)
        print game.current_player.legal_moves
        print game
        message1 = raw_input()
        message1 = message1.split()
        assert game.current_player.get_color() == message1[0]
        move = text_to_move(game.current_player.legal_moves, message1[2], message1[4],
                            message1[5], message1[7])
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
    # analyse_state(game)
    if print_msgs:
        print game
    sys.stdin.flush()
    sys.stdout.flush()
