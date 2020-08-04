import re
from collections import defaultdict

intre = re.compile("\d+")
intobj = re.compile("value|bot|output")

class Bot:
	def __init__(self):
		self.lowdst = None
		self.highdst = None
		self.values = []
	
class Output:
	def __init__(self):
		self.values = []

# def printbots(bots):
	# for botidx, bot in bots.items() :
		# print "bot " + str(botidx) + " :\nlow dst : " + str(bot.lowdst) + "\nhigh dst" + str(bot.highdst) + "\nvalues : " + str(bot.values)

# def printoutputs(outputs):
	# for outputidx, output in outputs.items() :
		# print "output " + str(outputidx) + " :\nvalues : " + str(output.values)
		
with open("input.txt", "r") as f:
	lines = f.readlines()
	lines = [line[:-1] for line in lines]
	
	bots = defaultdict(Bot)
	outputs = defaultdict(Output)
	for line in lines:
		ids = map(int, intre.findall(line))
		objects = intobj.findall(line)
		
		if objects[0] == "value":
			bots[ids[1]].values.append(ids[0])
			
		elif objects[0] == "bot":
			if objects[1] == "bot":
				bots[ids[0]].lowdst = bots[ids[1]]
			elif objects[1] == "output":
				bots[ids[0]].lowdst = outputs[ids[1]]
			if objects[2] == "bot":
				bots[ids[0]].highdst = bots[ids[2]]
			elif objects[2] == "output":
				bots[ids[0]].highdst = outputs[ids[2]]
				
	stop = False
	while not stop:
		stop = True
		for botidx, bot in bots.items():
			if len(bot.values) > 1:
				if 17 in bot.values and 61 in bot.values:
					print botidx
				bot.lowdst.values.append(min(bot.values))
				bot.highdst.values.append(max(bot.values))
				bot.values = []
				stop = False
			
	print reduce(lambda x,y:x*y, [1, outputs[0].values[0], outputs[1].values[0], outputs[2].values[0]])
			
			
			
			
			
			