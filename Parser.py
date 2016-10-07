import random
import sys

# usage python Parser.py <number of sentence you want>

class Message_Grammer:
    def __init__(self, file = "message-grammer.txt"):
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


sentence = []




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
    while not end:
        input_message = raw_input()

        # check if input message is assigning player a color
        if "you are " in input_message:
            # set color and skip outputting a message if necessary
            if "black" in input_message:
                grammer.CFG['<player>'] = [('black',)]
                continue
            else:
                grammer.CFG['<player>'] = [('white',)]

        elif "wins" in input_message or "loses" in input_message or "drawn" in input_message:
            sys.exit()

        sys.stdout.write(generate_sentence('<playermsg>', grammer.CFG)+"\n")
        sentence = []
