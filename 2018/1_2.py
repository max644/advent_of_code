if __name__ == "__main__":
	with open("1.txt", "r") as file:
		lines = file.readlines()
		
	lines = [line[:-1] for line in lines]
	
	results = {}
	
	idx = 0
	result = 0
	while result not in results:
		results[result] = True
		line = lines[idx]
		result = result + int(line)
		idx = (idx + 1) % len(lines)
		
	print result