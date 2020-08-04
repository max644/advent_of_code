import re
from itertools import combinations
import copy

class Moon:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.vx = 0
        self.vy = 0
        self.vz = 0
        
    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz
        
    def getCoordIdx(self, idx):
        if idx == 0:
            return self.x
        elif idx == 1:
            return self.y
        else:
            return self.z
            
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
        
    def getZ(self):
        return self.z
    
    def getVelocityIdx(self, idx):
        if idx == 0:
            return self.vx
        elif idx == 1:
            return self.vy
        else:
            return self.vz
            
    def setVelocityIdx(self, idx, value):
        if idx == 0:
            self.vx = value
        elif idx == 1:
            self.vy = value
        else:
            self.vz = value

    def potentialEnergy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)
        
    def kineticEnergy(self):
        return abs(self.vx) + abs(self.vy) + abs(self.vz)

    def totalEnergy(self):
        return self.potentialEnergy() * self.kineticEnergy()
        
    def __str__(self):
        return "pos=<x=%d, y=%d, z=%d>, vel=<x=%d, y=%d, z=%d>" % (self.x, self.y, self.z, self.vx, self.vy, self.vz)

def pgcd(nbA, nbB):
    high, low = max(nbA, nbB), min(nbA, nbB)
    while low != 0:
        rest = high % low
        high = low
        low = rest
    return high

def ppcm(nbA, nbB):
    return abs(nbA * nbB) / pgcd(nbA, nbB)

COORDS = ["x", "y", "z"]

with open("12.txt", "r") as file:
    lines = file.readlines()
    
origMoons = [Moon(*[int(nb) for nb in re.findall("(-?\d+)", line)]) for line in lines]
moons = copy.deepcopy(origMoons)

for idx in range(1000):
    for moonA, moonB in combinations(moons, 2):
        for coordIdx in range(3):
            minMoon = min(moonA, moonB, key=lambda moon: moon.getCoordIdx(coordIdx))
            maxMoon = max(moonA, moonB, key=lambda moon: moon.getCoordIdx(coordIdx))
            if minMoon.getCoordIdx(coordIdx) != maxMoon.getCoordIdx(coordIdx):
                minMoon.setVelocityIdx(coordIdx, minMoon.getVelocityIdx(coordIdx) + 1)
                maxMoon.setVelocityIdx(coordIdx, maxMoon.getVelocityIdx(coordIdx) - 1)
            
    for moon in moons:
        moon.move()
        
    # print("\nAfter %d steps : " % (idx+1))
    # for moon in moons:
        # print(moon)
        
print("Step 1 : %d" % sum(moon.totalEnergy() for moon in moons))


cycle = []
for coordIdx, coord in enumerate(COORDS):
    moons = copy.deepcopy(origMoons)
    histo = {}
    nextSpace = (moons[0].getCoordIdx(coordIdx), moons[1].getCoordIdx(coordIdx), moons[2].getCoordIdx(coordIdx), moons[3].getCoordIdx(coordIdx), moons[0].getVelocityIdx(coordIdx), moons[1].getVelocityIdx(coordIdx), moons[2].getVelocityIdx(coordIdx), moons[3].getVelocityIdx(coordIdx))
    idx = 0
    while nextSpace not in histo:
        histo[nextSpace] = idx
        for moonA, moonB in combinations(moons, 2):
            minMoonCoord = min(moonA, moonB, key=lambda moon: moon.getCoordIdx(coordIdx))
            maxMoonCoord = max(moonA, moonB, key=lambda moon: moon.getCoordIdx(coordIdx))
            if minMoonCoord.getCoordIdx(coordIdx) != maxMoonCoord.getCoordIdx(coordIdx):
                minMoonCoord.setVelocityIdx(coordIdx, minMoonCoord.getVelocityIdx(coordIdx) + 1)
                maxMoonCoord.setVelocityIdx(coordIdx, maxMoonCoord.getVelocityIdx(coordIdx) - 1)
        
        for moon in moons:
            moon.move()
        
        nextSpace = (moons[0].getCoordIdx(coordIdx), moons[1].getCoordIdx(coordIdx), moons[2].getCoordIdx(coordIdx), moons[3].getCoordIdx(coordIdx) , moons[0].getVelocityIdx(coordIdx), moons[1].getVelocityIdx(coordIdx), moons[2].getVelocityIdx(coordIdx), moons[3].getVelocityIdx(coordIdx))
        idx += 1

    print("For %s, state %d is the same as state %d" % (coord, idx, histo[nextSpace]))
    cycle.append(idx - histo[nextSpace])

print("Step 2 : %d" % ppcm(ppcm(cycle[0], cycle[1]), cycle[2]))