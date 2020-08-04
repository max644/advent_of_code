
def countValidTriangle(triangles):
	trianglecount = 0
	for triangle in triangles:
		a, b, c = triangle
		a = int(a)
		b = int(b)
		c = int(c)
		if a+b>c and a+c>b and b+c>a:
			trianglecount += 1
	return trianglecount

with open("input.txt", "r") as f:
	lines = f.readlines()
	lines = [l[:-1] for l in lines]
	
	triangles = []
	for line in lines:
		elements = line.split(" ")
		elements = [element for element in elements if element != ""]
		triangles.append(elements)
	print countValidTriangle(triangles)
	
	
	triangles2 = []
	for i in range(0, len(triangles), 3):
		l0 = (triangles[i+0][0], triangles[i+1][0], triangles[i+2][0])
		l1 = (triangles[i+0][1], triangles[i+1][1], triangles[i+2][1])
		l2 = (triangles[i+0][2], triangles[i+1][2], triangles[i+2][2])
		triangles2.append(l0)
		triangles2.append(l1)
		triangles2.append(l2)
	print countValidTriangle(triangles2)