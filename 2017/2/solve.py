from itertools import permutations


if __name__ == "__main__":
	lines = []
	with open("input.txt", "r") as file:
		lines = file.readlines()
		
	sum1 = 0
	for line in lines:
		numbers = [int(x) for x in line.split("\t")]
		sum1 += max(numbers) - min(numbers)
	print sum1
	
	sum2 = 0
	for line in lines:
		numbers = [int(x) for x in line.split("\t")]
		for candidateA, candidateB in permutations(numbers, 2):
			division = float(candidateA) / float(candidateB)
			if division % 1 == 0:
				sum2 += int(division)
	print sum2
			