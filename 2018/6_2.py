from collections import defaultdict

MAX_DISTANCE = 10000

charset = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
class Coord:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.totalDistance = 0
		self.points = []

class World:
	def __init__(self, width, height, points):
		self.map = []
		for line_idx in range(height):
			line = []
			for col_idx in range(width):
				line.append(Coord(col_idx, line_idx))
			self.map.append(line)
		
		for point in points:
			self.map[point.y][point.x] = point
		
		self.points = points
		
	def computeTotalDistances(self):
		for line_idx in range(len(self.map)):
			for col_idx in range(len(self.map[line_idx])):
				position = self.map[line_idx][col_idx]
				distance = sum(abs(position.x - point.x) + abs(position.y - point.y) for point in self.points)
				self.map[line_idx][col_idx].totalDistance = distance
				
	
if __name__ == "__main__":
	
	with open("6.txt", "r") as file:
		lines = file.readlines()
	
	lines = [line[:-1] for line in lines]
	
	points = [Coord(int(line.split(',')[0]), int(line.split(',')[1])) for idx, line in enumerate(lines)]
	
	x_max = max([point.x for point in points]) + 2
	y_max = max([point.y for point in points]) + 2
	
	world = World(x_max, y_max, points)
	world.computeTotalDistances()
				
	# 1st and last columns
	for line_idx in range(y_max):
		if world.map[line_idx][0].totalDistance < MAX_DISTANCE:
			print "test"
		if world.map[line_idx][x_max-1].totalDistance < MAX_DISTANCE:
			print "test"
	
	# 1st and last line
	for col_idx in range(x_max):
		if world.map[0][col_idx].totalDistance < MAX_DISTANCE:
			print "test"
		if world.map[y_max-1][col_idx].totalDistance < MAX_DISTANCE:
			print "test"
				
	zoneSize = sum([1 for line_idx in range(y_max) for col_idx in range(x_max) if world.map[line_idx][col_idx].totalDistance < MAX_DISTANCE])
				
	print zoneSize