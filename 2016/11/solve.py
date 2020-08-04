from enum import Enum
import random
import copy
import hashlib
import itertools
INFINITE = 500

def md5Hash(plain):
	m = hashlib.md5()
	m.update(plain)
	return m.digest()
	
class Type(Enum):
	GENERATOR="G"
	MICROCHIP="M"

class Element:
	def __init__(self, name, type, floor):
		self.name = name
		self.type = type
		self.floor = floor
	
	def __str__(self):
		return "{} {} {}".format(self.name, self.type, self.floor)

class Building:
	def __init__(self):
		# TRAIN DATA : 
		#self.elements = [
		#	Element("Hydrogen", Type.MICROCHIP, 1),
		#	Element("Lithium", Type.MICROCHIP, 1),
		#	Element("Hydrogen", Type.GENERATOR, 2),
		#	Element("Lithium", Type.GENERATOR, 3)
		#]
		
		# CHALLENGE DATA : 
		self.elements = [
			Element("Polonium", Type.GENERATOR, 1),
			Element("Thulium", Type.GENERATOR, 1),
			Element("Thulium", Type.MICROCHIP, 1),
			Element("Promethium", Type.GENERATOR, 1),
			Element("Ruthenium", Type.GENERATOR, 1),
			Element("Ruthenium", Type.MICROCHIP, 1),
			Element("Cobalt", Type.GENERATOR, 1),
			Element("Cobalt", Type.MICROCHIP, 1),
			Element("Polonium", Type.MICROCHIP, 2),
			Element("Promethium", Type.MICROCHIP, 2)
		]
		self.elevatorPosition = 1
		
	def __str__(self):
		return "".join([str(element) for element in self.elements])
		
	def getElementsAtFloor(self, floor):
		return [element for element in self.elements if element.floor == floor]
	
	def check(self):
		for floorIdx in range(1, 5):
			elements = self.getElementsAtFloor(floorIdx)
			
			microships = []
			for element in elements:
				if element.type is Type.MICROCHIP:
					microships.append(element.name)
			
			generators = {}
			for element in elements:
				if element.type is Type.GENERATOR:
					generators[element.name] = True
			
			if len(generators.keys()) > 0:
				for microship in microships:
					if microship not in generators:
						return False
		return True
		
	def end(self):
		return len(self.getElementsAtFloor(4)) == len(self.elements)
		
	def randomExecution(self, alreadySeen, minSteps, moves, depth):
		if depth == minSteps:
			print "ko"
			return minSteps, moves
	
		valid = False
		move = ""
		building = ""
		cnt = 0
		while cnt < 10 and (not valid or md5Hash(str(building)) in alreadySeen):
			move = ""
			cnt += 1
			building = copy.deepcopy(self)
			direction = bool(random.getrandbits(1))
			if building.elevatorPosition == 1:
				direction = True
			elif building.elevatorPosition == 4:
				direction = False
			
			floorElements = building.getElementsAtFloor(building.elevatorPosition)
			if direction: # UP
				elementsMoved = random.sample(floorElements, min(len(floorElements), random.sample([1, 2], 1)[0]))
				for idx, element in enumerate(elementsMoved):
					move += str(element) + ", "
					elementsMoved[idx].floor += 1
				building.elevatorPosition += 1
				move += " UP !"
			
			else: #DOWN
				elementsMoved = random.sample(floorElements, 1)
				move += str(elementsMoved[0]) + " DOWN !\n"
				elementsMoved[0].floor -= 1
				building.elevatorPosition -= 1
				
			valid = building.check()
		
		if valid:
			alreadySeen2 = copy.deepcopy(alreadySeen)
			alreadySeen2[md5Hash(str(building))] = True
			if not building.end():
				return building.randomExecution(alreadySeen2, minSteps, moves+[move], depth+1)
			else:
				return (depth, moves+[move])
		else:
			return minSteps, moves
			
	def exec1up(self):
		building = copy.deepcopy(self)
		floorElements = building.getElementsAtFloor(building.elevatorPosition)
		random.shuffle(floorElements)
		for element in floorElements:
			element.floor += 1
			if building.check():
				building.elevatorPosition += 1
				return building
			else:
				element.floor -= 1
		return None
		
	def exec2up(self):
		building = copy.deepcopy(self)
		floorElements = list(itertools.combinations(building.getElementsAtFloor(building.elevatorPosition), 2))
		random.shuffle(floorElements)
		for elementA, elementB in floorElements:
			elementA.floor += 1
			elementB.floor += 1
			if building.check():
				building.elevatorPosition += 1
				return building
			else:
				elementA.floor -= 1
				elementB.floor -= 1
		return None
		
	def exec1down(self):
		building = copy.deepcopy(self)
		floorElements = building.getElementsAtFloor(building.elevatorPosition)
		random.shuffle(floorElements)
		for element in floorElements:
			element.floor -= 1
			if building.check():
				building.elevatorPosition -= 1
				return building
			else:
				element.floor += 1
		return None
	
	def randomExecution2(self, minMove):
		cnt = 0
		
		while not self.end() and cnt < minMove:
			functions = []
			if self.elevatorPosition > 1:
				functions.append(self.exec1down)
			if self.elevatorPosition < 4:
				functions.append(self.exec1up)
				functions.append(self.exec2up)
			random.shuffle(functions)
		
			progression = False
			for function in functions:
				newBuilding = function()
				if newBuilding != None:
					self = newBuilding
					progression = True
					continue
			if progression:
				cnt += 1
			else: 
				return INFINITE
		
		return cnt
	
	def bruteforce(self):
		minSteps = INFINITE
		while True:
			steps, moves = self.randomExecution({}, minSteps, [], 1)
			if steps < minSteps:
				minSteps = steps
				print "\n----------------"
				print "new minSteps : {}".format(minSteps)
				print "\n".join(moves)
	
	def bruteforce2(self):
		result = INFINITE
		minresult = INFINITE
		while result != 11:
			minresult = min(result, minresult)
			while True:
				result = self.randomExecution2(result)
				if result < minresult:
					minresult = result
					print "==> {}".format(minresult)
				
if __name__ == "__main__":
	building = Building()
	#building.bruteforce()
	building.bruteforce2()
	
# EXPERIMENTAL MIN
# 79 (not the answer)
# 75 (not the answer)
# 65 (not the answer)


# THEORIC MIN
# 8*(3+3)+2(2+2) = 56



# 213

# [56, 213]