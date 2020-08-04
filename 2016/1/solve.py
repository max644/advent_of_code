import math
import copy

NORTH = 0
EST = 1
SOUTH = 2
OUEST = 3

def checkVisited(visited, coordA, coordB, diff):
	while coordA != coordB:
		coordA["x"] += diff["x"]
		coordA["y"] += diff["y"]
		key = str(coordA["x"])+";"+str(coordA["y"])
		if key in visited:
			print coordA
		visited[key] = True
	
with open("input.txt", "r") as f:
	content = f.read()
	instructions = content.split(",")
	instructions = [inst.strip() for inst in instructions]
	
	coord = {
		"x":0,
		"y":0
	}
	direction = NORTH
	visited = {"0;0":True}
	for inst in instructions:
		if (inst[0] == "R"):
			direction += 1
		else:
			direction -= 1
		direction = direction % 4
		
		copy_coord = copy.deepcopy(coord)
		distance = int(inst[1:])
		if direction == NORTH:
			coord["y"] += distance
			checkVisited(visited, copy_coord, coord, {"x":0,"y":1})
		elif direction == EST:
			coord["x"] += distance
			checkVisited(visited, copy_coord, coord, {"x":1,"y":0})
		elif direction == SOUTH:
			coord["y"] -= distance
			checkVisited(visited, copy_coord, coord, {"x":0,"y":-1})
		elif direction == OUEST:
			coord["x"] -= distance
			checkVisited(visited, copy_coord, coord, {"x":-1,"y":0})
		
		
	print math.fabs(coord["x"]) + math.fabs(coord["y"])