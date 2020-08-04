import re
from collections import defaultdict
INPUT_FILE = "input.txt"

class Context:
	def __init__(self, text):
		parts = content.split("\n\n")
	
		mg = re.search("Begin in state ([A-Z]).", parts[0])
		self.startState = mg.group(1)
		
		mg = re.search("Perform a diagnostic checksum after (\d+) steps.", parts[0])
		self.iterations = int(mg.group(1))
		
		self.states = {}
		for part in parts[1:]:
			state = State(part)
			self.states[state.name] = state
		
		self.tape = defaultdict(lambda: 0)
		self.state = self.states[self.startState]
		self.position = 0
		
	def execute(self):
		for idx in range(self.iterations):
			self.state.execute(self)

class State:
	def __init__(self, text):
		mg = re.search("In state ([A-Z]):\n\s\sIf the current value is 0:\n    - Write the value ([01])\.\n    - Move one slot to the (right|left)\.\n    - Continue with state ([A-Z])\.\n  If the current value is 1:\n    - Write the value ([01])\.\n    - Move one slot to the (right|left)\.\n    - Continue with state ([A-Z])", text)
		self.name = mg.group(1)

		self.zero_nextVal = int(mg.group(2))
		self.zero_move = 1 if mg.group(3) == "right" else -1
		self.zero_nextState = mg.group(4)
		
		self.one_nextVal = int(mg.group(5))
		self.one_move = 1 if mg.group(6) == "right" else -1
		self.one_nextState = mg.group(7)

	def execute(self, context):
		value = context.tape[context.position]
		if value == 1:
			context.tape[context.position] = self.one_nextVal
			context.position += self.one_move
			context.state = context.states[self.one_nextState]
		else:
			context.tape[context.position] = self.zero_nextVal
			context.position += self.zero_move
			context.state = context.states[self.zero_nextState]
		
if __name__ == "__main__":
	content = ""
	with open(INPUT_FILE, "r") as file:
		content = file.read()
	
	context = Context(Context)
	context.execute()
	
	print "==> {}".format(sum([slotVal for _, slotVal in context.tape.items()]))