class Position:
    def __init__(self, x, y, wireDistance):
        self.x = x
        self.y = y
        self.wireDistance = wireDistance

def getPositions(steps):
    position = (0, 0)
    positions = []
    wireDistance = 0
    for step in steps:
        var = int(step[1:])
        if step[0] == "R":
            positions += [Position(position[0] + x, position[1], wireDistance + x) for x in range(1, var+1)]
            position = (position[0] + var, position[1])
        if step[0] == "L":
            positions += [Position(position[0] - x, position[1], wireDistance + x) for x in range(1, var+1)]
            position = (position[0] - var, position[1])
        if step[0] == "U":
            positions += [Position(position[0], position[1] + y, wireDistance + y) for y in range(1, var+1)]
            position = (position[0], position[1] + var)
        if step[0] == "D":
            positions += [Position(position[0], position[1] - y, wireDistance + y) for y in range(1, var+1)]
            position = (position[0], position[1] - var)
        wireDistance += var
    
    return positions

with open("3.txt", "r") as file:
    lines = [line.strip() for line in file.readlines()]
    
positions1 = getPositions(lines[0].split(","))
positions2 = {(pos.x, pos.y):pos for pos in getPositions(lines[1].split(","))}
#print(positions2)

response1 = 10000000
response2 = 10000000
for position in positions1:
    if (position.x, position.y) in positions2:
        manhattanDistance = abs(position.x) + abs(position.y)
        wireDistance = position.wireDistance + positions2[(position.x, position.y)].wireDistance
        print(manhattanDistance, wireDistance)
        if manhattanDistance < response1:
            response1 = manhattanDistance
        if wireDistance < response2:
            response2 = wireDistance

print("Response 1 : %d" % response1)
print("Response 2 : %d" % response2)