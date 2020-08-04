import copy


with open("input.txt", "r") as f:
	lines = f.readlines()
	lines = [c[:-1] for c in lines]
	
	position = {"x":1, "y":1}
	for line in lines:
		for charidx in range(len(line)):
			char = line[charidx]
			if char == "R" and position["x"] < 2:
				position["x"] += 1
			if char == "L" and position["x"] > 0:
				position["x"] -= 1
			if char == "U" and position["y"] < 2:
				position["y"] += 1
			if char == "D" and position["y"] > 0:
				position["y"] -= 1
		print position
	
	print "----------------"
	
	allowed_positions = {
		"0;2":True,
		"1;1":True,
		"1;2":True,
		"1;3":True,
		"2;0":True,
		"2;1":True,
		"2;2":True,
		"2;3":True,
		"2;4":True,
		"3;1":True,
		"3;2":True,
		"3;3":True,
		"4;2":True,
	}
	position = {"x":0, "y":2}
	for line in lines:
		for charidx in range(len(line)):
			copy_position = copy.deepcopy(position)
			char = line[charidx]
			if char == "R":
				copy_position["x"] += 1
			if char == "L":
				copy_position["x"] -= 1
			if char == "U":
				copy_position["y"] += 1
			if char == "D":
				copy_position["y"] -= 1
			key = str(copy_position["x"])+";"+str(copy_position["y"])
			if key in allowed_positions:
				position = copy_position
		print position
		
#		#
#	y=2	#	1		2		3
#	y=1	#	4		5		6
#	y=0	#	7		8		9
#			x=0		x=1		x=2

# {'y': 1, 'x': 0}	4
# {'y': 0, 'x': 1}	8
# {'y': 1, 'x': 1}	5
# {'y': 0, 'x': 1}	8
# {'y': 1, 'x': 0}	4



#	y=4	#					1
#	y=3	#			2		3		4
#	y=2	#	5		6		7		8		9
#	y=1	#			A		B		C
#	y=0	#					D
#			x=0		x=1		x=2		x=3		x=4


# {'y': 2, 'x': 0}	5
# {'y': 2, 'x': 1}	6
# {'y': 3, 'x': 2}	3
# {'y': 1, 'x': 2}	B
# {'y': 2, 'x': 1}	6