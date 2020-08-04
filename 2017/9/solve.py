from collections import Counter

INPUT_FILE = "input.txt"

#{{<a!>},{<a!>},{<a!>},{<ab>}}
def symplifyExpression(expression):
	deletedCount = 0
	idx = 0
	garbageMode = False
	garbageStartAtIndex = -1
	while idx < len(expression):
		carac = expression[idx]
		if carac == "{" or carac == "}" or carac == ",":
			if garbageMode:
				expression = expression[:idx] + expression[idx+1:]
				deletedCount += 1
			else:
				idx += 1
		elif carac == "<":
			if garbageMode:
				expression = expression[:idx] + expression[idx+1:]
				deletedCount += 1
			else:
				garbageMode = True
				garbageStartAtIndex = idx
				idx += 1
		elif carac == ">":
			if garbageMode:
				garbageMode = False
				expression = expression[:garbageStartAtIndex] + expression[idx+1:]
				deletedCount += idx - garbageStartAtIndex - 1
			else:
				expression = expression[:idx] + expression[idx+1:]
				deletedCount += 1
		elif carac == "!":
			expression = expression[:idx] + expression[idx+2:]
		else:
			expression = expression[:idx] + expression[idx+1:]
			deletedCount += 1
	return expression, deletedCount

def countGroups(expression):
	cnt = 0
	openGroups = 0
	for carac in expression:
		if carac == "{":
			openGroups += 1
		if carac == "}":
			if openGroups > 0:
				cnt += openGroups
				openGroups -= 1
			else:
				print "test"
	return cnt

if __name__ == "__main__":
	expression = ""
	with open(INPUT_FILE, "r") as file:
		expression = file.read()
		
	expression, deletedCount = symplifyExpression(expression)
	groupCount = countGroups(expression)
	print "==> {}".format(groupCount)
	print "==> {}".format(deletedCount)
	