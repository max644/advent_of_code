MIN_LETTERS = [chr(x) for x in range(0x61, 0x7b)]
MAJ_LETTERS = [chr(x) for x in range(0x41, 0x5b)]

class Node:
	def __init__(self, letter, line, col):
		self.line = line
		self.col = col
		self.letter = letter
		
		self.previous = None
		
		self.dependencies = []
		
		self.distances = {}
		
	def __eq__(self, other):
		if other == None:	
			return False
		return self.col == other.col and self.line == other.line
	
	def __hash__(self):
		return hash((self.line, self.col))

class StatePart1:
	def __init__(self, start):
		self.visited = set()
		self.position = start
		self.distance = 0
		
	def clone(self):
		ret = StatePart1(self.position)
		ret.visited = self.visited.copy()
		ret.distance = self.distance
		return ret
		
	def __eq__(self, other):
		if other == None:	
			return False
		return self.position == other.position and self.visited == other.visited
		
	def __hash__(self):
		return hash((self.position, tuple(sorted(list(self.visited))))) # sort because order doesn't matter but we need to have same hash for 2 differents paths

class StatePart2:
	def __init__(self, starts):
		self.visited = set()
		self.positions = starts
		self.distance = 0
		
	def clone(self):
		ret = StatePart2(self.positions.copy())
		ret.visited = self.visited.copy()
		ret.distance = self.distance
		return ret
		
	def __eq__(self, other):
		if other == None:	
			return False
		return self.positions == other.positions and self.visited == other.visited
		
	def __hash__(self):
		return hash((tuple(self.positions), tuple(sorted(list(self.visited))))) # sort because order doesn't matter but we need to have same hash for 2 differents paths
		
def getAdjacentOpenNodes(grid, node):
	ret = []
	if grid[node.line+1][node.col].letter != "#":
		ret.append(grid[node.line+1][node.col])
	if grid[node.line-1][node.col].letter != "#":
		ret.append(grid[node.line-1][node.col])
	if grid[node.line][node.col+1].letter != "#":
		ret.append(grid[node.line][node.col+1])
	if grid[node.line][node.col-1].letter != "#":
		ret.append(grid[node.line][node.col-1])
	return ret

def computePreviousNodes(grid, nodeList1, nodeList2):
	newNodeList = []
	newNodeCnt = 0
	for node in nodeList1:
		adjacents = getAdjacentOpenNodes(grid, node)
		for adjacent in adjacents:
			if adjacent not in nodeList2:
				adjacent.previous = node
				newNodeList.append(adjacent)
				newNodeCnt += 1
	if newNodeCnt > 0:
		computePreviousNodes(grid, newNodeList, nodeList1)
	
def findKeyDependencies(grid, start):
	keyNodes = [node for line in grid for node in line if node.letter in MIN_LETTERS]
	for keyNode in keyNodes:
		curNode = keyNode
		while curNode.letter != "@":
			if curNode.letter in MAJ_LETTERS:
				keyNode.dependencies.insert(0, curNode.letter.lower())
			curNode = curNode.previous
			

def findKeyDistances(grid, targets, nodeList1, nodeList2, depth):
	ret = {}
	newNodeList = []
	newNodeCnt = 0
	for node in nodeList1:
		adjacents = getAdjacentOpenNodes(grid, node)
		for adjacent in adjacents:
			if adjacent not in nodeList2 and adjacent not in newNodeList:
				newNodeList.append(adjacent)
				newNodeCnt += 1
				if adjacent.letter in targets:
					ret[adjacent.letter] = depth
	if newNodeCnt > 0:
		ret.update(findKeyDistances(grid, targets, newNodeList, nodeList1, depth+1))
	return ret
	
def getReachableKeysPart1(state, keyNodes):
	ret = []
	for keyNode in keyNodes:
		if keyNode.letter not in state.visited and all([dependency in state.visited for dependency in keyNode.dependencies]):
			ret.append(keyNode)
	return ret

def tryAllPathsPart1(grid, start, keyNodes):
	allStates = [StatePart1(start)]
	
	for idx in range(len(keyNodes)):
		newAllStates = {}
		for state in allStates:
			for candidate in getReachableKeysPart1(state, keyNodes):
				newState = state.clone()
				newState.visited.add(candidate.letter)
				newState.distance += state.position.distances[candidate.letter]
				newState.position = candidate
				if newState not in newAllStates:
					newAllStates[newState] = newState
				elif newState.distance < newAllStates[newState].distance:
					newAllStates[newState] = newState
		
		print("key {} : {} states".format(idx, len(newAllStates)))
		
		allStates = newAllStates.values()
	
	return min(allStates, key=lambda state : state.distance)

def getReachableKeysPart2(state, keyNodes):
	ret = []
	for keyNode in keyNodes:
		if keyNode.letter not in state.visited and all([dependency in state.visited for dependency in keyNode.dependencies]):
			ret.append(keyNode)
	return ret

def tryAllPathsPart2(grid, starts, keyNodes):
	allStates = [StatePart2(starts)]
	
	for idx in range(len(keyNodes)):
		newAllStates = {}
		for state in allStates:
			for candidate in getReachableKeysPart2(state, keyNodes):
				newState = state.clone()
				positionIdx = [idx for idx, pos in enumerate(newState.positions) if candidate.letter in pos.distances][0]
				newState.visited.add(candidate.letter)
				newState.distance += newState.positions[positionIdx].distances[candidate.letter]
				newState.positions[positionIdx] = candidate
				if newState not in newAllStates:
					newAllStates[newState] = newState
				elif newState.distance < newAllStates[newState].distance:
					newAllStates[newState] = newState
		
		print("key {} : {} states".format(idx, len(newAllStates)))
		
		allStates = newAllStates.values()
	return min(allStates, key=lambda state : state.distance)

def part1():
	with open("18_1.txt", "r") as file:
		content = file.readlines()

	grid = [[Node(letter, lineIdx, colIdx) for colIdx, letter in enumerate(line)] for lineIdx, line in enumerate(content)]
	start = [node for line in grid for node in line if node.letter == "@"][0]
	keyNodes = [node for line in grid for node in line if node.letter in MIN_LETTERS]

	computePreviousNodes(grid, [start], [])
	findKeyDependencies(grid, start)

	start.distances = findKeyDistances(grid, [node.letter for node in keyNodes], [start], [], 1)
	for keyNode in keyNodes:
		keyNode.distances = findKeyDistances(grid, [node.letter for node in keyNodes if node != keyNode], [keyNode], [], 1)

	return tryAllPathsPart1(grid, start, keyNodes).distance

def part2():
	with open("18_2.txt", "r") as file:
		content = file.readlines()
	
	grid = [[Node(letter, lineIdx, colIdx) for colIdx, letter in enumerate(line)] for lineIdx, line in enumerate(content)]
	starts = [node for line in grid for node in line if node.letter == "@"]
	keyNodes = [node for line in grid for node in line if node.letter in MIN_LETTERS]

	for start in starts:
		computePreviousNodes(grid, [start], [])
	for start in starts:
		findKeyDependencies(grid, start)
	for start in starts:
		start.distances = findKeyDistances(grid, [node.letter for node in keyNodes], [start], [], 1)
	for keyNode in keyNodes:
		keyNode.distances = findKeyDistances(grid, [node.letter for node in keyNodes if node != keyNode], [keyNode], [], 1)
	
	return tryAllPathsPart2(grid, starts, keyNodes).distance

print("Step 1 : {}".format(part1()))
print("Step 2 : {}".format(part2()))