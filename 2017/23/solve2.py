import math

b = 106700
c = 123700

notPrimeCnt = 0
for candidate in range(b, c+1, 17):
	prime = True
	for x in range(2, int(math.ceil(math.sqrt(candidate)))):
		if candidate % x == 0:
			prime = False
	
	if not prime:
		notPrimeCnt += 1
		
print "==> {}".format(notPrimeCnt)

#904