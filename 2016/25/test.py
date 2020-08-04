
candidate = 2538
found = False
while not found:
	b = candidate
	prevval = 1
	signal = ""
	stop = False
	while b != 0 and not stop:
		c = 0
		if b % 2 == 0:
			c = 2
		else:
			c = 1
		b = int(float(b) / 2)
		value = 2 - c
		if (prevval == 0 and value != 1) or (prevval == 1 and value != 0):
			stop = True
		prevval = value
	
	if not stop:
		print candidate - (9 * 282)
		found = True
	
	candidate += 1
	if candidate % 10000 == 0:
		print candidate
#test : 010101111001
#prog : 010101111001