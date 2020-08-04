from itertools import combinations

def one_caracter_differ(str1, str2):
	differ = 0
	str_without_caracter_differ = ""
	for caracter in zip(str1, str2):
		if caracter[0] != caracter[1]:
			differ += 1
		else:
			str_without_caracter_differ += caracter[0]
	return (differ == 1, str_without_caracter_differ)
			
if __name__ == "__main__":
	with open("2.txt", "r") as file:
		lines = file.readlines()
	
	lines = [line[:-1] for line in lines]
	
	for str1, str2 in combinations(lines, 2):
		res = one_caracter_differ(str1, str2)
		if res[0]:
			print res[1]