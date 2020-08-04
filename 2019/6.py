class Planet:
    def __init__(self, name):
        self.name = name
        self.centerOf = []
        self.orbit = None

with open("6.txt", "r") as file:
    lines = [line.strip() for line in file.readlines()]
    
planetsByName = {}

for line in lines:
    center, orbit = line.split(")")
    if center not in planetsByName:
        planetsByName[center] = Planet(center)
    if orbit not in planetsByName:
        planetsByName[orbit] = Planet(orbit)
    planetsByName[center].centerOf.append(planetsByName[orbit])
    planetsByName[orbit].orbit = planetsByName[center]
    
def countOrbits(node, depth):
    return len(node.centerOf) * depth + sum(countOrbits(orbit, depth+1) for orbit in node.centerOf)

def pathToCom(node):
    ret = [node.name]
    if node.orbit != None:
        ret += pathToCom(node.orbit)
    return ret

print("Step 1 : %d" % countOrbits(planetsByName["COM"], 1))

path1 = pathToCom(planetsByName["YOU"])
path2 = pathToCom(planetsByName["SAN"])

path1.reverse()
path2.reverse()

commonPathLen = len([True for nodeA, nodeB in zip(path1, path2) if nodeA == nodeB])
# non common path for path1 and path2 - 2 because the first orbit does not count
print("Step 2 : %d" % ((len(path1) - commonPathLen) + (len(path2) - commonPathLen) - 2))