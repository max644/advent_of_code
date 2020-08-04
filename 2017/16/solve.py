import re
import copy
import md5
INPUT_FILE = "input.txt"
ITERATIONS = 1000000000

def md5hash(plain):
	m = md5.new()
	m.update(plain)
	return m.digest()

def spin(ll, offset):
	return ll[-offset:] + ll[0:-offset]

def exchange(ll, offset1, offset2):
	pivot = ll[offset1]
	ll[offset1] = ll[offset2]
	ll[offset2] = pivot
	return ll
	
def partner(ll, program1, program2):
	offset1 = ll.index(program1)
	offset2 = ll.index(program2)
	return exchange(ll, offset1, offset2)

def executeInstruction(ll, instruction):
	if instruction.startswith("s"):
		mg = re.search("s(\d+)", instruction)
		ll = spin(ll, int(mg.group(1)))
	elif instruction.startswith("x"):
		mg = re.search("x(\d+)/(\d+)", instruction)
		ll = exchange(ll, int(mg.group(1)), int(mg.group(2)))
	elif instruction.startswith("p"):
		mg = re.search("p([a-p])\/([a-p])", instruction)
		ll = partner(ll, mg.group(1), mg.group(2))
	return ll
	
if __name__ == "__main__":
	content = ""
	with open(INPUT_FILE, "r") as file:
		content = file.read()
	
	instructions = content.split(",")
	
	orig_ll = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p"]
	#orig_ll = ["a", "b", "c", "d", "e"]
	
	ll = copy.deepcopy(orig_ll)
	for instruction in instructions:
		ll = executeInstruction(ll, instruction)
	
	print "==> {}".format("".join(ll))
	
	ll = copy.deepcopy(orig_ll)
	lls = {}
	
	hash = md5hash("".join(ll))
	idx = 0
	while hash not in lls:
		lls[hash] = idx
		for instruction in instructions:
			ll = executeInstruction(ll, instruction)
		hash = md5hash("".join(ll))
		idx += 1
	
	start = lls[hash]
	step = idx - lls[hash]
	remaining = ((ITERATIONS - start) % step)
	
	for idx in range(remaining):
		for instruction in instructions:
			ll = executeInstruction(ll, instruction)
	
	print "==> {}".format("".join(ll))