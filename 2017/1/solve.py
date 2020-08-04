

if __name__ == "__main__":
	content = ""
	
	with open("input.txt", "r") as file:
		content = file.read()
	
	sum1 = 0
	for idx in range(len(content)):
		curnum = content[idx]
		prevnum = content[idx-1]
		if prevnum == curnum:
			sum1 += int(curnum)
	print sum1
	
	sum2 = 0
	halfsize = len(content)/2
	for idx in range(len(content)):
		curnum = content[idx]
		halfaheadnum = content[(idx+halfsize)%len(content)]
		if halfaheadnum == curnum:
			sum2 += int(curnum)
	print sum2