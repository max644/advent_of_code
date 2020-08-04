INPUT_FILE = "input.txt"
ITERATIONS = 50000000

if __name__ == "__main__":
	step = -1
	with open(INPUT_FILE, "r") as file:
		step = int(file.read())
	
	offset = 0
	valueAfterZero = 0
	for idx in range(1, ITERATIONS+1):
		offset = ((offset + step) % idx)
		if offset == 0:
			valueAfterZero = idx
		offset += 1
		
	print "==> {}".format(valueAfterZero)