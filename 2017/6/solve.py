import md5

INPUT_FILE = "input.txt"

def hash(bank):
	m = md5.new()
	m.update(str(bank))
	return m.digest()

def findBiggestBankIndex(banks):
	maxBank = -1
	idxMaxBank = -1
	for idx, bank in enumerate(banks):
		if bank > maxBank:
			maxBank = bank
			idxMaxBank = idx
	return idxMaxBank



if __name__ == "__main__":
	content = ""
	with open(INPUT_FILE, "r") as file:
		content = file.read()
	banks = [int(bank) for bank in content.split("\t")]
	
	previousSituations = {}
	
	cnt = 0
	while hash(banks) not in previousSituations:
		cnt += 1
		biggestBankIndex = findBiggestBankIndex(banks)
		length = banks[biggestBankIndex]
		startIdx = biggestBankIndex + 1
		
		previousSituations[hash(banks)] = cnt
		
		banks[biggestBankIndex] = 0
		for idx in range(length):
			banks[(startIdx+idx)%len(banks)] += 1

		
		
	print "==> {}".format(cnt)
	print "==> {}".format(cnt - previousSituations[hash(banks)] + 1)
	