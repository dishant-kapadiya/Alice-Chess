import random
import sys

# usage python Parser.py <number of sentence you want>

lines = [line.rstrip('\n').split("~~~") for line in open("message-grammer.txt")]
lines[-1][-1] = '\n'


CFG = dict()

for line in lines:
    if not line[0] == "":
        if line[0] not in CFG.keys():
            CFG[line[0]] = list()
        # if line[0] == '<message>':
        #     abc = [tuple(temp.split("~")) for temp in line[1:]]
        #     print abc
        xyz = []
        for temp in line[1:]:
            a = tuple(temp.split("~"))
            CFG[line[0]].append(a)


sentence = []

def generate(symbol):
    if symbol not in CFG.keys():
        sentence.append(symbol)
        return

    for transitional_element in CFG[symbol][random.randrange(0,len(CFG[symbol]))]:
        generate(transitional_element)

    return "".join(sentence)



CFG['<player>'] = [('black',)]
for i in range(int(sys.argv[1])):
    print generate('<playermsg>')
    sentence = []
