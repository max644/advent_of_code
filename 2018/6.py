from collections import defaultdict

charset = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
class Coord:
	def __init__(self, x, y, c="."):
		self.x = x
		self.y = y
		self.c = c
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
			
	def display(self):
		output = ""
		for line_idx in range(0, y_max):
			line = ""
			for col_idx in range(0, x_max):
				line += self.map[line_idx][col_idx].c
			output += line + "\n"
		
		with open("output.txt", "w") as file:
			file.write(output)
			
	def getClosestPoint(self, position):
		distancesPerPoint = sorted([(point, abs(position.x - point.x) + abs(position.y - point.y)) for point in self.points], key = lambda x:x[1])
		if distancesPerPoint[0][1] == distancesPerPoint[1][1]:
			return None
		else:
			return distancesPerPoint[0][0]
		
	def computeClosestPoints(self):
		for line_idx in range(len(self.map)):
			for col_idx in range(len(self.map[line_idx])):
				closestPoint = self.getClosestPoint(self.map[line_idx][col_idx])
				if closestPoint != None:
					self.map[line_idx][col_idx].c = closestPoint.c
				
				
def get_letter(idx):
	return charset[idx]
	
if __name__ == "__main__":
	
	with open("6.txt", "r") as file:
		lines = file.readlines()
	
	lines = [line[:-1] for line in lines]
	
	points = [Coord(int(line.split(',')[0]), int(line.split(',')[1]), get_letter(idx)) for idx, line in enumerate(lines)]
	
	x_max = max([point.x for point in points]) + 2
	y_max = max([point.y for point in points]) + 2
	
	world = World(x_max, y_max, points)
	world.computeClosestPoints()
	world.display()
	
	count = defaultdict(int)
	for line_idx in range(y_max):
		for col_idx in range(x_max):
			carac = world.map[line_idx][col_idx].c
			count[carac] += 1
	
	# 1st and last columns
	for line_idx in range(y_max):
		carac = world.map[line_idx][0].c
		if carac in count:
			del count[carac]
		carac = world.map[line_idx][x_max-1].c
		if carac in count:
			del count[carac]
	
	# 1st and last line
	for col_idx in range(x_max):
		carac = world.map[0][col_idx].c
		if carac in count:
			del count[carac]
		carac = world.map[y_max-1][col_idx].c
		if carac in count:
			del count[carac]
			
	print max(count.values())