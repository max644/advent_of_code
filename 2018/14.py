PUZZLE_INPUT = 509671

recipesScores = [3, 7]
elf1Position = 0
elf2Position = 1

def printRecipesScores():
	output = ""
	for idx, recipe in enumerate(recipesScores):
		if idx == elf1Position:
			output += "(" + str(recipe) + ")\t"
		elif idx == elf2Position:
			output += "[" + str(recipe) + "]\t"
		else:
			output += str(recipe) + "\t"
	print output
	
def cook():
	global elf1Position
	global elf2Position
	global recipesScores
	newRecipe = recipesScores[elf1Position] + recipesScores[elf2Position]
	if newRecipe >= 10:
		recipesScores.append(newRecipe / 10)
		recipesScores.append(newRecipe % 10)
	else:
		recipesScores.append(newRecipe)
	elf1Position = (elf1Position + recipesScores[elf1Position] + 1) % len(recipesScores)
	elf2Position = (elf2Position + recipesScores[elf2Position] + 1) % len(recipesScores)
	
def after9():
	global elf1Position
	global recipesScores
	position = elf1Position
	return "".join([str(score) for score in recipesScores[PUZZLE_INPUT:PUZZLE_INPUT+10]])
	
printRecipesScores()
while (len(recipesScores)) < PUZZLE_INPUT + 10:
	cook()
	print len(recipesScores)
print "==>" + after9()