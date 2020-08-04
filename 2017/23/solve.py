import re
from collections import defaultdict
INPUT_FILE = "input2.txt"

def isDigits(inputStr):
	return bool(re.search("^-?\d+$", inputStr))

class Context:
	def __init__(self):
		self.registers = defaultdict(lambda: 0)
		self.ip = 0
		self.mulInvocationCnt = 0
		
class Instruction:
	def __init__(self, line):
		parts = line.split(" ")
		self.opcode = parts[0]
		self.reg_1 = None
		self.value_1 = None
		self.reg_2 = None
		self.value_2 = None
		if isDigits(parts[1]):
			self.value_1 = int(parts[1])
		else:
			self.reg_1 = parts[1]
		if len(parts) > 2:
			if isDigits(parts[2]):
				self.value_2 = int(parts[2])
			else:
				self.reg_2 = parts[2]
	
	def execute(self, context):
		value = None
		if self.value_2 != None :
			value = self.value_2
		if self.reg_2 != None:
			value = context.registers[self.reg_2]
			
		if self.opcode == "set":
			context.registers[self.reg_1] = value
			context.ip += 1
		elif self.opcode == "sub":
			context.registers[self.reg_1] -= value
			context.ip += 1
		elif self.opcode == "mul":
			context.registers[self.reg_1] *= value
			context.ip += 1
			context.mulInvocationCnt += 1
		elif self.opcode == "jnz":
			if self.reg_1 != None and context.registers[self.reg_1] != 0:
				context.ip += value
			elif self.value_1 > 0:
				context.ip += value
			else:
				context.ip += 1
		
if __name__ == "__main__":
	lines = []
	with open(INPUT_FILE, "r") as file:
		lines = file.readlines()
	
	lines = [line[:-1] for line in lines]
	
	instructions = [Instruction(line) for line in lines]
	
	context = Context()
	while context.ip >= 0 and context.ip < len(instructions):
		instruction = instructions[context.ip]
		instruction.execute(context)
	
	print "==> {}".format(context.mulInvocationCnt)