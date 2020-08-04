def decrypt(cipher, key):
	plain = ""
	for c in cipher:
		plain += chr((((ord(c) - 0x61) + key) % 26) + 0x61)
	return plain

def checksumCharSort(x, y):
	ret = 0
	c1, count1 = x
	c2, count2 = y
	if count1 != count2:
		ret = count2 - count1
	else:
		ret = ord(c1) - ord(c2)
	return ret
	
def computeChecksum(plain):
	ret = ""
	csum = {}
	for c in plain:
		if c not in csum:
			csum[c] = 0
		csum[c] += 1
	
	counts = []
	for c, sum in csum.items():
		counts.append((c, sum))
	counts = sorted(counts, cmp=checksumCharSort)
	for c in range(0, min(len(counts), 5)):
		ret += counts[c][0]
	return ret
		
with open("input.txt", "r") as f:
	lines = f.readlines()
	lines = [line[:-1] for line in lines]
	
	sectoridsum = 0
	for line in lines:
		dashindex = line.rfind('-')
		head = line[0:dashindex]
		head = head.replace("-", "")
		tail = line[dashindex+1:]
		parts = tail.split("[")
		sectorid = int(parts[0])
		checksum = parts[1][:-1]
		if checksum == computeChecksum(head):
			sectoridsum += sectorid
		if "northpole" in decrypt(head, sectorid):
			print head + " ==> " + decrypt(head, sectorid) + "(" + str(sectorid) + ")"
	print sectoridsum