from enum import Enum

INPUT_FILE = "input.txt"

class Direction(Enum):
	UP = 0
	RIGHT = 1
	DOWN = 2
	LEFT = 3

class Virus:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.direction = Direction.UP
		
	def move(self, grid):
		position = str((self.x, self.y))
		
		#infected
		if position in grid:
			grid.pop(position, None)
			self.direction = Direction((self.direction.value + 1) % 4)
			infection = False
			
		#not infected
		else:
			grid[position] = True
			self.direction = Direction((self.direction.value - 1) % 4)
			infection = True

		if self.direction == Direction.UP:
			self.y -= 1
		if self.direction == Direction.RIGHT:
			self.x += 1
		if self.direction == Direction.DOWN:
			self.y += 1
		if self.direction == Direction.LEFT:
			self.x -= 1
		
		return infection
		
if __name__ == "__main__":
	lines = []
	with open(INPUT_FILE, "r") as file:
		lines = file.readlines()
	
	lines = [line[:-1] for line in lines]
	
	iterations = int(lines.pop(0))
	
	gridArr = [[box=="#" for box in line] for line in lines]
	
	center_y, center_x = (len(gridArr) / 2, len(gridArr[1]) / 2)
	
	grid = {}
	for rowidx, row in enumerate(gridArr):
		for colidx, box in enumerate(row):
			if box:
				grid[str((colidx - center_x, rowidx - center_y))] = True
	
	virus = Virus()
	infectionCnt = 0
	for i in range(iterations):
		if virus.move(grid):
			infectionCnt += 1
			
	print "==> {}".format(infectionCnt)
	