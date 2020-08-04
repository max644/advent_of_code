if __name__ == "__main__":
	with open("5.txt", "r") as file:
		content = file.read()
		
	reaction = True
	startIdx = 0
	while reaction:
		idx = startIdx
		reaction = False
		while reaction == False and idx < len(content) - 1:
			element_a = content[idx] 
			element_b = content[idx+1]
			if abs(ord(element_a) - ord(element_b)) == 0x20:
				content = content[:idx] + content[idx+2:]				
				reaction = True
				startIdx = idx - 1
				if startIdx < 0:
					startIdx = 0
			idx += 1
		print len(content)
	print len(content)
	
	
#9288