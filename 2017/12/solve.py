import binascii
import re
import md5
INPUT_FILE = "input.txt"

def md5Hash(x):
	m = md5.new()
	m.update(str(x))
	return binascii.hexlify(m.digest())

class Program():
	def __init__(self, name, connectedPrograms):
		self.name = name
		self.connectedPrograms = connectedPrograms

	def __str__(self):
		return "{} connected with {}".format(self.name, self.connectedPrograms)

def browseNetwork(programs, group, entryProgramName):
	entryProgram = programs[entryProgramName]
	group.append(entryProgramName)
	for childProgram in entryProgram.connectedPrograms:
		if childProgram not in group:
			browseNetwork(programs, group, childProgram)
	return group
	
	
if __name__ == "__main__":
	lines = ""
	with open(INPUT_FILE, "r") as file:
		lines = file.readlines()
	
	lines = [line[:-1] for line in lines]
	
	programs = {}
	for line in lines:
		mo = re.match("(\d+)\s<->\s([0-9,\s]+)", line)
		programs[mo.group(1)] = Program(mo.group(1), mo.group(2).split(", "))
	
	print "==> {}".format(len(browseNetwork(programs, [], "0")))
	
	groupHashs = []
	for _, program in programs.items():
		hash = md5Hash(sorted(browseNetwork(programs, [], program.name)))
		if hash not in groupHashs:
			groupHashs.append(hash)
	
	print "==> {}".format(len(groupHashs))