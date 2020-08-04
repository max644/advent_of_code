import re
import copy
from enum import Enum
INPUT_FILE = "input.txt"

class Direction(Enum):
	UP="up"
	DOWN="down"
	
class Scanner():
	def __init__(self, layer, depth):
		self.layer = layer
		self.depth = depth
		self.position = 0
		self.direction = Direction.UP
		
	def __str__(self):
		return "layer {} : {}".format(self.layer, self.depth)
		
	def move(self):
		if self.direction is Direction.UP and self.position == self.depth - 1:
			self.direction = Direction.DOWN
		if self.direction is Direction.DOWN and self.position == 0:
			self.direction = Direction.UP
		
		if self.direction is Direction.UP:
			self.position += 1
		if self.direction is Direction.DOWN:
			self.position -= 1
		
def crossFirewall(scanners_input, delay):
	scanners = copy.deepcopy(scanners_input)
	numberOfLayers = max(scanner.layer for _, scanner in scanners.items())
	detections = []
	
	for idx in range(delay):
		for _, scanner in scanners.items():
			scanner.move()
	
	for layer in range(0, numberOfLayers+1):
		if str(layer) in scanners:
			scanner = scanners[str(layer)]
			if scanner.position == 0:
				detections.append((layer, scanner.depth))
		for _, scanner in scanners.items():
			scanner.move()
	return detections
	
if __name__ == "__main__":
	lines = []
	with open(INPUT_FILE, "r") as file:
		lines = file.readlines()
	
	lines = [line[:-1] for line in lines]
	scanners = {}
	for line in lines:
		mo = re.match("(\d+):\s(\d+)", line)
		layer = int(mo.group(1))
		depth = int(mo.group(2))
		scanners[str(layer)] = Scanner(layer, depth)
	
	for _, scanner in scanners.items():
		print scanner
		
	
	detections = crossFirewall(scanners, 0)
	print "==> {}".format(sum(map(lambda detection: detection[0]*detection[1], detections)))
	
	goTrought = False
	delay = -1
	while not goTrought:
		delay += 1
		goTrought = True
		for _, scanner in scanners.items():
			if (delay + scanner.layer) % ((scanner.depth-1) * 2) == 0:
				goTrought = False
				break
	
	print "==> {}".format(delay)