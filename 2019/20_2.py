import copy

LETTERS_MAJ = [chr(x) for x in range(0x41, 0x5b)]

class World:
	def __init__(self, grid, levels):
		self.levels = [grid]
		for idx in range(1, levels):
			self.levels.append([[node.copy(idx) for node in line] for line in grid])

class Node:
	def __init__(self, line, col, letter):
		self.line = line
		self.col = col
		self.letter = letter
		self.level = 0
		
		self.isTeleporter = False
		self.teleporterCode = ""
		self.teleporterDirection = 0
		
		self.distance = 0
		
	def copy(self, level):
		ret = Node(self.line, self.col, self.letter)
		ret.level = level
		ret.isTeleporter = self.isTeleporter
		ret.teleporterCode = self.teleporterCode
		ret.teleporterDirection = self.teleporterDirection
		return ret
		
	def __eq__(self, other):
		return self.line == other.line and self.col == other.col and self.level == other.level
	

def getAdjacents(grid, node, fil):
	ret = [
		grid[node.line+1][node.col],
		grid[node.line-1][node.col],
		grid[node.line][node.col+1],
		grid[node.line][node.col-1]
	]
	return list(filter(fil, ret))

def getTeleporterDirection(grid, node):
	if node.line == 0 or node.line == len(grid)-1 or node.col == 0 or node.col == len(grid[0])-1:
		return -1
	return 1

def findTeleporterMap(grid):
	passages = [node for line in grid for node in line if node.letter == "."]
	for passage in passages:
		adjacents = getAdjacents(grid, passage, lambda node : node.letter in LETTERS_MAJ)
		if len(adjacents) > 0:
			firstLetterNode = adjacents[0]
			secondLetter = getAdjacents(grid, firstLetterNode, lambda node : node.letter in LETTERS_MAJ)[0]
			passage.isTeleporter = True
			passage.teleporterDirection = getTeleporterDirection(grid, secondLetter)
			passage.teleporterCode = tuple(sorted([firstLetterNode.letter, secondLetter.letter]))
	
	teleporters = [node for line in grid for node in line if node.isTeleporter]
	ret = {}
	for teleporter in teleporters:
		destinationNode = [node for node in teleporters if node.teleporterCode == teleporter.teleporterCode and node != teleporter]
		if len(destinationNode) > 0:
			ret[(teleporter.line, teleporter.col)] = (destinationNode[0].line, destinationNode[0].col)
	return ret

def findPaths(world, processed, end, teleporterMap):	
	nodeCnt = 1
	
	while nodeCnt > 0:
		newProcessed = []
		nodeCnt = 0
		for node in processed:
			adjacents = getAdjacents(world.levels[node.level], node, lambda n: n.letter == ".")
			if node.isTeleporter:
				newLevelIdx = node.level + node.teleporterDirection
				if newLevelIdx >= 0 and newLevelIdx < len(world.levels):
					destinationCoords = teleporterMap[(node.line, node.col)]
					adjacents.append(world.levels[newLevelIdx][destinationCoords[0]][destinationCoords[1]])
			for adjacent in adjacents:
				if adjacent.distance == 0 and adjacent not in newProcessed:
					adjacent.distance = node.distance + 1
					newProcessed.append(adjacent)
					nodeCnt += 1
		processed = newProcessed
	
with open("20.txt", "r") as file:
	lines = [line[:-1] for line in file.readlines()]

grid = [[Node(lineIdx, colIdx, letter) for colIdx, letter in enumerate(line)] for lineIdx, line in enumerate(lines)]
teleporterMap = findTeleporterMap(grid)

start = [node for line in grid for node in line if node.teleporterCode == ("A", "A")][0]
start.isTeleporter = False

end = [node for line in grid for node in line if node.teleporterCode == ("Z", "Z")][0]
end.isTeleporter = False

world = World(grid, (len(teleporterMap) - 2) // 2) # because start and end aren't teleporter and for every teleporter key, we have an inner and an outer direction
findPaths(world, [start], end, teleporterMap)

print("Step 2 : {}".format(end.distance))