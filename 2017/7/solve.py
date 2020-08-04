import re

INPUT_FILE = "input.txt"

class Program:
	programs = {}
	
	def __init__(self, name, weight, children):
		self.name = name
		self.weight = weight
		self.children = children
	
	def __str__(self):
		return "{} ({}) -> {}".format(self.name, self.weight, ", ".join(self.children))

def allListItemsEquals(list):
	for item in list[1:]:
		if item != list[0]:
			return False
	return True
	
def conrolWeight(rootName):
		program = Program.programs[rootName]
		totalWeight = program.weight
		childWeights = []
		for child in program.children:
			childWeights.append(conrolWeight(child))
		if not allListItemsEquals(childWeights):
			print "==> {} children : {}".format(rootName, zip(program.children, childWeights))
		totalWeight += sum(childWeights)
		return totalWeight
		
def parse(line):
	name = ""
	weight = 0
	children = []
	pattern = re.compile('([a-z]+)\s\((\d+)\)(\s->\s)?([a-z,\s]+)?')
	
	match = pattern.match(line)
	
	name = match.group(1)
	weight = int(match.group(2))
	if match.group(4) != None:
		children = match.group(4).split(",")
	children = [child.strip() for child in children]
	
	return name, weight, children
	
if __name__ == "__main__":
	lines = []
	with open(INPUT_FILE, "r") as file:
		lines = file.readlines()
		
	lines = [line[:-1] for line in lines]
	for line in lines:
		name, weight, children = parse(line)
		Program.programs[name] = Program(name, weight, children)

	isChildrenOfAnotherProgram = {}
	for _, program in Program.programs.items():
		for child in program.children:
			isChildrenOfAnotherProgram[child] = True
	
	for _, program in Program.programs.items():
		if program.name not in isChildrenOfAnotherProgram:
			print "==> {}".format(program.name)
			
	print conrolWeight("vvsvez")