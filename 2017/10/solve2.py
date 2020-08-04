import binascii

INPUT_FILE = "input.txt"
LIST = range(256)
NUMBER_OF_HASH = 64

#[0]1 2 3 4 
# 2 1 0[3]4
# 4 3 0[1]2
# 4[3]0 1 2
# 3 4 2 1[0]
#
#

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

if __name__ == "__main__":
	content = ""
	with open(INPUT_FILE, "r") as file:
		content = file.read()
	lengths = [ord(carac) for carac in list(content)] + [17, 31, 73, 47, 23]
	
	ll = LIST
	skipSize = 0
	position = 0
	for _ in range(NUMBER_OF_HASH):
		for length in lengths:
			ll, position = loop(ll, position, length, skipSize)
			skipSize += 1

	hash = ""
	for idx1 in range(16):
		bucket = []
		for idx2 in range(16):
			bucket.append(ll[idx1*16 + idx2])
		hash += hexlify(reduce(lambda a, b : a ^ b, bucket, 0))
	print hash
		
		