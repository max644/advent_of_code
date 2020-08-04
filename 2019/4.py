def toNbArray(nb):
    ret = []
    while nb > 0:
        ret.append(nb % 10)
        nb = nb // 10
    ret.reverse()
    return ret

def twoAdjacent(nb):
    digitArray = toNbArray(nb)
    for digit1, digit2 in zip(digitArray, digitArray[1:]):
        if digit1 == digit2:
            return True
    return False

def neverDecrease(nb):
    digitArray = toNbArray(nb)
    cur = 0
    for digit in digitArray:
        if digit < cur:
            return False
        cur = digit    
    return True

def onlyTwoAdjacent(nb):
    digitArray = toNbArray(nb)
    idx = 0
    while idx < len(digitArray):
        curr = digitArray[idx]
        clusterLen = 1
        while idx + clusterLen < len(digitArray) and digitArray[idx + clusterLen] == curr:
            clusterLen += 1
        if clusterLen == 2:
            return True
        idx += clusterLen
    return False

with open("4.txt", "r") as file:
    content = file.read().split("-")

min = int(content[0])
max = int(content[1])

count = 0
for nb in range(min, max+1):
    if neverDecrease(nb) and twoAdjacent(nb):
        count += 1
        
print("step 1 : %s" % count)

count = 0
for nb in range(min, max+1):
    if neverDecrease(nb) and onlyTwoAdjacent(nb):
        count += 1
        
print("step 2 : %s" % count)