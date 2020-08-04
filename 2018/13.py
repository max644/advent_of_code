from collections import Counter

HORIZONTAL = "-"
VERTICAL = "|"
CORNER_1 = "/"
CORNER_2 = "\\"
CORNER_TOP_LEFT = "CORNER_TOP_LEFT"
CORNER_TOP_RIGHT = "CORNER_TOP_RIGHT"
CORNER_BOTTOM_LEFT = "CORNER_BOTTOM_LEFT"
CORNER_BOTTOM_RIGHT = "CORNER_BOTTOM_RIGHT"
INTERSECTION = "+"
CART_UP = "^"
CART_DOWN = "v"
CART_RIGHT = ">"
CART_LEFT = "<"
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
CART_DIRECTION_TO_DIRECTION = {
	CART_UP : UP,
	CART_DOWN : DOWN,
	CART_RIGHT : RIGHT,
	CART_LEFT : LEFT
}
DIRECTION_TO_CART_DIRECTION = {
	UP : CART_UP,
	DOWN : CART_DOWN,
	RIGHT : CART_RIGHT,
	LEFT : CART_LEFT
}
DIRECTIONS = [UP, RIGHT, DOWN, LEFT]

TURN_LEFT = 0
TURN_STRAIGHT = 1
TURN_RIGHT = 2
TURNS = [-1, 0, +1]

SYMBOLS = {
	HORIZONTAL: HORIZONTAL,
	VERTICAL: VERTICAL,
	INTERSECTION: INTERSECTION,
	CORNER_TOP_LEFT: "/",
	CORNER_TOP_RIGHT: "\\",
	CORNER_BOTTOM_LEFT: "\\",
	CORNER_BOTTOM_RIGHT: "/"
}

class Cart:
	def __init__(self, x, y, cartDirection):
		self.x = x
		self.y = y
		self.direction = CART_DIRECTION_TO_DIRECTION[cartDirection]
		self.turnIdx = 0
		
	def turn(self):
		self.direction = (self.direction + TURNS[self.turnIdx % len(TURNS)]) % len(DIRECTIONS)
		self.turnIdx += 1
		
	def move(self):
		if self.direction == UP:
			self.y -= 1
		elif self.direction == DOWN:
			self.y += 1
		elif self.direction == LEFT:
			self.x -= 1
		elif self.direction == RIGHT:
			self.x += 1
			
	def __eq__(self, other):
		return self.y == other.y and self.x == other.x
		
	def __lt__(self, other):
		if self.y < other.y:
			return self.y < other.y
		return self.x < other.x


class Circuit:
	def __init__(self, lines):
		self.width = len(lines[0])
		self.height = len(lines)
		
		self.grid = {}
		self.carts = []
		
		for lineIdx, line in enumerate(lines):
			line = list(line)
			for colIdx, cell in enumerate(line):
				if cell in [HORIZONTAL, VERTICAL]:
					self.grid[(colIdx, lineIdx)] = cell
				elif cell == CORNER_1 and (colIdx-1 < len(line) and (line[colIdx-1] in [HORIZONTAL, INTERSECTION, CART_RIGHT, CART_LEFT])):
					self.grid[(colIdx, lineIdx)] = CORNER_TOP_LEFT
				elif cell == CORNER_1 and (colIdx+1 < len(line) and (line[colIdx+1] in [HORIZONTAL, INTERSECTION, CART_RIGHT, CART_LEFT])):
					self.grid[(colIdx, lineIdx)] = CORNER_BOTTOM_RIGHT
				elif cell == CORNER_2 and (colIdx-1 < len(line) and (line[colIdx-1] in [HORIZONTAL, INTERSECTION, CART_RIGHT, CART_LEFT])):
					self.grid[(colIdx, lineIdx)] = CORNER_BOTTOM_LEFT
				elif cell == CORNER_2 and (colIdx+1 < len(line) and (line[colIdx+1] in [HORIZONTAL, INTERSECTION, CART_RIGHT, CART_LEFT])):
					self.grid[(colIdx, lineIdx)] = CORNER_TOP_RIGHT
				elif cell == INTERSECTION:
					self.grid[(colIdx, lineIdx)] = cell
				elif cell in [CART_UP, CART_DOWN, CART_RIGHT, CART_LEFT]:
					if cell in [CART_UP, CART_DOWN]:
						self.grid[(colIdx, lineIdx)] = VERTICAL
					else:
						self.grid[(colIdx, lineIdx)] = HORIZONTAL
					self.carts.append(Cart(colIdx, lineIdx, cell))
					
	def move(self):
		for cart in sorted(self.carts):
			cell = self.grid[(cart.x, cart.y)]
			if cell == INTERSECTION:
				cart.turn()
			elif cell == CORNER_TOP_LEFT:
				if cart.direction == DOWN:
					cart.direction = LEFT
				else:
					cart.direction = UP
			elif cell == CORNER_TOP_RIGHT:
				if cart.direction == DOWN:
					cart.direction = RIGHT
				else:
					cart.direction = UP
			elif cell == CORNER_BOTTOM_LEFT:
				if cart.direction == UP:
					cart.direction = LEFT
				else:
					cart.direction = DOWN
			elif cell == CORNER_BOTTOM_RIGHT:
				if cart.direction == UP:
					cart.direction = RIGHT
				else:
					cart.direction = DOWN
			cart.move()
			self.detectCollision()
			
	def detectCollision(self):
		positions = [(cart.x, cart.y) for cart in self.carts]
		positionsCount = Counter(positions)
		for position, count in positionsCount.items():
			if count > 1:
				print "COLLISION AT POSITION : " + str(position)
				
			
	def __str__(self):
		grid = []
		for lineIdx in range(self.height):
			grid.append([])
			for colIdx in range(self.width):
				grid[lineIdx].append(" ")
		
		for (x, y), cell in self.grid.items():
			grid[y][x] = SYMBOLS[cell]
		
		for cart in self.carts:
			grid[cart.y][cart.x] = DIRECTION_TO_CART_DIRECTION[cart.direction]
		
		ret = ""
		for lineIdx in range(self.height):
			ret += str(lineIdx) + "\t" + "".join(grid[lineIdx]) + "\n"
		
		return ret
		
if __name__ == "__main__":
	with open("13.txt", "r") as file:
		lines = file.readlines()
	
	lines = [line[:-1] for line in lines]
	
	circuit = Circuit(lines)
	
	#print circuit
	for idx in range(500):
		circuit.move()
		#print "-- iteration " + str(idx) + " --"
		#print circuit
		circuit.detectCollision()