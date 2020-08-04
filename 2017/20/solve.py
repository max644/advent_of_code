import re
import copy

INPUT_FILE = "input.txt"
ITERATIONS = 100

class Particule:
	def __init__(self, line, idx):
		mg = re.search("p=<(-?\d+),(-?\d+),(-?\d+)>, v=<(-?\d+),(-?\d+),(-?\d+)>, a=<(-?\d+),(-?\d+),(-?\d+)>", line)
		self.pos_x = int(mg.group(1))
		self.pos_y = int(mg.group(2))
		self.pos_z = int(mg.group(3))
		
		self.vel_x = int(mg.group(4))
		self.vel_y = int(mg.group(5))
		self.vel_z = int(mg.group(6))
		
		self.acc_x = int(mg.group(7))
		self.acc_y = int(mg.group(8))
		self.acc_z = int(mg.group(9))
		
		self.idx = idx
		
		self.collision = False
		
	def __eq__(self, other):
		return self.pos_x == other.pos_x and self.pos_y == other.pos_y and self.pos_z == other.pos_z
	
	def getAccelerationScore(self):
		return abs(particule.acc_x) + abs(particule.acc_y) + abs(particule.acc_z)
		
	def getVelocityScore(self):
		return abs(particule.vel_x) + abs(particule.vel_y) + abs(particule.vel_z)

	def getPositionScore(self):
		return abs(particule.pos_x) + abs(particule.pos_y) + abs(particule.pos_z)
		
	def move(self):
		self.vel_x += self.acc_x
		self.vel_y += self.acc_y
		self.vel_z += self.acc_z
	
		self.pos_x += self.vel_x
		self.pos_y += self.vel_y
		self.pos_z += self.vel_z
	
if __name__ == "__main__":
	lines = []
	with open(INPUT_FILE, "r") as file:
		lines = file.readlines()
	
	orig_particules = []
	for idx, line in enumerate(lines):
		orig_particules.append(Particule(line, idx))
		
	particules = copy.deepcopy(orig_particules)
	
	accelerationScores = [particule.getAccelerationScore() for particule in particules]
	particules = [particule for particule in particules if particule.getAccelerationScore() == min(accelerationScores)]
	
	velocityScores = [particule.getVelocityScore() for particule in particules]
	particules = [particule for particule in particules if particule.getVelocityScore() == min(velocityScores)]
	
	positionScores = [particule.getPositionScore() for particule in particules]
	particules = [particule for particule in particules if particule.getPositionScore() == min(positionScores)]
	
	print "==> {}".format(particules[0].idx)
	
	particules = copy.deepcopy(orig_particules)
	
	for iterIdx in range(ITERATIONS):
		for particule in particules:
			particule.move()
		for idx1, particule1 in enumerate(particules):
			for idx2, particule2 in enumerate(particules[idx1+1:]):
				if particule1 == particule2:
					particule1.collision = True
					particule2.collision = True
		particules = [particule for particule in particules if not particule.collision]
		print "==> {}".format(len(particules))