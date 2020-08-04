LETTERS_MAJ = [chr(x) for x in range(0x41, 0x5b)]

class Node:
	def __init__(self, line, col, letter):
		self.line = line
		self.col = col
		self.letter = letter
		
		self.isTeleporter = False
		self.teleporterCode = ""
		self.destination = None
		
		self.distance = 0
		
	def __eq__(self, other):
		return self.line == other.line and self.col == other.col

with open("20.txt", "r") as file:
	lines = [line[:-1] for line in file.readlines()]
	

def getAdjacents(grid, node, fil):
	ret = [
		grid[node.line+1][node.col],
		grid[node.line-1][node.col],
		grid[node.line][node.col+1],
		grid[node.line][node.col-1],
	]
	return list(filter(fil, ret))

def findTeleporters(grid):
	passages = [node for line in grid for node in line if node.letter == "."]
	for passage in passages:
		adjacents = getAdjacents(grid, passage, lambda node : node.letter in LETTERS_MAJ)
		if len(adjacents) > 0:
			firstLetterNode = adjacents[0]
			secondLetter = getAdjacents(grid, firstLetterNode, lambda node : node.letter in LETTERS_MAJ)[0]
			passage.isTeleporter = True
			passage.teleporterCode = tuple(sorted([firstLetterNode.letter, secondLetter.letter]))
	
	teleporters = [node for line in grid for node in line if node.isTeleporter]
	for teleporter in teleporters:
		destinationNode = [node for node in teleporters if node.teleporterCode == teleporter.teleporterCode and node != teleporter]
		if len(destinationNode) > 0:
			teleporter.destination = destinationNode[0]
	
def findPaths(grid, processed, end):
	nodeCnt = 0
	newProcessed = []
	for node in processed:
		adjacents = getAdjacents(grid, node, lambda n: n.letter == ".")
		if node.isTeleporter:
			adjacents.append(node.destination)
		for adjacent in adjacents:
			if adjacent.distance == 0 and adjacent not in newProcessed:
				adjacent.distance = node.distance + 1
				newProcessed.append(adjacent)
				nodeCnt += 1

	if nodeCnt > 0:
		findPaths(grid, newProcessed, end)
	

grid = [[Node(lineIdx, colIdx, letter) for colIdx, letter in enumerate(line)] for lineIdx, line in enumerate(lines)]
findTeleporters(grid)

start = [node for line in grid for node in line if node.teleporterCode == ("A", "A")][0]
start.isTeleporter = False

end = [node for line in grid for node in line if node.teleporterCode == ("Z", "Z")][0]
end.isTeleporter = False

findPaths(grid, [start], end)

print("Step 1 : {}".format(end.distance))