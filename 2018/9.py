import re
from collections import deque

def solve(nbPlayers, lastMarbleValue):
	game = deque()
	game.append(0)
	players = [0] * nbPlayers
	for marbleValue in range(1, lastMarbleValue+1):
		if marbleValue % 23 == 0:
			game.rotate(7)
			players[(marbleValue-1)%len(players)] += game.pop() + marbleValue
			game.rotate(-1)
		else:
			game.rotate(-1)
			game.append(marbleValue)
	return max(players)

if __name__ == "__main__":
	with open("9.txt", "r") as file:
		content = file.read()
	
	m = re.match(r"(\d+) players; last marble is worth (\d+) points", content)
	nbPlayers = int(m.group(1))
	lastMarbleValue = int(m.group(2))
	
	print str(nbPlayers) + " players, last marble value : " + str(lastMarbleValue) + " => " + str(solve(nbPlayers, lastMarbleValue))
	print str(nbPlayers) + " players, last marble value : " + str(lastMarbleValue*100) + " => " + str(solve(nbPlayers, lastMarbleValue*100))