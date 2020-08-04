
SIDE = 300

class Grid:
	def __init__(self, grid_serial_number):
		self.grid_serial_number = grid_serial_number
		self.grid = []
		for line_idx in range(SIDE):
			self.grid.append([])
			for col_idx in range(SIDE):
				self.grid[line_idx].append(self.computePower(col_idx, line_idx))
				
	def computePower(self, x, y):
		rackId = x + 10
		ret = rackId * y
		ret += self.grid_serial_number
		ret *= rackId
		ret = (ret / 100) % 10
		return ret - 5

	def getSquarePower(self, x, y, side = 3):
		return sum([self.grid[y+delta_y][x+delta_x] for delta_y in range(side) for delta_x in range(side)])
		
	def findSquare(self, minSide = 3, maxSide = 3):
		if minSide == maxSide:
			return max([(self.getSquarePower(col_idx, line_idx, minSide), col_idx, line_idx) for line_idx in range(SIDE-minSide) for col_idx in range(SIDE-minSide)], key = lambda x:x[0])
		else:
			count = 0
			allSquares = {}
			for line_idx in range(SIDE):
				for col_idx in range(SIDE):
					firstSquarePower = self.getSquarePower(col_idx, line_idx, minSide)
					squares = [(minSide, firstSquarePower)]
					previousSquarePower = firstSquarePower
					#print str((line_idx, col_idx)) + " => " + str(min(min(maxSide, SIDE - line_idx), min(maxSide, SIDE - col_idx))) + " => " + str(range(minSide, min(min(maxSide, SIDE - line_idx), min(maxSide, SIDE - col_idx))))
					
					for side in range(minSide, min(min(maxSide, SIDE - line_idx), min(maxSide, SIDE - col_idx))):
						newColScore = sum([self.grid[idx][col_idx+side] for idx in range(line_idx, line_idx+side)])
						newLineScore = sum([self.grid[line_idx+side][idx] for idx in range(col_idx, col_idx+side+1)])
						#print str((line_idx, col_idx, side)) + " => " + str(newColScore) + " | " + str(newLineScore)
						previousSquarePower += newLineScore + newColScore
						squares.append((side+1, previousSquarePower))
					allSquares[(col_idx, line_idx)] = squares
				print len(allSquares)
			#print allSquares
			
			maxSquare = (-1, -1, -1, float("-Inf"))
			for (col_idx, line_idx), squares in allSquares.items():
				for side, power in squares:
					if power > maxSquare[3]:
						maxSquare = (col_idx, line_idx, side, power)
			
			return maxSquare
			
if __name__ == "__main__":
	
	with open("11.txt", "r") as file:
		grid_serial_number = int(file.read())
		
	grid = Grid(grid_serial_number)
	#grid.grid = [
	#	[1, 2, 3],
	#	[4, 5, 6],
	#	[7, 8, 9]
	#]
	
	#power, x, y = grid.findSquare()
	
	#print "#1 : " + str(grid.findSquare()[1:])
	#print "#2 : " + str(grid.findSquare(1, 300))
	print "#2 : " + str(grid.findSquare(1, 300))
	#print "#2 : " + str(grid.findSquare(16, 16))