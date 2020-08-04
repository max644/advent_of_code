from enum import Enum
import math
import copy

TARGET = 277678
KEY_FORMAT = "({}, {})"

#
#
#	37	36	35	34	33	32	31
#	38	17	16	15	14	13	30
#	39	18	5	4	3	12	29
#	40	19	6	1	2	11	28
#	41	20	7	8	9	10	27
#	42	21	22	23	24	25	26
#	43	44	45	46	47	48	49						
#
#	c1 : 1
#	c2 : 8	/	9
#	c3 : 16	/	25
#
# 	1		2		10		26		50
#	
#	1	2	4	6	8	10
#	1	3	7	13	21	31
#

class Orientation(Enum):
	SOUTH = 0
	EST = 1
	NORTH = 2
	OUEST = 3
	
	def next(self):
		return Orientation((self.value+1)%4)

class Coordinates:
	adjacents = [
		[1, 0],
		[1, 1],
		[1, -1],
		[0, 1],
		[0, -1],
		[-1, 0],
		[-1, 1],
		[-1, -1]
	]

	def __init__(self, x, y, value, index):
		self.x = x
		self.y = y
		self.value = value
		self.index = index

	def __str__(self):
		return KEY_FORMAT.format(self.x, self.y)
	
	def sumAdjacent(self, positions):
		summ = 0
		for adjacent in Coordinates.adjacents:
			key = "({}, {})".format(self.x + adjacent[0], self.y + adjacent[1])
			if key in positions:
				summ += positions[key].value
		return summ
	
if __name__ == "__main__":
	square_side = 1
	idx2 = 0
	coordinates = Coordinates(0, 0, 1, 1)
	orientation = Orientation.SOUTH
	
	positions = {"1": copy.deepcopy(coordinates)}
	positions2 = {"(0, 0)": copy.deepcopy(coordinates)}
	
	for idx in range(2, TARGET+1):
		if idx2 % square_side*2 == 0:
			orientation = orientation.next()
		if idx2 == square_side*2:
			idx2 = 0
			square_side += 1
		
		if orientation == Orientation.NORTH:
			coordinates.y += 1
		elif orientation == Orientation.OUEST:
			coordinates.x -= 1
		elif orientation == Orientation.SOUTH:
			coordinates.y -= 1
		elif orientation == Orientation.EST:
			coordinates.x += 1
		
		coordinates.value = coordinates.sumAdjacent(positions2)
		coordinates.index += 1 
		positions[str(idx)] = copy.deepcopy(coordinates)
		key = KEY_FORMAT.format(coordinates.x, coordinates.y)
		positions2[key] = copy.deepcopy(coordinates)
		idx2 += 1
	
	targetPosition = positions[str(TARGET)]
	print "==> {}".format(math.fabs(targetPosition.x)+math.fabs(targetPosition.y))
		
	first_index_above_target = 999999
	first_value_above_target = 0
	for key, coordinate in positions2.items():
		if coordinate.index < first_index_above_target and coordinate.value > TARGET:
			first_index_above_target = coordinate.index
			first_value_above_target = coordinate.value
	print "==> {}".format(first_value_above_target)