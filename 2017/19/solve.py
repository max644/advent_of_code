from enum import Enum
import re

INPUT_FIILE = "input.txt"

# 	(0, 0)	(1, 0)	(2, 0)	(3, 0)
#	(0, 1)	(1, 1)	(2, 1)	(3, 1)
#	(0, 2)	(1, 2)	(2, 2)	(3, 2)
#	(0, 3)	(1, 3)	(2, 3)	(3, 3)

class Direction(Enum):
	SOUTH = 0
	WEST = 1
	NORTH = 2
	EAST = 3

class Packet():
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.direction = Direction.SOUTH
		self.checkPointCrossed = []
		self.reachDestination = False
		self.boxCrossedCount = 1
		
	def move(self, grid):
		inc_x = 0
		inc_y = 0
		directionSymbol = ""
		
		if self.direction == Direction.SOUTH:
			inc_y = 1
			directionSymbol = "|"
		elif self.direction == Direction.WEST:
			inc_x = -1
			directionSymbol = "-"
		elif self.direction == Direction.NORTH:
			inc_y = -1
			directionSymbol = "|"
		elif self.direction == Direction.EAST:
			inc_x = 1
			directionSymbol = "-"	
			
		if not self.inGrid(grid, self.x+inc_x, self.y+inc_y):
			self.reachDestination = True
		else:
			self.boxCrossedCount += 1
			self.y += inc_y
			self.x += inc_x
			boxValue = grid[self.y][self.x]
			if self.isCheckpoint(boxValue):
				self.checkPointCrossed.append(boxValue)
			elif boxValue == "+":
				self.changeDirection(grid)
			elif boxValue == " ":
				self.reachDestination = True
				self.boxCrossedCount -= 1

	def changeDirection(self, grid):
		if self.direction == Direction.SOUTH or self.direction == Direction.NORTH:
			if self.inGrid(grid, self.x+1, self.y) and grid[self.y][self.x+1] != " ":
				self.direction = Direction.EAST
			elif self.inGrid(grid, self.x-1, self.y) and grid[self.y][self.x-1] != " ":
				self.direction = Direction.WEST
		elif self.direction == Direction.EAST or self.direction == Direction.WEST:
			if self.inGrid(grid, self.x, self.y+1) and grid[self.y+1][self.x] != " ":
				self.direction = Direction.SOUTH
			elif self.inGrid(grid, self.x, self.y-1) and grid[self.y-1][self.x] != " ":
				self.direction = Direction.NORTH
	
	def isCheckpoint(self, value):
		return bool(re.search("^[A-Z]$", value))
		
	def inGrid(self, grid, x, y):
		return y >= 0 and y < len(grid) and x >= 0 and x < len(grid[0])
		
def findStartPoint(grid):
	for idx in range(len(grid[0])):
		if grid[0][idx] == "|":
			return Packet(idx, 0)
	return None
	
if __name__ == "__main__":
	lines = []
	with open(INPUT_FIILE, "r") as file:
		lines = file.readlines()
		
	lines = [line[:-1] for line in lines]
	
	grid = [[x for x in list(line)] for line in lines]
	
	packet = findStartPoint(grid)
	
	while not packet.reachDestination:
		packet.move(grid)
	
	print "==> {}".format("".join(packet.checkPointCrossed))
	print "==> {}".format(packet.boxCrossedCount)