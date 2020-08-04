from collections import Counter

if __name__ == "__main__":
	with open("2.txt", "r") as file:
		lines = file.readlines()
	
	lines = [line[:-1] for line in lines]
	
	count2 = 0
	count3 = 0
	for line in lines:
		if len(filter(lambda x: x[1] == 2, Counter(line).items())) > 0:
			count2 += 1
		if len(filter(lambda x: x[1] == 3, Counter(line).items())) > 0:
			count3 += 1
			
	print count2 * count3