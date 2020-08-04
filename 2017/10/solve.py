INPUT_FILE = "input.txt"
LIST = range(256)

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
	
if __name__ == "__main__":
	content = ""
	with open(INPUT_FILE, "r") as file:
		content = file.read()
	
	lengths = [int(length) for length in content.split(",")]
	
	ll = LIST
	skipSize = 0
	position = 0
	for length in lengths:
		ll, position = loop(ll, position, length, skipSize)
		skipSize += 1
		#print ll, position
	print "==> {}".format(ll[0] * ll[1])
		
		
		
		
		