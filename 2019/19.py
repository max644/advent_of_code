from program import Program
import math

MAX = 1000

with open("19.txt", "r") as file:
    code = file.read()

code = [int(opcode) for opcode in code.split(",")]

def test(x, y):
	program = Program(code, [x, y])
	program.run()
	return program.outputs[0]

count = 0
attractionPoints = []
for x in range(50):
	for y in range(50):
		result = test(x, y)
		count += result
		if result == 1:
			attractionPoints.append((x, y))

def getClosestShipPosition():	
	x = 0
	for y in range(10, 5000):
		while test(x, y) != 1:
			x += 1
		if test(x+99, y-99) == 1:
			return  x*10000 + (y-99)
			
print("Step 1 : {}".format(count))
print("Step 2 : {}".format(getClosestShipPosition()))