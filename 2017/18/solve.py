import re
from collections import defaultdict
INPUT_FILE = "input.txt"

def isDigits(inputStr):
	return bool(re.search("^-?\d+$", inputStr))

class Context:
	def __init__(self):
		self.registers = defaultdict(lambda: 0)
		self.ip = 0
		self.lastSoundPlayed = None
		
	def __str__(self):
		return "ip : {}, lastSoundPlayed : {}".format(self.ip, self.lastSoundPlayed)

class Instruction:
	def __init__(self, line):
		parts = line.split(" ")
		self.opcode = parts[0]
		self.reg = parts[1]
		self.value_2 = None
		self.reg_2 = None
		if len(parts) > 2:
			if isDigits(parts[2]):
				self.value_2 = int(parts[2])
			else:
				self.reg_2 = parts[2]
	
	def __str__(self):
		return "{}, {}, [{}, {}]".format(self.opcode, self.reg, self.value_2, self.reg_2)
	
	def execute(self, context):
		value = None
		if self.value_2 != None :
			value = self.value_2
		if self.reg_2 != None:
			value = context.registers[self.reg_2]
			
		if self.opcode == "snd":
			context.lastSoundPlayed = context.registers[self.reg]
		elif self.opcode == "set":
			context.registers[self.reg] = value
		elif self.opcode == "add":
			context.registers[self.reg] += value
		elif self.opcode == "mul":
			context.registers[self.reg] *= value
		elif self.opcode == "mod":
			context.registers[self.reg] %= value
		elif self.opcode == "rcv" and context.registers[self.reg] != 0:
			print "sound played : {}".format(context.lastSoundPlayed)
		
		if self.opcode == "jgz" and context.registers[self.reg] > 0:
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