from program import Program

with open("17.txt", "r") as file:
    code = file.read()

code = [int(opcode) for opcode in code.split(",")]

program = Program(code, [])


def getView():
    out = ""
    while True:
        ret = program.run()
        if ret == None:
            return out
        out += chr(ret)

def detectIntersect(view, lineIdx, colIdx):
    if lineIdx == 0 or lineIdx >= len(view) - 1 or colIdx == 0 or colIdx >= len(view[0]) - 1:
        return False
    if view[lineIdx][colIdx] == "#" and view[lineIdx-1][colIdx] == "#" and view[lineIdx+1][colIdx] == "#" and view[lineIdx][colIdx-1] == "#" and view[lineIdx][colIdx+1] == "#":
        return True
    return False

def detectAllIntersect(view):
    cnt = 0
    for lineIdx, line in enumerate(view):
        for colIdx, point in enumerate(line):
            if detectIntersect(view, lineIdx, colIdx):
                cnt += lineIdx * colIdx
    return cnt
        
 
view = getView()
print(view)

view = [[point for point in line] for line in view.split("\n")]

view = [line for line in view if len(line) > 0]

print("Step 1 : %d" % detectAllIntersect(view))