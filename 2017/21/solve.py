INPUT_FILE = "input.txt"
PART_1_ITERATIONS = 5
PART_2_ITERATIONS = 18

class Rule:
	def __init__(self, idx, inputPattern, outputPattern):
		self.idx = idx
		self.inputPattern = inputPattern
		self.outputPattern = outputPattern
		self.dimention = len(self.inputPattern)
		
	def __str__(self):
		return "Rule {} :\ninput pattern : {}\noutput pattern : {}\n".format(self.idx, self.inputPattern, self.outputPattern)
		
	def match(self, pattern):
		return pattern == self.inputPattern
		
	@staticmethod
	def findMatchingRule(pattern):
		for rule in rules:
			if rule.match(pattern):
				return rule
		return None
		
	@staticmethod
	def buildRules(lines):
		rules = []
		idx = 1
		for line in lines:
			inputPatternLine, outputPatternLine = line.split(" => ")
			inputPattern = [list(part) for part in inputPatternLine.split("/")]
			outputPattern = [list(part) for part in outputPatternLine.split("/")]

			versions = Rule.getPatterVersions(inputPattern)
			
			for version in versions:
				rules.append(Rule(idx, version, outputPattern))
				idx += 1
				
		return rules
			
	@staticmethod
	def getRotationVerions(pattern):
		versions = [pattern]
		for versionIdx in range(3):
			versions.append([[line[-idx-1] for line in versions[versionIdx]] for idx in range(len(pattern))])
		return versions
		
	@staticmethod
	def getPatterVersions(pattern):
		#Rotations
		versions = Rule.getRotationVerions(pattern)

		if len(pattern) == 3: #(c rotation for 2 dimentions matrix)			
			#Horizontal flip
			flippedPattern = [pattern[-idx-1] for idx in range(len(pattern))]
			versions = versions + Rule.getRotationVerions(flippedPattern)
			
			#Vertical flip
			flippedPattern = [[pattern[rowIdx][-colIdx-1] for colIdx in range(len(pattern[0]))] for rowIdx in range(len(pattern))]
			versions = versions + Rule.getRotationVerions(flippedPattern)
		
		return versions
	
def printPattern(pattern):
	output = ""
	for line in pattern : 
		output += "".join(line) + "\n"
	print output

def splitPattern(pattern):
	patternParts = []
	if len(pattern) % 2 == 0:
		for rowIdx in range(0, len(pattern), 2):
			patternPartsRow = []
			for colIdx in range(0, len(pattern[0]), 2):
				patternPartsRow.append([
					[pattern[rowIdx][colIdx], pattern[rowIdx][colIdx+1]],
					[pattern[rowIdx+1][colIdx], pattern[rowIdx+1][colIdx+1]]
				])
			patternParts.append(patternPartsRow)
	else:
		for rowIdx in range(0, len(pattern), 3):
			patternPartsRow = []
			for colIdx in range(0, len(pattern[0]), 3):
				patternPartsRow.append([
					[pattern[rowIdx][colIdx], pattern[rowIdx][colIdx+1], pattern[rowIdx][colIdx+2]],
					[pattern[rowIdx+1][colIdx], pattern[rowIdx+1][colIdx+1], pattern[rowIdx+1][colIdx+2]],
					[pattern[rowIdx+2][colIdx], pattern[rowIdx+2][colIdx+1], pattern[rowIdx+2][colIdx+2]]
				])
			patternParts.append(patternPartsRow)
	return patternParts
	
def joinPatternParts(patternParts):
	pattern = []
	dimention = len(patternParts) * len(patternParts[0][0])
	partDimention = len(patternParts[0][0])
	for rowIdx in range(dimention):
		pattern.append([])
		for colIdx in range(dimention):
			pattern[rowIdx].append(patternParts[rowIdx/partDimention][colIdx/partDimention][rowIdx%partDimention][colIdx%partDimention])
	return pattern

if __name__ == "__main__":
	lines = []
	with open(INPUT_FILE, "r") as file:
		lines = file.readlines()

	lines = [line[:-1] for line in lines]
		
	rules = Rule.buildRules(lines)
	
	#for rule in rules:
	#	print rule
	
	pattern = [
		[".", "#", "."],
		[".", ".", "#"],
		["#", "#", "#"]
	]
	
	#printPattern(pattern)
	for idx in range(PART_2_ITERATIONS):
		patternParts = splitPattern(pattern)
		for rowIdx, patternPartRow in enumerate(patternParts):
			for colIdx, patternPart in enumerate(patternPartRow):
				rule = Rule.findMatchingRule(patternPart)
				patternParts[rowIdx][colIdx] = rule.outputPattern
		pattern = joinPatternParts(patternParts)
		#printPattern(pattern)
		
		if idx == PART_1_ITERATIONS:
			print "==> {}".format(sum([line.count("#") for line in pattern]))
	
	print "==> {}".format(sum([line.count("#") for line in pattern]))