from collections import defaultdict

class Opcode:
    def __init__(self, code):
        self.opcode = code % 100
        self.param1mode = (code // 100) % 10
        self.param2mode = (code // 1000) % 10
        self.param3mode = (code // 10000) % 10
        
class Program:
    def __init__(self, code, inputs):
        self.memory = defaultdict(int, {offset:intVal for offset, intVal in enumerate(code)})
        self.ip = 0
        self.inputs = inputs
        self.inputIdx = 0
        self.outputs = []
        self.relativeBase = 0
    
    def getInput(self):
        if self.inputIdx >= len(self.inputs):
            print("no more input")
            sys.exit()
        ret = self.inputs[self.inputIdx]
        self.inputIdx += 1
        return ret
    
    def getParamsAddr(self, opcode):
        ret = []
        for paramIdx, paramMode in zip([1, 2, 3], [opcode.param1mode, opcode.param2mode, opcode.param3mode]):
            if paramMode == 1:
                ret.append(self.ip + paramIdx)
            else:
                addrOffset = self.ip + paramIdx
                if paramMode == 0:
                    ret.append(None if addrOffset not in self.memory else self.memory[addrOffset])
                elif paramMode == 2:
                    ret.append(None if addrOffset not in self.memory else self.memory[self.ip + paramIdx] + self.relativeBase)
                
        return ret
        
    def run(self):
        while self.memory[self.ip] != 99:
            opcode = Opcode(self.memory[self.ip])
            param1Addr, param2Addr, param3Addr = self.getParamsAddr(opcode)
            # print("----")
            # print("opcode : ", opcode.opcode)
            # print("params mods : ", opcode.param1mode, opcode.param2mode, opcode.param3mode)
            # print("params addrs : ", param1Addr, param2Addr, param3Addr)
            if opcode.opcode == 1:
                self.memory[param3Addr] = self.memory[param1Addr] + self.memory[param2Addr]
                self.ip += 4
            elif opcode.opcode == 2:
                self.memory[param3Addr] = self.memory[param1Addr] * self.memory[param2Addr]
                self.ip += 4
            elif opcode.opcode == 3:
                self.memory[param1Addr] = self.getInput()
                self.ip += 2
            elif opcode.opcode == 4:
                out = self.memory[param1Addr]
                self.outputs.append(out)
                self.ip += 2
                return out
            elif opcode.opcode == 5:
                if self.memory[param1Addr] != 0:
                    self.ip = self.memory[param2Addr]
                else:
                    self.ip += 3
            elif opcode.opcode == 6:
                if self.memory[param1Addr] == 0:
                    self.ip = self.memory[param2Addr]
                else:
                    self.ip += 3
            elif opcode.opcode == 7:
                if self.memory[param1Addr] < self.memory[param2Addr]:
                    self.memory[param3Addr] = 1
                else:
                    self.memory[param3Addr] = 0
                self.ip += 4
            elif opcode.opcode == 8:
                if self.memory[param1Addr] == self.memory[param2Addr]:
                    self.memory[param3Addr] = 1
                else:
                    self.memory[param3Addr] = 0
                self.ip += 4
            elif opcode.opcode == 9:
                self.relativeBase += self.memory[param1Addr]
                self.ip += 2
            else:
                print("unknown opcode at %d" % self.ip)
                sys.exit()


tiles = {}
with open("13.txt", "r") as file:
    code = [int(intVal) for intVal in file.read().split(",")]
    
program = Program(code, [])
stop = False
test = 0
while not stop:
    x = program.run()
    if x == None:
        stop = True
    else:
        y = program.run()
        type = program.run()
        if type == 2:
            tiles[(x, y)] = type
            test += 1
    print(x, y, type)
print(len(tiles))
print(test)
# 358 too high