def getrepetitor(sequence):
	endidx = sequence.find(")", 0, 10)
	rep = sequence[1:endidx]
	repparts = rep.split("x")
	sequencesize = int(repparts[0])
	times = int(repparts[1])
	repetitorsize = endidx + 1
	return (endidx+1, sequencesize, times, repetitorsize)
	
def computeLength(sequence):
	length = 0
	idx = 0
	while idx < len(sequence):
		if sequence[idx] != "(":
			length += 1
			idx += 1
		else:
			start, sequencesize, times, repetitorsize = getrepetitor(sequence[idx:idx+10])
			length += times * computeLength(sequence[idx+start:idx+start+sequencesize])
			idx += repetitorsize + sequencesize
	return length


with open("input.txt", "r") as f:
	lines = f.readlines()
	lines = [line[:-1] for line in lines]
	
	for line in lines:
		print line + " : " + str(computeLength(line))
