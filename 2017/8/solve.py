import re
from enum import Enum
from collections import defaultdict

INPUT_FILE = "input.txt"

class OpType(Enum):
	INC = "inc"
	DEC = "dec"
	
class CompType(Enum):
	LT = "<"
	GT = ">"
	LTE = "<="
	GTE = ">="
	EQUALS = "=="
	NOT_EQUALS = "!="

class Instruction:
	def __init__(self, op_reg, op_type, op_value, comp_reg, comp_type, comp_value):
		self.op_reg = op_reg
		self.op_type = op_type
		self.op_value = int(op_value)
		self.comp_reg = comp_reg
		self.comp_type = comp_type
		self.comp_value = int(comp_value)
	
	def __str__(self):
		return "{} {} {} if {} {} {}".format(self.op_reg, self.op_type, self.op_value, self.comp_reg, self.comp_type, self.comp_value)

class Program:
	def __init__(self, instructions):
		self.instructions = instructions
		self.registers = defaultdict(lambda: 0)
		self.executionHighestValue = -99999999
		
	def execute(self):
		for instr in instructions:
			condutionResult = False
			if instr.comp_type == CompType.LT.value:
				condutionResult = self.registers[instr.comp_reg] < instr.comp_value
			elif instr.comp_type == CompType.GT.value:
				condutionResult = self.registers[instr.comp_reg] > instr.comp_value
			elif instr.comp_type == CompType.LTE.value:
				condutionResult = self.registers[instr.comp_reg] <= instr.comp_value
			elif instr.comp_type == CompType.GTE.value:
				condutionResult = self.registers[instr.comp_reg] >= instr.comp_value
			elif instr.comp_type == CompType.EQUALS.value:
				condutionResult = self.registers[instr.comp_reg] == instr.comp_value
			elif instr.comp_type == CompType.NOT_EQUALS.value:
				condutionResult = self.registers[instr.comp_reg] != instr.comp_value

			if condutionResult:
				if instr.op_type == OpType.INC.value:
					self.registers[instr.op_reg] = self.registers[instr.op_reg] + instr.op_value
				elif instr.op_type == OpType.DEC.value:
					self.registers[instr.op_reg] = self.registers[instr.op_reg] - instr.op_value
	
			self.logHighestValue()
		
	def logHighestValue(self):
		currentHighestValue = max(self.registers.values())
		if currentHighestValue > self.executionHighestValue:
			self.executionHighestValue = currentHighestValue
	
def parse(line):
	name = ""
	weight = 0
	children = []
	pattern = re.compile('([a-z]+)\s(inc|dec)\s(-?\d+)\sif\s([a-z]+)\s(==|!=|>=|<=|>|<)\s(-?\d+)')
	
	match = pattern.match(line)
	return match.group(1), match.group(2), match.group(3), match.group(4), match.group(5), match.group(6)
	
if __name__ == "__main__":
	lines = []
	with open(INPUT_FILE, "r") as file:
		lines = file.readlines()
		
	lines = [line[:-1] for line in lines]
	instructions = []
	for line in lines:
		instructions.append(Instruction(*parse(line)))
	
	program = Program(instructions)
	program.execute()
	
	print "1==> {}".format(max(program.registers.values()))
	print "2==> {}".format(program.executionHighestValue)