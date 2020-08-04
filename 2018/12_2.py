import copy

PLANT = "#"
NO_PLANT = "."

class Rule:
	def __init__(self, line):
		pattern, result = line.split(" => ")
		self.pattern = [Pot(symbol == PLANT) for symbol in list(pattern)]
		self.result = result == PLANT
		
	def match(self, p):
		return self.pattern == p

class Pot:
	def __init__(self, isPlant, id = -1):
		self.isPlant = isPlant
		self.id = id

	def __str__(self):
		if self.isPlant:
			return PLANT
		return NO_PLANT
		
	def next_generation(self, pattern, rules):
		self.isPlant = False
		for rule in rules:
			if rule.match(pattern):
				self.isPlant = rule.result
		
	def __eq__(self, other):
		if isinstance(other, Pot):
			return self.isPlant == other.isPlant
		return False
		
class Crop:
	def __init__(self, initialStateLine, rules):
		self.pots = [Pot(symbol == PLANT, id) for id, symbol in enumerate(list(initialStateLine.replace("initial state: ", "")))]
		self.rules = rules
		
	def __str__(self):
		return "".join([str(pot) for pot in self.pots])
		
	def getFirstPlantIdx(self):
		for idx, pot in enumerate(self.pots):
			if pot.isPlant:
				return idx
	
	def getLastPlantIdx(self):
		for idx, pot in enumerate(reversed(self.pots)):
			if pot.isPlant:
				return len(self.pots) - idx
	
	def next_generation(self):
		while self.getFirstPlantIdx() < 4:
			self.pots = [Pot(False, self.pots[0].id - 1)] + self.pots
		while self.getLastPlantIdx() > len(self.pots) - 4:
			self.pots = self.pots + [Pot(False, self.pots[-1].id + 1)]
		nextPots = copy.deepcopy(self.pots)
		for idx, pot in enumerate(self.pots[2:-2]):
			nextPots[idx+2].next_generation(self.pots[idx:idx+5], rules)
		self.pots = nextPots
			
def patternRepetition(cropA, cropB):
	potsA = cropA.pots[cropA.getFirstPlantIdx():cropA.getLastPlantIdx()]
	potsB = cropB.pots[cropB.getFirstPlantIdx():cropB.getLastPlantIdx()]
	return potsA == potsB
	
if __name__ == "__main__":
	with open("12.txt", "r") as file:
		lines = file.readlines()
		
	lines = [line[:-1] for line in lines]
	
	initialStateLine = lines[0]
	ruleLines = lines[2:]

	rules = [Rule(line) for line in ruleLines]
	crop = Crop(initialStateLine, rules)
	
	idx = 0
	previous_crop = Crop("", [])
	while not patternRepetition(crop, previous_crop):
		previous_crop = copy.deepcopy(crop)
		crop.next_generation()
		idx += 1
	
	scorePreviousCrop = sum([pot.id for pot in previous_crop.pots if pot.isPlant])
	scoreCrop = sum([pot.id for pot in crop.pots if pot.isPlant])
	
	growth = scoreCrop - scorePreviousCrop
	
	print "===> " + str(scoreCrop + (50000000000 - idx) * growth)