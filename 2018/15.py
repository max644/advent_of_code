def getPuzzle():
    with open("15.txt", "r") as file:
        lines = file.readlines()
    puzzle = [list(line[:-1]) for line in lines]
    return puzzle

class Caracter:
    def __init__(self, line, col, case):
        self.line = line
        self.col = col
        self.hp = 200
        self.attack = 3
        self.type = case
        
    def __str__(self):
        return "[%s:%s] %s" % (self.line, self.col, self.type)
        
    def __eq__(self, other):
        return self.line == other.line and self.col == other.col

    def __lt__(self, other):
        if self.line == other.line:
            return self.col < other.col
        return self.line < other.line
    
class Game:
    def __init__(self, puzzle):
        self.map = [[case == "#" for case in line] for line in puzzle]
        self.caracters = [Caracter(lineIdx, colIdx, case) for lineIdx, line in enumerate(puzzle) for colIdx, case in enumerate(line) if case == "E" or case == "G"]
        print(self.caracters)
    
    def caractersByReadingOrder(self):
        return sorted(self.caracters)
    
    def playRound(self):
        for carac in self.caractersByReadingOrder():
            
    
    def printGame(self):
        caracHash = {"%s:%s" % (carac.line, carac.col):carac for carac in self.caracters}
        
        board = ""
        for lineIdx, line in enumerate(self.map):
            for colIdx, case in enumerate(line):
                if "%s:%s" % (lineIdx, colIdx) in caracHash:
                    board += caracHash["%s:%s" % (lineIdx, colIdx)].type
                else:
                    board += "#" if case else "."
            board += "\n"
        print(board)
                    
if __name__ == "__main__":
    puzzle = getPuzzle()
    game = Game(puzzle)
    game.printGame()
    game.playRound()