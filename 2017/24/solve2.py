import copy
from random import shuffle
INPUT_FILE = "input.txt"

def searchByPinValue(components, value):
	matchingComponents = []
	for component in components:
		if component[0] == value:
			matchingComponents.append((component, component[1]))
		if component[1] == value:
			matchingComponents.append((component, component[0]))
	return matchingComponents

def scoreBridge(bridge):
	return sum([sum(component) for component in bridge])
	
def buildBridges(components, bridgeBeginning, prevPin, strongestBridge, depth):
	shuffle(components)
	maxLen = len(strongestBridge)
	maxScore = scoreBridge(strongestBridge)
	bridges = [bridgeBeginning]
	if len(searchByPinValue(components, prevPin)) > 0:
		for candidate, nextPin in searchByPinValue(components, prevPin):
			newComponents = copy.deepcopy(components)
			newBridge = copy.deepcopy(bridgeBeginning)
			
			newBridge.append(newComponents.pop(newComponents.index(candidate)))
			
			bridge = buildBridges(newComponents, newBridge, nextPin, strongestBridge, depth+1)
			
			
			score = scoreBridge(bridge)
			if len(bridge) > maxLen or (len(bridge) == maxLen and score > maxScore):
				maxLen = len(bridge)
				maxScore = score
				strongestBridge = bridge
				print "maxlen : {}, maxscore : {}".format(maxLen, maxScore)
		return strongestBridge
	return bridgeBeginning
	
if __name__ == "__main__":
	lines = []
	with open(INPUT_FILE, "r") as file:
		lines = file.readlines()
	
	lines = [line[:-1] for line in lines]
	components = [map(int, line.split("/")) for line in lines]
	
	bridge = buildBridges(components, [], 0, [], 1)

# 35 / 1799