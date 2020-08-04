import re
import datetime
import operator
from collections import defaultdict


class Instruction:
	def __init__(self, line):
		m = re.match(r"\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] (.*)", line)
		self.year = int(m.group(1))
		self.month = int(m.group(2))
		self.day = int(m.group(3))
		self.hour = int(m.group(4))
		self.minute = int(m.group(5))
		self.date = datetime.datetime(self.year, self.month, self.day, self.hour, self.minute)
		self.guard_id = -1
		self.action = ""
		self.raw_action = m.group(6)
	
	def fill_action(self, guard_id):
		if self.raw_action.startswith("falls"):
			self.guard_id = guard_id
			self.action = "sleep"
		elif self.raw_action.startswith("wakes"):
			self.guard_id = guard_id
			self.action = "wakes up"
		elif self.raw_action.startswith("Guard"):
			self.guard_id = int(re.match(r"Guard #(\d+) begins shift", self.raw_action).group(1))
			self.action = "begins shift"
		
class Nap:
	def __init__(self, start_time, end_time):
		self.start = start_time
		self.end = end_time
		
	def get_duration(self):
		return (self.end - self.start).total_seconds()/60
		#return (self.end.total_seconds() - self.start.total_seconds()) / 60
		
class Guard:
	def __init__(self, guard_id, instructions):
		self.guard_id = guard_id
		self.nap_list = []
		start = None
		for instr in instructions:
			if instr.action == "sleep":
				start = instr.date
			elif instr.action == "wakes up":
				self.nap_list.append(Nap(start, instr.date))
	
	def most_slept_minute(self):
		minutes = {}
		for minute in range(0, 59):
			minutes[minute] = sum([1 for nap in self.nap_list if nap.start.minute <= minute and nap.end.minute > minute])
		return max(minutes.iteritems(), key=operator.itemgetter(1))

if __name__ == "__main__":
	with open("4.txt", "r") as file:
		lines = file.readlines()
		
	lines = [line[:-1] for line in lines]
	
	instructions = [Instruction(line) for line in lines]
	
	instructions = sorted(instructions, key = lambda instr: (instr.year, instr.month, instr.day, instr.hour, instr.minute))
	
	guard_id = -1
	for instr in instructions:
		instr.fill_action(guard_id)
		guard_id = instr.guard_id
		
	instructions_by_guard_id = defaultdict(list)
	for instr in instructions:
		instructions_by_guard_id[instr.guard_id].append(instr)
		
	guards = []
	for guard_id, instructions in instructions_by_guard_id.iteritems():
		guards.append(Guard(guard_id, instructions))
	
	max_nap_guard = max(guards, key = lambda guard: sum([nap.get_duration() for nap in guard.nap_list]))
	
	print max_nap_guard.guard_id * max_nap_guard.most_slept_minute()[0]
	
	sleepiest_guard_and_minute = max([(guard.guard_id, guard.most_slept_minute()) for guard in guards], key=lambda x:x[1][1])
	
	print sleepiest_guard_and_minute[0] * sleepiest_guard_and_minute[1][0]