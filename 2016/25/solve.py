import re

re_num = re.compile("-?\d+")

def getvalue(ope, registers):
	value = 0
	if re_num.match(ope):
		value = int(ope)
	else:
		value = registers[ope]
	return value


with open("input.txt", "r") as file:
	lines = file.readlines()
	lines = [line[:-1] for line in lines]

	
	reg_a = 0
	while True:
		if reg_a % 1000 == 0:
			print reg_a
		ip = 0
		stop = False
		prevval = 1
		cnt = 0
		registers = {
			"a" : reg_a,
			"b" : 0,
			"c" : 0,
			"d" : 0
		}
		signal = ""
		while ip < len(lines) and not stop:
			line = lines[ip]
			parts = line.split(" ")

			instr = parts[0]
			ope1 = parts[1]
			if len(parts) > 2:
				ope2 = parts[2]

			if instr == "cpy":
				value = getvalue(ope1, registers)
				registers[ope2] = value

			elif instr == "inc":
				registers[ope1] += 1

			elif instr == "dec":
				registers[ope1] -= 1

			elif instr == "jnz":
				value = getvalue(ope1, registers)
				if value != 0:
					ip += int(ope2)-1
			
			elif instr == "out":
				value = getvalue(ope1, registers)
				signal += str(value)
				# if (prevval == 0 and value != 1) or (prevval == 1 and value != 0):
					# stop = True
				# prevval = value
				# cnt += 1

			ip += 1
			if ip == 29:
				print reg_a, signal
				stop = True
		reg_a += 1
