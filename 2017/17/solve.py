INPUT_FILE = "input.txt"
ITERATIONS = 2017

if __name__ == "__main__":
	step = -1
	with open(INPUT_FILE, "r") as file:
		step = int(file.read())
	
	ll = [0]
	offset = 0
	for idx in range(1, ITERATIONS+1):
		offset = ((offset + step) % len(ll)) + 1
		ll = ll[0:offset] + [idx] + ll[offset:]
		
	print "==> {}".format(ll[(ll.index(2017)+1)%len(ll)])