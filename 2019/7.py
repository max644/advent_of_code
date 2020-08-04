import sys
import itertools
import copy

class Opcode:
    def __init__(self, code):
        self.opcode = code % 100
        self.param1mode = (code // 100) % 10
        self.param2mode = (code // 1000) % 10
        self.param3mode = (code // 10000) % 10
        
class Program:
    def __init__(self, code, inputs):
        self.code = code
        self.ip = 0
        self.inputs = inputs
        self.inputIdx = 0
        self.outputs = []
    
    def getInput(self):
        if self.inputIdx >= len(self.inputs):
            print("no more input")
            sys.exit()
        ret = self.inputs[self.inputIdx]
        self.inputIdx += 1
        return ret
    
    def run(self):
        while self.code[self.ip] != 99:
            opcode = Opcode(self.code[self.ip])
            param1Addr = self.ip + 1 if opcode.param1mode == 1 else (None if self.ip + 1 >= len(self.code) else self.code[self.ip + 1])
            param2Addr = self.ip + 2 if opcode.param2mode == 1 else (None if self.ip + 2 >= len(self.code) else self.code[self.ip + 2])
            param3Addr = self.ip + 3 if opcode.param3mode == 1 else (None if self.ip + 3 >= len(self.code) else self.code[self.ip + 3])
            if opcode.opcode == 1:
                self.code[param3Addr] = self.code[param1Addr] + self.code[param2Addr]
                self.ip += 4
            elif opcode.opcode == 2:
                self.code[param3Addr] = self.code[param1Addr] * self.code[param2Addr]
                self.ip += 4
            elif opcode.opcode == 3:
                self.code[param1Addr] = self.getInput()
                self.ip += 2
            elif opcode.opcode == 4:
                out = self.code[param1Addr]
                self.outputs.append(out)
                self.ip += 2
                return out
            elif opcode.opcode == 5:
                if self.code[param1Addr] != 0:
                    self.ip = self.code[param2Addr]
                else:
                    self.ip += 3
            elif opcode.opcode == 6:
                if self.code[param1Addr] == 0:
                    self.ip = self.code[param2Addr]
                else:
                    self.ip += 3
            elif opcode.opcode == 7:
                if self.code[param1Addr] < self.code[param2Addr]:
                    self.code[param3Addr] = 1
                else:
                    self.code[param3Addr] = 0
                self.ip += 4
            elif opcode.opcode == 8:
                if self.code[param1Addr] == self.code[param2Addr]:
                    self.code[param3Addr] = 1
                else:
                    self.code[param3Addr] = 0
                self.ip += 4
            else:
                print("unknown opcode at %d" % self.ip)
                sys.exit()

AMPLIFIER_NB = 5

with open("7.txt", "r") as file:
    content = file.read()
    
intcode = [int(x) for x in content.split(",")]

possibleFirstInput = (0, 1, 2, 3, 4)
maxThruster = 0
for firstInput in itertools.permutations(possibleFirstInput, AMPLIFIER_NB):
    previousAmplifierResult = 0
    for amplifierIdx in range(AMPLIFIER_NB):
        program = Program(copy.deepcopy(intcode), [firstInput[amplifierIdx], previousAmplifierResult])
        previousAmplifierResult = program.run()
    maxThruster = max(maxThruster, previousAmplifierResult)

print("Step 1 : %d" % maxThruster)


def loop(programs):
    idx = 0
    previousAmplifierResult = 0
    while True:
        program = programs[idx % 5]
        program.inputs.append(previousAmplifierResult)
        res = program.run()
        if res == None:
            return previousAmplifierResult
        previousAmplifierResult = res
        idx += 1
    return previousAmplifierResult

possibleFirstInput = (5, 6, 7, 8, 9)
maxThruster = 0
for firstInput in itertools.permutations(possibleFirstInput, AMPLIFIER_NB):
    maxThruster = max(maxThruster, loop([Program(copy.deepcopy(intcode), [firstInput[amplifierIdx % 5]]) for amplifierIdx in range(AMPLIFIER_NB)]))

print("Step 2 : %d" % maxThruster)
