import re
INPUT_FILE = "input.txt"
ITERATIONS = 40000000

class Generator:
	def __init__(self, value, factor):
		self.value = value
		self.factor = factor

	def computeNextValue(self):
		self.value = (self.value * self.factor) % 2147483647
	
if __name__ == "__main__":
	content = ""
	with open(INPUT_FILE, "r") as file:
		content = file.read()
	
	mg = re.search("Generator A starts with (\d+)", content)
	genA = Generator(int(mg.group(1)), 16807)
	
	mg = re.search("Generator B starts with (\d+)", content)
	genB = Generator(int(mg.group(1)), 48271)
	
	cnt = 0
	for idx in range(ITERATIONS):
		genA.computeNextValue()
		genB.computeNextValue()
		if bin(genA.value)[-16:] == bin(genB.value)[-16:]:
			cnt += 1
	
	print "==> {}".format(cnt)