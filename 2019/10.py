import math
from collections import defaultdict

with open("10.txt", "r") as file:
    space = [list(line.strip()) for line in file.readlines()]

width = len(space[0])
height = len(space)
meteorCoords = [(colIdx, lineIdx) for lineIdx, line in enumerate(space) for colIdx, case in enumerate(line) if case == "#"]

def pgcd(nbA, nbB):
    high, low = max(nbA, nbB), min(nbA, nbB)
    while low != 0:
        rest = high % low
        high = low
        low = rest
    return high

def howManyMeteorsVisible(colIdx, lineIdx):
    visible = set(meteorCoords)
    for meteorCoord in meteorCoords:
        if meteorCoord in visible and not (meteorCoord[0] == colIdx and meteorCoord[1] == lineIdx):
            meteorCol, meteorLine = meteorCoord
            deltaLine = meteorLine - lineIdx
            deltaCol = meteorCol - colIdx
            divisor = pgcd(deltaLine, deltaCol)
            stepLine = deltaLine / abs(divisor)
            stepCol = deltaCol / abs(divisor)
            hiddenSpot = (meteorCol + stepCol, meteorLine + stepLine)
            while hiddenSpot[0] >= 0 and hiddenSpot[0] < width and hiddenSpot[1] >= 0 and hiddenSpot[1] < height:
                if hiddenSpot in visible:
                    visible.remove(hiddenSpot)
                hiddenSpot = (hiddenSpot[0] + stepCol, hiddenSpot[1] + stepLine)
    return len(visible) - 1 # we don t count the station meteor

class Meteor:
    def __init__(self, stationCol, stationLine, meteorCol, meteorLine):
        self.col = meteorCol
        self.line = meteorLine
        self.distance = self.computeDistance(stationCol, stationLine)
        self.angle = self.computeAngleWithStation(stationCol, stationLine)
        
    def computeDistance(self, stationCol, stationLine):
        return math.sqrt((stationCol - self.col) ** 2 + (stationLine - self.line) ** 2)
    
    def computeAngleWithStation(self, stationCol, stationLine):
        distance = math.sqrt((stationCol - self.col) ** 2 + (stationLine - self.line) ** 2)
        scalarProduct = (self.line - stationLine) * -1
        angle = math.degrees(math.acos(scalarProduct / distance))
        if self.col < stationCol:
            angle = 360 - angle
        return round(angle, 3) # round to avoid 2 differentes value for 1 angle due to computer lack of precision
    
    
def destroyClockwise(stationCol, stationLine):
    meteorByAngle = defaultdict(list)
    
    for meteorCol, meteorLine in meteorCoords:
        if (stationCol, stationLine) != (meteorCol, meteorLine):
            meteor = Meteor(stationCol, stationLine, meteorCol, meteorLine)
            meteorByAngle[meteor.angle].append(meteor)
    
    for _, meteors in meteorByAngle.items():
        meteors.sort(key= lambda meteor: meteor.distance)
        
    possibleAngles = list(meteorByAngle)
    possibleAngles.sort()
    destroyed = True
    destroyedIdx = 1
    while destroyed:
        destroyed = False
        for angle in possibleAngles:
            if len(meteorByAngle[angle]) > 0:
                meteor = meteorByAngle[angle].pop(0)
                print("destroyed #%d : (%d; %d)" % (destroyedIdx, meteor.col, meteor.line))
                destroyedIdx += 1
                destroyed = True

maxVisible, stationColIdx, stationLineIdx = max([(howManyMeteorsVisible(colIdx, lineIdx), colIdx, lineIdx) for colIdx, lineIdx in meteorCoords], key = lambda x: x[0])
print("Step 1 : %d" % maxVisible)
print("Step 2 : ")
destroyClockwise(stationColIdx, stationLineIdx)