SIGLEN = 8

with open("input.txt", "r") as f:
	lines = f.readlines()
	lines = [line[:-1] for line in lines]
	
	csums = [{}, {}, {}, {}, {}, {}, {}, {}]
	for line in lines:
		for cidx in range(SIGLEN):
			c = line[cidx]
			if c not in csums[cidx]:
				csums[cidx][c] = 0
			csums[cidx][c] += 1
	
	signal1 = ""
	signal2 = ""
	for csum in csums:
		cmax = ("", 0)
		cmin = ("", 100)
		for key, value in csum.items():
			if value > cmax[1]:
				cmax = (key, value)
			if value < cmin[1]:
				cmin = (key, value)
		signal1 += cmax[0]
		signal2 += cmin[0]
	
	print signal1
	print signal2