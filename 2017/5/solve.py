import copy

if __name__ == "__main__":
	lines = []
	with open("input.txt", "r") as file:
		lines = file.readlines()
		
	lines1 = [int(line[:-1]) for line in lines]
	lines2 = copy.deepcopy(lines1)
	
	position = 0
	cnt = 0
	while position >= 0 and position < len(lines1):
		jump = lines1[position]
		lines1[position] += 1
		position = position + jump
		cnt += 1
		
	print "{}".format(cnt)
	
	position = 0
	cnt = 0
	while position >= 0 and position < len(lines2):
		jump = lines2[position]
		if lines2[position] >= 3:
			lines2[position] -= 1
		else:
			lines2[position] += 1
		position = position + jump
		cnt += 1
		
	print "{}".format(cnt)