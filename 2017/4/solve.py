from collections import Counter

if __name__ == "__main__":
	lines = []
	with open("input.txt", "r") as file:
		lines = file.readlines()
	
	lines = [line[:-1] for line in lines]
	
	validCount = 0
	for line in lines:
		valid = True
		words = line.split(" ")
		counter = Counter(words)
		for _, count in counter.items():
			if count > 1:
				valid = False
		if valid:
			validCount += 1
	print validCount
	
	validCount = 0
	for line in lines:
		valid = True
		words = line.split(" ")
		for idx, word1 in enumerate(words):
			for word2 in words[(idx+1):]:
				if Counter(list(word1)) == Counter(list(word2)):
					valid = False
		if valid:
			validCount += 1
			
	print validCount