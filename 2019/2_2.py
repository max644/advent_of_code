import copy

with open("2.txt", "r") as file:
    content = file.read()
    
intcode = [int(x) for x in content.split(",")]

def run(intcode):
    ip = 0
    while intcode[ip] != 99:
        instruction = intcode[ip]
        if instruction == 1:
            intcode[intcode[ip+3]] = intcode[intcode[ip+1]] + intcode[intcode[ip+2]]
        elif instruction == 2:
            intcode[intcode[ip+3]] = intcode[intcode[ip+1]] * intcode[intcode[ip+2]]
        else:
            print("unknown opcode at %d", ip)
        ip += 4
    return intcode[0]

for arg1 in range(0, 100):
    for arg2 in range(0, 100):
        candidate = copy.deepcopy(intcode)
        candidate[1] = arg1
        candidate[2] = arg2
        if run(candidate) == 19690720:
            print("Found 19690720 with arg1 = %d and arg2 = %d" % (arg1, arg2))
            print("Step 2 response : %d" % (100 * arg1 + arg2))