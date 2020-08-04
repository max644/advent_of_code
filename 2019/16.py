import copy

PATTERN = [1, 0, -1, 0]

with open("16.txt", "r") as file:
    origSignal = file.read()

def computeNextSignal(signal):
    output = []
    idx = 0
    while len(output) < len(signal):
        ret = 0
        for signalIdx in range(0, len(signal) - idx):
            ret += int(signal[idx + signalIdx]) * PATTERN[(signalIdx // (idx + 1)) % len(PATTERN)]
        output.append(abs(ret) % 10)
        idx += 1
    return "".join([str(x) for x in output])

def computeEndOfSignal(signal):
    output = []
    total = 0
    for idx in range(len(signal)-1, -1, -1):
        total += int(signal[idx])
        output.append(abs(total) % 10)
    output.reverse()
    return "".join([str(x) for x in output])
    
signal = copy.deepcopy(origSignal)    
for idx in range(0, 100):
    signal = computeNextSignal(signal)
print("Step 1 : %s" % signal[0:8])

# PART 2 : 
# fist 7 digits : 5977709 so the key is the digits 5977709 -> 5977717 of the 100th signal
# signal length : 6500000
# so the patter for digits 5977709-6500000 will always be 0...1...
# last digit (n) of signal s == last digit of signal s-1
# digit n - 1 of signal s == (digit n - 1 + digit) n % 10 of signal s-1
    
signal = copy.deepcopy(origSignal)
offset = int(signal[0:7]) # 5977709
endOfSignal = (signal * 10000)[offset:]
for idx in range(0, 100):
    endOfSignal = computeEndOfSignal(endOfSignal)

print("Step 2 : %s" % endOfSignal[0:8])
# 20556360 too high
# 14288025