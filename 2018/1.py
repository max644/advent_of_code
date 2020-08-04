if __name__ == "__main__":
	with open("1.txt", "r") as file:
		lines = file.readlines()
		
	lines = [line[:-1] for line in lines]
	
	print sum([int(line) for line in lines])