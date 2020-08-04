from collections import defaultdict
from enum import Enum
import copy
from program import Program

class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4

class STATUS(Enum):
    UNKNOWN = "?"
    WALL = "#"
    EMPTY = "X"
    OXYGEN_SYS = "G"
    
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.status = STATUS.UNKNOWN
        self.linkedPositions = []
        self.oxygen = False
    
    def pos(self):
        return (self.x, self.y)
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
        
    def __str__(self):
        return "(%d, %d)" % (self.x, self.y)

class World:
    def __init__(self, code):
        self.program = Program(code, [])
        self.droidCoord = (0, 0)
        
        position = Position(0, 0)
        self.positions = {position.pos(): position}
        position.status = STATUS.EMPTY
        adjacent = self.getAdjacentsPositions(position)
        position.linkedPositions = adjacent
        self.uncoveredPositions = adjacent
        self.coveredPositions = [position]

    def getAdjacentsPositions(self, position):
        ret = []
        if (position.x + 1, position.y) in self.positions:
            ret.append(self.positions[(position.x + 1, position.y)])
        else:
            ret.append(Position(position.x + 1, position.y))
        if (position.x - 1, position.y) in self.positions:
            ret.append(self.positions[(position.x - 1, position.y)])
        else:
            ret.append(Position(position.x - 1, position.y))
        if (position.x, position.y + 1) in self.positions:
            ret.append(self.positions[(position.x, position.y + 1)])
        else:
            ret.append(Position(position.x, position.y + 1))
        if (position.x, position.y - 1) in self.positions:
            ret.append(self.positions[(position.x, position.y - 1)])
        else:
            ret.append(Position(position.x, position.y - 1))
        return ret
    
    def shortestPath(self, destination):
        visitedPositions = {}
        visitedPositions[self.droidCoord] = (0, [])
        while destination.pos() not in visitedPositions:
            newlyVisitedPositions = {}
            for coord, infos in visitedPositions.items():
                distance, path = infos
                if coord in self.positions:
                    for adjacent in self.positions[coord].linkedPositions:
                        if adjacent.status != STATUS.WALL and adjacent.pos() not in visitedPositions:
                            newlyVisitedPositions[adjacent.pos()] = (distance + 1, path + [adjacent])
            visitedPositions.update(newlyVisitedPositions)
        return visitedPositions[destination.pos()][1]
    
    def pathToInstructions(self, path):
        instructions = []
        curpos = copy.deepcopy(self.droidCoord)
        for position in path:
            if (curpos[0] + 1, curpos[1]) == position.pos():
                instructions.append(Direction.EAST)
                curpos = (curpos[0] + 1, curpos[1])
            elif (curpos[0] - 1, curpos[1]) == position.pos():
                instructions.append(Direction.WEST)
                curpos = (curpos[0] - 1, curpos[1])
            elif (curpos[0], curpos[1] + 1) == position.pos():
                instructions.append(Direction.NORTH)
                curpos = (curpos[0], curpos[1] + 1)
            elif (curpos[0], curpos[1] - 1) == position.pos():
                instructions.append(Direction.SOUTH)
                curpos = (curpos[0], curpos[1] - 1)
        return instructions
    
    def move(self, instructions):
        for instruction, position in instructions:
            self.program.inputs.append(instruction.value)
            ret = self.program.run()
            if ret != 0:
                self.droidCoord = position.pos()
        if ret == 0:
            position.status = STATUS.WALL
        else:
            if ret == 1:
                position.status = STATUS.EMPTY
            elif ret == 2:
                position.status = STATUS.OXYGEN_SYS
            adjacents = self.getAdjacentsPositions(position)
            self.uncoveredPositions += [adj for adj in adjacents if adj not in self.uncoveredPositions and adj not in self.coveredPositions]
            position.linkedPositions = adjacents
            self.positions[position.pos()] = position
        self.coveredPositions.append(position)
                
    def discover(self):
        #while STATUS.OXYGEN_SYS not in [position.status for position in self.positions.values()]:
        while len(self.uncoveredPositions) > 0:
            next = self.uncoveredPositions[0]
            path = self.shortestPath(next)
            instructions = self.pathToInstructions(path)
            self.move(zip(instructions, path))
            self.uncoveredPositions = self.uncoveredPositions[1:]
        
    def pathFromOrigineToOxygen(self):
        self.droidCoord = (0, 0)
        return self.shortestPath()
        
    def show(self):
        xmin, xmax = min(self.positions, key=lambda coord: self.positions[coord].x)[0], max(self.positions, key=lambda coord: self.positions[coord].x)[0]
        ymin, ymax = min(self.positions, key=lambda coord: self.positions[coord].y)[1], max(self.positions, key=lambda coord: self.positions[coord].y)[1]
        print(xmin, xmax, ymin, ymax)
        out = ""
        for y in range(ymin, ymax+1):
            for x in range(xmin, xmax+1):
                if (x, y) == (0, 0):
                    out += "S"
                elif (x, y) in self.positions:
                    out += self.positions[(x, y)].status.value
                else:
                    out += " "
            out += "\n"
        print(out)
        
    def fillWithOxygen(self, depth):
        positionsToOxygen = []
        
        for position in self.positions.values():
            if position.oxygen:
                positionsToOxygen += position.linkedPositions
        
        for position in positionsToOxygen:
            position.oxygen = True
           
        if len([position for position in self.positions.values() if not position.oxygen]) == 0:
            return depth
        return self.fillWithOxygen(depth + 1)
        
with open("15.txt", "r") as file:
    code = [int(intVal) for intVal in file.read().split(",")]

world = World(code)
world.discover()
world.show()
world.droidCoord = (0, 0)
oxygenSysPosition = [position for position in world.positions.values() if position.status == STATUS.OXYGEN_SYS][0]
print("Step 1 : %d" % len(world.shortestPath(oxygenSysPosition)))

oxygenSysPosition.oxygen = True
print("Step 2 : %d" % world.fillWithOxygen(1))