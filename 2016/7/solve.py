import re

def findpattern(sequence):
	for idx in range(len(sequence)-3):
		if sequence[idx] == sequence[idx+3] and sequence[idx+1] == sequence[idx+2] and sequence[idx] != sequence[idx+1]:
			return True

def findpattern2(sequence, pattern):
	for idx in range(len(sequence)-2):
		if sequence[idx:idx+3] == pattern:
			return True

def checksequence(ipparts, hypernets):
	for hypernet in hypernets:
		if findpattern(hypernet):
			return False
	for ippart in ipparts:
		if findpattern(ippart):
			return True

def checksequence2(ipparts, hypernets):
	for ippart in ipparts:
		for ippartidx in range(len(ippart)-2):
			if ippart[ippartidx] == ippart[ippartidx+2] and ippart[ippartidx] != ippart[ippartidx+1]:
				for hypernet in hypernets:
					if findpattern2(hypernet, ippart[ippartidx+1]+ippart[ippartidx]+ippart[ippartidx+1]):
						return True
			
with open("input.txt", "r") as f:
	lines = f.readlines()
	lines = [line[:-1] for line in lines]
	
	abbacount = 0
	sslcount = 0
	for line in lines:
		hypernets = re.findall('\[([a-z]*)\]', line)
		for hypernet in hypernets:
			line = line.replace("["+hypernet+"]", ";")
		ipparts = line.split(";")
		if checksequence(ipparts, hypernets):
			abbacount += 1
		if checksequence2(ipparts, hypernets):
			sslcount += 1
			
	print abbacount
	print sslcount