from collections import Counter

if __name__ == "__main__":
	with open("5.txt", "r") as file:
		orig_content = file.read()
	
	sizeByLetter = []
	for letter in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o" ,"p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]:
		print letter
		reaction = True
		startIdx = 0
		content = orig_content.replace(letter, "").replace(letter.upper(), "")
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
		sizeByLetter.append((letter, len(content)))
	print sorted(sizeByLetter, key=lambda x:x[1])