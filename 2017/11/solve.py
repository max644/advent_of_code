from enum import Enum
import math
INPUT_FILE = "input.txt"

class Direction(Enum):
	NORTH = "north"
	NORTH_EAST = "north east"
	SOUTH_EAST = "south east"
	SOUTH = "south"
	SOUTH_OUEST = "south ouest"
	NORTH_OUEST = "north ouest"

class Coordinate():
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def move(self, direction):
		if direction is Direction.NORTH:
			self.y += 2
		elif direction is Direction.NORTH_EAST:
			self.y += 1
			self.x += 1
		elif direction is Direction.SOUTH_EAST:
			self.y -= 1
			self.x += 1
		elif direction is Direction.SOUTH:
			self.y -= 2
		elif direction is Direction.SOUTH_OUEST:
			self.y -= 1
			self.x -= 1
		elif direction is Direction.NORTH_OUEST:
			self.y += 1
			self.x -= 1
	
	def distanceFromOrigine(self):
		distance = abs(self.x)
		if abs(self.y) > abs(self.x):
			distance += (abs(self.y) - abs(self.x))/2 
		return distance
	
	def __str__(self):
		return "({}; {})".format(self.x, self.y)
	
def strToDirection(value):
	if value == "n":
		return Direction.NORTH
	if value == "ne":
		return Direction.NORTH_EAST
	if value == "se":
		return Direction.SOUTH_EAST
	if value == "s":
		return Direction.SOUTH
	if value == "sw":
		return Direction.SOUTH_OUEST
	if value == "nw":
		return Direction.NORTH_OUEST
	

if __name__ == "__main__":
	content = ""
	with open(INPUT_FILE, "r") as file:
		content = file.read()

	directions = [strToDirection(direction) for direction in content.split(",")]
	
	coord = Coordinate(0, 0)
	maxDistanceFromOrigine = 0
	for direction in directions:
		coord.move(direction)
		maxDistanceFromOrigine = max(maxDistanceFromOrigine, coord.distanceFromOrigine())
	
	print "==> {}".format(coord.distanceFromOrigine())
	print "==> {}".format(maxDistanceFromOrigine)
	
	
	
	
	
	
	
	
	
	
	
	
	