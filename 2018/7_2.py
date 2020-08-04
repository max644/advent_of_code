import re

WORKER_NB = 5
BASE_STEP_DURATION = 60

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
	
class Worker:
	def __init__(self, id):
		self.id = id
		self.available = True
		self.timeRemaining = 0
		self.stepName = ""
	
	def dec(self):
		self.timeRemaining -= 1
		if self.timeRemaining == 0:
			self.available = True
			return True
		return False
		
	def get_step_duration(self, stepName):
		return BASE_STEP_DURATION + (ord(stepName) - 0x40)
	
	def assign(self, stepName):
		self.available = False
		self.stepName = stepName
		self.timeRemaining = self.get_step_duration(stepName)
		
		
def sort_steps_alphabetically(steps):
	return sorted(steps, key = lambda step:step.name)
	
def list_in_another_list(list, biggerList):
	return all(item in biggerList for item in list)

def get_first_worker_available(workers):
	for worker in workers:
		if worker.available:
			return worker
	return None

def all_workers_available(workers):
	return sum(1 for worker in workers if worker.available) == len(workers)

if __name__ == "__main__":
	with open("7.txt", "r") as file:
		lines = file.readlines()
		
	lines = [line[:-1] for line in lines]
	
	causalities = [Causality(line) for line in lines]
	
	stepNames = list(set([causality.causeStep for causality in causalities] + [causality.consequenceStep for causality in causalities]))
	
	steps = [Step(step, causalities) for step in stepNames]
	
	workers = [Worker(idx) for idx in range(WORKER_NB)]
	
	order = []
	stepsDone = []
	
	seconds = 0
	while len(stepsDone) < len(steps) or not all_workers_available(workers):
		for worker in workers:
			if worker.dec():
				stepsDone.append(worker.stepName)
				
		for step in sort_steps_alphabetically(steps):
			if list_in_another_list(step.prerequisite, stepsDone) and step.name not in order:
				worker = get_first_worker_available(workers)
				if worker != None:
					worker.assign(step.name)
					order.append(worker.stepName)
		seconds += 1
		
	print "".join(stepsDone)
	print seconds-1