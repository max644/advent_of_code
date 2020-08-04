import re

class Causality:
	def __init__(self, line):
		m = re.match(r"Step (\w) must be finished before step (\w) can begin.", line)
		self.causeStep = m.group(1)
		self.consequenceStep = m.group(2)

class Step:
	def __init__(self, stepName, causalities):
		self.name = stepName
		self.prerequisite = []
		for causality in causalities:
			if causality.consequenceStep == step:
				self.prerequisite.append(causality.causeStep)
		
def sort_steps_alphabetically(steps):
	return sorted(steps, key = lambda step:step.name)
	
def list_in_another_list(list, biggerList):
	return all(item in biggerList for item in list)

if __name__ == "__main__":
	with open("7.txt", "r") as file:
		lines = file.readlines()
		
	lines = [line[:-1] for line in lines]
	
	causalities = [Causality(line) for line in lines]
	
	stepNames = list(set([causality.causeStep for causality in causalities] + [causality.consequenceStep for causality in causalities]))
	
	steps = [Step(step, causalities) for step in stepNames]
	
	order = []
	
	for idx in range(len(steps)):
		for step in sort_steps_alphabetically(steps):
			if list_in_another_list(step.prerequisite, order) and step.name not in order:
				order.append(step.name)
				break
				
	print "".join(order)