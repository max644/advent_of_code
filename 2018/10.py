import re
import copy

class Point:
	def __init__(self, line):
		m = re.match(r"position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>", line)
		
		self.x = int(m.group(1))
		self.y = int(m.group(2))
		
		self.velX = int(m.group(3))
		self.velY = int(m.group(4))
		
	def move(self, factor = 1):
		self.x += self.velX * factor
		self.y += self.velY * factor

class Sky:
	def __init__(self, lines, width, height):
		self.points = [Point(line) for line in lines]
		self.width = width
		self.height = height
		
	def move(self, factor):
		for point in self.points:
			point.move(factor)
			
	def meanDistance(self):
		distances = []
		for idx, pointA in enumerate(self.points):
			distanceA = 0
			for pointB in self.points[:idx] + self.points[idx+1:]:
				distanceA += abs(pointA.x - pointB.x) + abs(pointA.y - pointB.y)
			distances.append(distanceA)
		return float(sum(distances)) / len(distances)
		
	def getCenter(self):
		center_x = sum([point.x for point in self.points]) / len(self.points)
		center_y = sum([point.y for point in self.points]) / len(self.points)
		return center_x, center_y
		
	def __str__(self):
		center_x, center_y = self.getCenter()
		
		ret = ""
		sky = []
		for lineIdx in range(self.height):
			line = []
			for colIdx in range(self.width):
				line.append(".")
			sky.append(line)
		
		for point in self.points:
			sky[point.y-center_y+self.height/2][point.x-center_x+self.width/2] = "#"
			
		for lineIdx in range(self.height):
			ret += "".join(sky[lineIdx]) + "\n"
		
		return ret
		
def minimumReached(sky):
	skyPrev = copy.deepcopy(sky)
	skyPrev.move(-1)
	skyNext = copy.deepcopy(sky)
	skyNext.move(1) 
	return sky.meanDistance() < skyPrev.meanDistance() and sky.meanDistance() < skyNext.meanDistance()
	
def findMinDistance(sky_orig, step = 10000):
	sky = copy.deepcopy(sky_orig)
	moves = 0
	prev_distance = float("+Inf")
	while not minimumReached(sky):
		sky.move(step)
		moves += step
		if sky.meanDistance() > prev_distance : 
			step = int(-0.5 * step)
		prev_distance = sky.meanDistance()
	return moves

if __name__ == "__main__":
	with open("10.txt", "r") as file:
		lines = file.readlines()
	
	sky = Sky(lines, 62, 62)
	
	waitDuration = findMinDistance(sky)
	sky.move(waitDuration)
	print "After " + str(waitDuration) + " seconds : \n" + str(sky)