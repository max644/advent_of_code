import re
from collections import defaultdict
INPUT_FILE = "input.txt"

def isDigits(inputStr):
	return bool(re.search("^-?\d+$", inputStr))

class Context:
	def __init__(self, programId):
		self.programId = programId
		self.registers = defaultdict(lambda: 0)
		self.registers["p"] = programId
		self.ip = 0
		self.valueQueue = []
		self.isLocked = False
		self.valuesSent = 0
		
	def addValueToQueue(self, value):
		self.valueQueue.append(value)
		self.isLocked = False
		
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
	
	def execute(self, contextSelf, contextOther):
		value = None
		if self.value_2 != None :
			value = self.value_2
		if self.reg_2 != None:
			value = contextSelf.registers[self.reg_2]
			
		if self.opcode == "snd":
			contextOther.addValueToQueue(contextSelf.registers[self.reg_1])
			contextSelf.valuesSent += 1
			contextSelf.ip += 1
		elif self.opcode == "set":
			contextSelf.registers[self.reg_1] = value
			contextSelf.ip += 1
		elif self.opcode == "add":
			contextSelf.registers[self.reg_1] += value
			contextSelf.ip += 1
		elif self.opcode == "mul":
			contextSelf.registers[self.reg_1] *= value
			contextSelf.ip += 1
		elif self.opcode == "mod":
			contextSelf.registers[self.reg_1] %= value
			contextSelf.ip += 1
		elif self.opcode == "rcv":
			if len(contextSelf.valueQueue) > 0:
				contextSelf.registers[self.reg_1] = contextSelf.valueQueue.pop(0)
				contextSelf.ip += 1
			else:
				contextSelf.isLocked = True
		elif self.opcode == "jgz":
			if self.reg_1 != None and contextSelf.registers[self.reg_1] > 0:
				contextSelf.ip += value
			elif self.value_1 > 0:
				contextSelf.ip += value
			else:
				contextSelf.ip += 1
		
if __name__ == "__main__":
	lines = []
	with open(INPUT_FILE, "r") as file:
		lines = file.readlines()
	
	lines = [line[:-1] for line in lines]
	
	instructions = [Instruction(line) for line in lines]
	
	contextProgA = Context(0)
	contextProgB = Context(1)
	while not (contextProgA.isLocked and contextProgB.isLocked):
		if not contextProgA.isLocked:
			instructionProgA = instructions[contextProgA.ip]
			instructionProgA.execute(contextProgA, contextProgB)
		elif not contextProgB.isLocked:
			instructionProgB = instructions[contextProgB.ip]
			instructionProgB.execute(contextProgB, contextProgA)
	
	print "==> {}".format(contextProgB.valuesSent)