import re

GRID_SIDE = 1000

class Square:
	def __init__(self, line):
		m = re.match(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)", line)
		self.id = int(m.group(1))
		self.from_left = int(m.group(2))
		self.from_top = int(m.group(3))
		self.width = int(m.group(4))
		self.height = int(m.group(5))

if __name__ == "__main__":
	with open("3.txt", "r") as file:
		lines = file.readlines()
		
	lines = [line[:-1] for line in lines]
	
	squares = [Square(line) for line in lines]
	
	grid = [0]*GRID_SIDE
	for line_idx in range(GRID_SIDE):
		grid[line_idx] = []
		for col_idx in range(GRID_SIDE):
			grid[line_idx].append([[], 0])
			
	for square in squares:
		for line_idx in range(square.from_left, square.from_left+square.width):
			for col_idx in range(square.from_top, square.from_top+square.height):
				grid[line_idx][col_idx][0].append(square.id)
				grid[line_idx][col_idx][1] += 1
	
	print sum([1 for line in grid for case in line if case[1] > 1])
	
	ids = {square.id:True for square in squares}
	
	for line_idx in range(len(grid)):
		for col_idx in range(len(grid[line_idx])):
			if grid[line_idx][col_idx][1] > 1:
				for id in grid[line_idx][col_idx][0]:
					ids[id] = False
				
	print filter(lambda x: x[1], ids.iteritems())