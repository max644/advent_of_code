import md5
from collections import Counter

INPUT_FILE = "input.txt"

#  ##.#.#..   11010100 D4
#  .#.#.#.#   01010101 55
#  ....#.#.   00001010 0A
#  #.#.##.#   10101101 AD
#  .##.#...   01101000 68
#  ##..#..#   11001001 C9
#  .#...#..   01000100 44
#  ##.#.##.	  11010110 D6

def md5hash(plain):
	m = md5.new()
	m.update(plain)
	return m.digest()

def reversePartOfList(ll, position, length):
	for idx in range(length/2):
		idx1 = (position + idx) % len(ll)
		idx2 = (position + length - idx - 1) % len(ll)
		pivot = ll[idx1]
		ll[idx1] = ll[idx2]
		ll[idx2] = pivot

def loop(ll, position, length, skipSize):
	reversePartOfList(ll, position, length)
	
	position = (position + length + skipSize) % len(ll)
	
	return ll, position
	
def hexlify(number):
	toReturn = hex(number)[2:]
	if len(toReturn) == 1:
		toReturn = "0" + toReturn
	return toReturn
	
def knotHash(lengths):
	ll = range(256)
	skipSize = 0
	position = 0
	for _ in range(64):
		for length in lengths:
			ll, position = loop(ll, position, length, skipSize)
			skipSize += 1

	hash = ""
	for idx1 in range(16):
		bucket = []
		for idx2 in range(16):
			bucket.append(ll[idx1*16 + idx2])
		hash += hexlify(reduce(lambda a, b : a ^ b, bucket, 0))
	return hash
	
def toBin(hexStr):
	bins = [bin(int(x, 16))[2:] for x in hexStr]
	for idx in range(len(bins)):
		while len(bins[idx]) != 4:
			bins[idx] = "0" + bins[idx]
	return "".join(bins)


def getGroup(grid, lineIdx, colIdx, group):
	if grid[lineIdx][colIdx] == 1 and (lineIdx, colIdx) not in group:
		group.append((lineIdx, colIdx))
		if lineIdx < len(grid[0])-1:
			group = getGroup(grid, lineIdx+1, colIdx, group)
		if lineIdx > 0:
			group = getGroup(grid, lineIdx-1, colIdx, group)
		if colIdx < len(grid)-1:
			group = getGroup(grid, lineIdx, colIdx+1, group)
		if colIdx > 0:
			group = getGroup(grid, lineIdx, colIdx-1, group)
	return sorted(group)
	
if __name__ == "__main__":
	content = ""
	with open(INPUT_FILE, "r") as file:
		content = file.read()
		
	gridBinStr = ""
	grid = []
	for idx in range(0, 128):
		lengths = [ord(carac) for carac in list(content+"-"+str(idx))] + [17, 31, 73, 47, 23]
		binStr = toBin(knotHash(lengths))
		grid.append(map(lambda x: int(x), list(binStr)))
	
	grid = grid
	print "==> {}".format(sum([line.count(1) for line in grid]))
	
	groups = {}
	for lineIdx, line in enumerate(grid):
		for colIdx, element in enumerate(line):
			group = getGroup(grid, lineIdx, colIdx, [])
			if len(group) > 0:
				groupHash = md5hash(str(group))
				if groupHash not in groups:
					groups[groupHash] = True
	
	print "==> {}".format(len(groups.keys()))
	
	
	
	
	
	