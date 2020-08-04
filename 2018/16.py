import re
import copy

class VM:
    def __init__(self, registers, program, opcodeMethods):
        self.registers = registers
        self.program = program
        self.opcodeMethods = opcodeMethods
        self.ip = 0
        
    def run(self):
        for instruction in program:
            opcode = instruction[0]
            self.callByName(self.opcodeMethods[opcode])
            self.ip += 1
            print(self.registers)
        
    def callByName(self, methodName):
        getattr(VM, methodName)(self, self.program[self.ip][1], self.program[self.ip][2], self.program[self.ip][3])
        
    def addr(self, rA, rB, rC):
        self.registers[rC] = self.registers[rA] + self.registers[rB]
        
    def addi(self, rA, vB, rC):
        self.registers[rC] = self.registers[rA] + vB
        
    def mulr(self, rA, rB, rC):
        self.registers[rC] = self.registers[rA] * self.registers[rB]
        
    def muli(self, rA, vB, rC):
        self.registers[rC] = self.registers[rA] * vB
    
    def banr(self, rA, rB, rC):
        self.registers[rC] = self.registers[rA] & self.registers[rB]
    
    def bani(self, rA, vB, rC):
        self.registers[rC] = self.registers[rA] & vB
        
    def borr(self, rA, rB, rC):
        self.registers[rC] = self.registers[rA] | self.registers[rB]
    
    def bori(self, rA, vB, rC):
        self.registers[rC] = self.registers[rA] | vB
        
    def setr(self, rA, _, rC):
        self.registers[rC] = self.registers[rA]
        
    def seti(self, vA, _, rC):
        self.registers[rC] = vA
        
    def gtir(self, vA, rB, rC):
        self.registers[rC] = 1 if vA > self.registers[rB] else 0
        
    def gtri(self, rA, vB, rC):
        self.registers[rC] = 1 if self.registers[rA] > vB else 0
    
    def gtrr(self, rA, rB, rC):
        self.registers[rC] = 1 if self.registers[rA] > self.registers[rB] else 0
    
    def eqir(self, vA, rB, rC):
        self.registers[rC] = 1 if vA == self.registers[rB] else 0
        
    def eqri(self, rA, vB, rC):
        self.registers[rC] = 1 if self.registers[rA] == vB else 0
    
    def eqrr(self, rA, rB, rC):
        self.registers[rC] = 1 if self.registers[rA] == self.registers[rB] else 0
    
class CpuMonitoring:
    def __init__(self, l1, l2, l3):
        self.registers_before = [int(x) for x in re.findall("(\d+)", l1)]
        self.program = [[int(x) for x in re.findall("(\d+)", l2)]]
        self.registers_after = [int(x) for x in re.findall("(\d+)", l3)]
        
    def validOpcodes(self, instuctionMethods):
        ret = []
        vmInstances = [VM(copy.deepcopy(self.registers_before), copy.deepcopy(self.program), None) for _ in range(16)]
        for idx, instuctionMethod in enumerate(instuctionMethods):
            vmInstances[idx].callByName(instuctionMethod)
            if vmInstances[idx].registers == self.registers_after:
                ret.append(instuctionMethod)
        return ret
        
        
with open("16.txt", "r") as file:
    content = file.read()
    
monitoringSample = content[0:content.rindex("\n\n\n")]
monitoringSample = monitoringSample.split("\n")
program = content[content.rindex("\n\n\n")+3:]
castToInt = lambda ll: [int(x) for x in ll]
program = [castToInt(re.findall("(\d+)", line)) for line in program.split("\n")]

instuctionMethods = ["addr", "addi", "mulr", "muli", "banr", "bani", "borr", "bori", "setr", "seti", "gtir", "gtri", "gtrr", "eqir", "eqri", "eqrr"]

total = 0
for idx in range(0, len(monitoringSample), 4):
    if len(CpuMonitoring(monitoringSample[idx+0], monitoringSample[idx+1], monitoringSample[idx+2]).validOpcodes(instuctionMethods)) >= 3:
        total += 1

print("Step 1 : %d" % total)

opcodeMethods = {}
idx = 0
while len(instuctionMethods) > 0:
    cpuMonitoring = CpuMonitoring(monitoringSample[idx+0], monitoringSample[idx+1], monitoringSample[idx+2])
    if cpuMonitoring.program[0][0] not in opcodeMethods:
        validOpcodes = CpuMonitoring(monitoringSample[idx+0], monitoringSample[idx+1], monitoringSample[idx+2]).validOpcodes(instuctionMethods)
        validOpcodes = [validOpcode for validOpcode in validOpcodes if validOpcode in instuctionMethods]
        if len(validOpcodes) == 1:
            opcodeMethods[cpuMonitoring.program[0][0]] = validOpcodes[0]
            instuctionMethods.remove(validOpcodes[0])
            idx = 0 
    idx += 4

print(opcodeMethods)
vm = VM([0, 0, 0, 0], program, opcodeMethods)
vm.run()
print("Step 2 : %d" % vm.registers[0])