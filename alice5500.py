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

# class for grammer to generate player messages
# self.CFG is a dictionary which stores values based on the Non-Terminal head of grammer
# the corresponding value is list of tuples. Each tuples describes a combination of Terminal
# and Non-Terminal which can be used to generate a valid statement.
class Message_Grammer:
    def __init__(self, file="message-grammer"):
        self.__grammer_file = file
        self.CFG = dict()
        lines = [line.rstrip('\n').split("~~~") for line in open(self.__grammer_file)]
        lines[-1][-1] = '\n'

        for line in lines:
            if not line[0] == "":
                if line[0] not in self.CFG.keys():
                    self.CFG[line[0]] = list()
                for temp in line[1:]:
                    a = tuple(temp.split("~"))
                    self.CFG[line[0]].append(a)

#global variable for generated sentance
sentence = []

# function to generate a valid sentence based on the given grammer
# creates a tree from the start symbol and explores it until no Non-Terminal is found in the sentance
def generate_sentence(symbol, CFG):
    if symbol not in CFG.keys():
        sentence.append(symbol)
        return

    for transitional_element in CFG[symbol][random.randrange(0, len(CFG[symbol]))]:
        generate_sentence(transitional_element, CFG)

    return "".join(sentence)

def generate_move_sentence(param):
    return "{0} moves {1} from {2} {3} to {4}\n".format(param[0], param[1], str(param[2]), param[3], param[4])


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
    grammer = Message_Grammer()
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
                move = valid_moves[random.randrange(len(valid_moves))]
                game.receive_move(generate_move_sentence([my_team_color] + list(move)))
                sys.stdout.write(generate_move_sentence([my_team_color] + list(move)))
	
        elif "moves" in input_message:
            game.receive_move(input_message)
            game_rep = game.get_game_state()
            valid_moves = my_team.get_valid_moves(game_rep)
            move = valid_moves[random.randrange(len(valid_moves))]
            game.receive_move(generate_move_sentence([my_team_color] + list(move)))
            sys.stdout.write(generate_move_sentence([my_team_color] + list(move)))

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
