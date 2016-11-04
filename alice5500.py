#!/usr/bin/env python

import random
import sys
import json

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


if __name__ == '__main__':
    end = False
    grammer = Message_Grammer()
    my_team = None
    game = Game()

    while not end:
        input_message = raw_input()
        # check if input message is assigning player a color
        if "you are " in input_message:
            # set color and skip outputting a message if necessary
            if "black" in input_message:
                grammer.CFG['<player>'] = [('black',)]
                my_team = game.players[0]
                continue
            else:
                grammer.CFG['<player>'] = [('white',)]
                my_team = game.players[1]

        elif "moves" in input_message:

            game.receive_move(input_message)

        elif "wins" in input_message or "loses" in input_message or "drawn" in input_message:
            end = True
            sys.exit(0)

        game_rep = game.get_game_state()

        # Get all valid moves for my team
        valid_moves = my_team.get_valid_moves(game_rep)

        sys.stdout.write(generate_sentence('<playermsg>', grammer.CFG) + "\n")
        sentence = []
        sys.stdin.flush()
        sys.stdout.flush()