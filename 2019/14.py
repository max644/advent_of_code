import re
import math
from collections import defaultdict

BASIC_INPUT = "ORE"
TARGET_OUTPUT = "FUEL"

class Ingrediant:
    def __init__(self, quantity, name):
        self.name = name
        self.quantity = int(quantity)
        
    def __str__(self):
        return self.name + " (" + str(self.quantity) + ")"

class Reaction:
    def __init__(self, line):
        inputsStr, outputsStr = line.split("=>")
        self.inputs = [Ingrediant(quantity, name) for quantity, name in re.findall("(\d+)\s(\w+)", inputsStr)]
        self.output = Ingrediant(*re.findall("(\d+)\s(\w+)", outputsStr)[0])
        self.index = 0
    
    def __str__(self):
        return "[" + str(self.index) + "] " + str([str(input) for input in self.inputs]) + " => " + str(self.output)

def orderReactions(reaction, depth):
    nextReactions = []
    reaction.index = max(reaction.index, depth)
    for ingrediant in reaction.inputs:
        if ingrediant.name != BASIC_INPUT:
            orderReactions(reactionsByOutput[ingrediant.name], depth + 1)
   
def howManyBasicForXTarget(nbTarget):
    stock = defaultdict(int)
    stock[TARGET_OUTPUT] = nbTarget
    for index in range(min([reaction.index for reaction in reactions]), max([reaction.index for reaction in reactions]) + 1):
        for reaction in reactionsByIndex[index]:
            outputQuantity = stock[reaction.output.name]
            stock[reaction.output.name] = 0
            reactionNeeded = math.ceil(outputQuantity / reaction.output.quantity)
            for input in reaction.inputs:
                stock[input.name] += reactionNeeded * input.quantity
    return stock[BASIC_INPUT]

def dicotomy(fct, min, max, target):
    while abs(min - max) > 1:
        pivot = (min + max) // 2
        res = fct(pivot)
        if res > target:
            max = pivot
        elif res < target:
            min = pivot
    return min                              
            
with open("14.txt", "r") as file:
    reactions = [Reaction(line.strip()) for line in file.readlines()]
    
reactionsByOutput = {reaction.output.name: reaction for reaction in reactions}

orderReactions(reactionsByOutput[TARGET_OUTPUT], 1)

reactionsByIndex = defaultdict(list)
for reaction in reactions:
    reactionsByIndex[reaction.index].append(reaction)

print("Step 1 : %d" % howManyBasicForXTarget(1))
print("Step 2 : %d" % dicotomy(howManyBasicForXTarget, 1, 1000000000000, 1000000000000))