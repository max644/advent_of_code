from program import Program

with open("21.txt", "r") as file:
    code = file.read()

code = [int(opcode) for opcode in code.split(",")]

instructions = [
	"NOT A T", # si un trou en A, T = True, Sinon T = False
	"OR T J", # J = True si Trou en A
	"AND A T", # T = false
	"NOT B T", # si un trou en A, T = True, Sinon T = False
	"OR T J", # J = True si Trou en A ou en B
	"AND B T", # T = false
	"NOT C T", # si un trou en C, T = True, Sinon T = False
	"OR T J", # J = True si Trou en A ou en B ou en C
	"AND C T", # T = false
	# J == True si Trou en A ou en B ou en C
	# T == False
	"OR D T", # T = True si sol en D
	"AND T J", # on saute si trou en A ou en B ou en C et sol en D
	"WALK"
]

program = Program(code, [])
program.inputs = [ord(carac) for carac in "\n".join(instructions) + "\n"]
for idx in range(2000):
	program.run()
ret = program.outputs

output = ""
for carac in ret:
	if carac < 255:
		output += chr(carac)
	else:
		output += str(carac)
print(output)
