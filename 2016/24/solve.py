import itertools

NUMBER_OF_POINTS = 8
FILE_INPUT = "input.txt"

# NUMBER_OF_POINTS = 5
# FILE_INPUT = "exemple.txt"

def printBoard(board):
	for y in xrange(len(board)):
		line = ""
		for x in xrange(len(board[y])):
			line += board[y][x]
		print line

def findCoordinates(board, number):
	for y in xrange(len(board)):
		for x in xrange(len(board[y])):
			if board[y][x] == str(number):
				return (x, y)
	return None

	
def findAdjacent(board, coord):
	ret = []
	# y + 1 - DOWN
	if board[coord[1]+1][coord[0]] != "#":
		ret.append((coord[0], coord[1]+1))
	# y - 1 - UP
	if board[coord[1]-1][coord[0]] != "#":
		ret.append((coord[0], coord[1]-1))
	# x + 1 - RIGHT
	if board[coord[1]][coord[0]+1] != "#":
		ret.append((coord[0]+1, coord[1]))
	# x - 1 - LEFT
	if board[coord[1]][coord[0]-1] != "#":
		ret.append((coord[0]-1, coord[1]))
	return ret
	
def dijkstra(board, start, targets):
	ret = {}
	nodes = [{"coord":start, "distance":0}]
	visited = [start]
	while len(nodes) > 0:
		new_nodes = []
		for node in nodes:
			if node["coord"] in targets and node["coord"] not in ret:
				ret[node["coord"]] = node["distance"]
			adjacents = findAdjacent(board, node["coord"])
			for adjacent in adjacents:
				if adjacent not in visited:
					visited.append(adjacent)
					new_nodes.append({"coord":adjacent, "distance":node["distance"]+1})
		nodes = new_nodes
	return ret

with open(FILE_INPUT, "r") as file:
	lines = file.readlines()
	lines = [line[:-1] for line in lines]
	board = []
	for line in lines:
		l = []
		for case in line:
			l.append(case)
		board.append(l)
	
	printBoard(board)
	
	targets = []
	targethash = {}
	for i in range(NUMBER_OF_POINTS):
		coord = findCoordinates(board, i)
		targets.append(coord)
		targethash[coord] = str(i)
	print targets
	
	distances = {}
	for i in range(0, NUMBER_OF_POINTS):
		distances_fromi = dijkstra(board, findCoordinates(board, i), targets)
		print "distance from " + str(i)
		dist = {}
		for coord, distance in distances_fromi.items():
			print targethash[coord] + " => " + str(distance)
			dist[targethash[coord]] = distance
		distances[str(i)] = dist
	
	shortestpath = {"distance" : 100000, "path" : ""}
	for candidate in itertools.permutations("".join([str(i) for i in range(1, NUMBER_OF_POINTS)]), NUMBER_OF_POINTS-1):
		prevpoint = "0"
		totaldist = 0
		for point in candidate:
			totaldist += distances[prevpoint][point]
			prevpoint = point
		if totaldist < shortestpath["distance"]:
			shortestpath["distance"] = totaldist
			shortestpath["path"] = "".join(candidate)
		print candidate, totaldist
	print "shortestpath is " + shortestpath["path"] + "(" + str(shortestpath["distance"]) + ")"