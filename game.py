import constants
import sys, pygame
from pygame.locals import *
from bitmapfont import BitmapFont

blackNeighbors = [(0, 1), (-1, 1), (1, 1)]

class Cell:
    def __init__(self):
        self.towerColor = constants.EMPTY
        self.towerSide = constants.NONE


class Board:
    def __init__(self):
        self.arr = []
        self.currentPlayer = constants.pwhite
        self.activecolor = constants.EMPTY
        self.turns = 0
        self.skip = 0
        self.parent = None
        for i in range(8):
            arr = []
            for j in range(8):
                cell = Cell()
                if i == 0:
                    cell.towerSide = constants.pblack
                    cell.towerColor = constants.COLORMAP[i][j]
                elif i == 7:
                    cell.towerSide = constants.pwhite
                    cell.towerColor = constants.COLORMAP[i][j]          
                arr.append(cell)
            self.arr.append(arr)

    def expand(self, x, y):
        cell = self.arr[y][x]
        validMoves = []
        for i, j in blackNeighbors:
            
            if cell.towerSide == constants.pwhite:
                j *= -1
            startX = x + i
            startY = y + j
            while startY < 8 and startY >= 0 and startX < 8 and startX >= 0:       
                
                if self.arr[startY][startX].towerColor != constants.EMPTY:
                    break
                validMoves.append((startX, startY))
                startX += i
                startY += j
                
        return validMoves

    def checkWin(self):
        winPlayer = constants.NONE
        if self.skip == 2:
            if self.currentPlayer == constants.pblack:
                winPlayer = constants.pwhite
            else:
                winPlayer = constants.pblack
        else:
            for x in range(8):
                if self.arr[0][x].towerSide == constants.pwhite:
                    winPlayer = constants.pwhite
                    break
                if self.arr[7][x].towerSide == constants.pblack:
                    winPlayer = constants.pblack
                    break
            

        return winPlayer

    def moves(self, cellX, cellY, targetX, targetY):
        
        if (targetX, targetY) not in self.expand(cellX, cellY):
            return False

        startCell = self.arr[cellY][cellX]
        targetCell = self.arr[targetY][targetX]
        
        targetCell.towerColor = startCell.towerColor
        targetCell.towerSide = startCell.towerSide
        startCell.towerColor = constants.EMPTY
        startCell.towerSide = constants.NONE

        self.activecolor = constants.COLORMAP[targetY][targetX]

        self.currentPlayer = constants.pwhite if self.currentPlayer == constants.pblack else constants.pblack
        self.turns += 1
        self.skip = 0

    def canMove(self, x, y):
        cell = self.arr[y][x]
        if self.turns == 0 and cell.towerSide == self.currentPlayer:
            return True
        return cell.towerColor == self.activecolor and cell.towerSide == self.currentPlayer

    def skipMove(self):
        for i in range(8):
            for j in range(8):
                if self.arr[i][j].towerColor == self.activecolor and self.arr[i][j].towerSide == self.currentPlayer:
                    x = j
                    y = i

        validMoves = self.expand(x, y)
        if len(validMoves) == 0:
            self.turns += 1
            self.currentPlayer = constants.pwhite if self.currentPlayer == constants.pblack else constants.pblack
            self.activecolor = constants.COLORMAP[y][x]
            self.skip += 1
            return True
        else:
            return False
        
        


class GameState: 
    def __init__(self, runner):
        self.runner = runner
    
    def on_enter(self, prev_state):
        pass

    def on_exit(self):
        pass

    def update(self, deltatime):
        pass

    def draw(self, surface):
        pass


    
class Runner:
    def __init__(self, name, width, height):
        self.name = name
        self.width = width
        self.height = height
        pygame.init()
        pygame.display.set_caption(self.name)
        self.WINDOWS = pygame.display.set_mode((self.width, self.height))
        self.fpsClock = pygame.time.Clock()
        self.font = BitmapFont("assets/fasttracker2-style_12x12.png", 12, 12)
        self.BLACK = pygame.Color(0,0,0)
        self.state = None
        self.mouseClick = None
    
    def change_state(self, newState):
        if self.state is not None:
            self.state.on_exit()

        if newState is None:
            pygame.quit()
            sys.exit()
        else:
            newState.on_enter(self.state)
            self.state = newState
    
    def run(self, initialState):
        self.change_state(initialState)

        while True:
            self.mouseClick = None
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                elif event.type == MOUSEBUTTONUP:
                    self.mouseClick = event.pos

            self.state.update(self.fpsClock.get_time())
            self.WINDOWS.fill(self.BLACK)
            self.state.draw(self.WINDOWS)
        
            pygame.display.update()
            self.fpsClock.tick(60)


if __name__ == '__main__':
    board = Board()
    print(board.expand(1, 7))

    
    
                
        

            
            





