#!/usr/bin/env python

import random
import sys

from player import Player
from pawn import Pawn
from rook import Rook
from knight import Knight
from bishop import Bishop
from queen import Queen
from king import King


from game import Game

def generate_move_sentence(param):
    return "{0} moves {1} from {2} {3} to {4}\n".format(param[0],
                                                        param[1],
                                                        str(param[2]),
                                                        param[3],
                                                        param[4])


def evaluate_game_state(my_team, other_team):
    my_arsenal = my_team.arsenal
    other_arsenal = other_team.arsenal

    # print my_arsenal
    # print other_arsenal
    my_score = evaluate_arsenal(my_arsenal)
    other_score = evaluate_arsenal(other_arsenal)

    return my_score - other_score

def evaluate_arsenal(arsenal):
    score = 0
    for piece in arsenal:
        if isinstance(piece, Pawn):
            score += 1

        if isinstance(piece, Knight):
            score += 5

        if isinstance(piece, Bishop):
            score += 6

        if isinstance(piece, Rook):
            score += 7

        if isinstance(piece, Queen):
            score += 9

        if isinstance(piece, King):
            score += 10
    return score

global my_team

if __name__ == '__main__':
    end = False
    game = Game()
    my_team_color = None
    msg_count = 0
    while not end:
        input_message = raw_input()
        # check if input message is assigning player a color
        if msg_count > 8:
            sys.stdout.write(my_team_color + " surrenders\n")
            end = True
            sys.exit(0)

        if "you are " in input_message:
            # set color and skip outputting a message if necessary
            if "black" in input_message:
                my_team_color = 'black'
                my_team = game.players[0]
                continue
            else:
                my_team_color = 'white'
                my_team = game.players[1]
                game_rep = game.get_game_state()
                valid_moves = my_team.get_valid_moves(game_rep)
                # move = valid_moves[random.randrange(len(valid_moves))]
                # game.receive_move(generate_move_sentence([my_team_color] + list(move)))
                move = game.receive_move(raw_input())
                # sys.stdout.write(generate_move_sentence([my_team_color] + list(move)))
                game_rep = game.get_game_state()
                # print move
    
        elif "moves" in input_message:
            game.receive_move(input_message)
            game_rep = game.get_game_state()
            valid_moves = my_team.get_valid_moves(game_rep)
            # move = valid_moves[random.randrange(len(valid_moves))]
            # game.receive_move(generate_move_sentence([my_team_color] + list(move)))
            move = game.receive_move(raw_input())
            # sys.stdout.write(generate_move_sentence([my_team_color] + list(move)))
            game_rep = game.get_game_state()
            # print move

        elif "wins" in input_message or "loses" in input_message or "drawn" in input_message:
            end = True
            sys.exit(0)

        elif " offers draw" in input_message:
            sys.stdout.write(my_team_color + " accepts draw\n")
            end = True
            sys.exit(0)

        

        msg_count += 1
        # other_team = game.players[0] if my_team != game.players[0] else game.players[1]
        # print evaluate_game_state(my_team, other_team)
        sys.stdin.flush()
        sys.stdout.flush()