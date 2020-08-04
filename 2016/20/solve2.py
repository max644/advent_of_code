

rules = []

def removeDuplicate(rules):
	idx = 0
	modifications = False
	while idx < len(rules):
		rule = rules[idx]
		ridx = idx+1
		while ridx < len(rules):
			r = rules[ridx]
			# print "compare", rule, r
			if (r["min"]-1 <= rule["min"] and r["max"]+1 >= rule["min"]) or (r["min"]-1 <= rule["max"] and r["max"]+1 >= rule["max"]) or ((rule["min"] <= r["max"] and rule["max"] >= r["max"])):
				rmin = min(r["min"], rule["min"])
				rmax = max(r["max"], rule["max"])
				rule = {"min":rmin, "max":rmax}
				# print rules[idx], " => ", rule
				rules[idx] = rule
				del rules[ridx]
				modifications = True
			else:
				ridx += 1
		idx += 1
	return modifications

def rulecmp(rule1, rule2):
	return rule1["min"] - rule2["min"]
	
with open("input.txt", "r") as file:
	lines = file.readlines()
	lines = [line[:-1] for line in lines]
	lines = [line.split("-") for line in lines]
	rules = [{"min":int(a), "max":int(b)} for (a, b) in lines]
	
	
	while removeDuplicate(rules):
		print "ok"
	rules.sort(key=lambda rule: rule["min"])
	
	forbbidencnt = 0
	for rule in rules:
		forbbidencnt += (rule["max"] - rule["min"]) + 1
	print str(4294967296 - forbbidencnt)

# 116 is too low
# 234 is too high