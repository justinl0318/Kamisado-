import sys, pygame, time
from game import GameState, Runner, Board
import solver
from pygame.locals import *
import constants


class MainMenu(GameState):
    def __init__(self, runner, nextState):
        super().__init__(runner)
        self.nextState = nextState
        self.arr = ["START", "EXIT"]
        self.currentSelection = 0
        self.delayTime = 200

    def update(self, deltatime):
        keys = pygame.key.get_pressed()
        if self.delayTime > 0:
            self.delayTime -= deltatime
        else:
            if keys[K_UP]:
                self.currentSelection = 0
                self.delayTime = 200
            elif keys[K_DOWN]:
                self.currentSelection = 1
                self.delayTime = 200

            elif keys[K_SPACE]:
                if self.currentSelection == 0:
                    self.runner.change_state(self.nextState)
                    self.delayTime = 200

                else:
                    self.runner.change_state(None)
                    self.delayTime = 200

        if self.delayTime < 0:
            self.delayTime = 0

    def draw(self, surface):
        self.runner.font.centre(surface, "Kamisado", self.runner.height * 0.3)
        for i, j in enumerate(self.arr):
            if i == self.currentSelection:
                msg = ">" + j + "<"
            else:
                msg = j
            self.runner.font.centre(surface, msg, self.runner.height * 0.5 + 18 * i)


class OptionMenu(GameState):
    def __init__(self, runner, mainmenuState, InGameState):
        super().__init__(runner)
        self.mainmenuState = mainmenuState
        self.nextState = InGameState
        self.p1UseSolver = "Human"
        self.p2UseSolver = "Human"
        self.playerUseAI = 0
        self.depth = 3
        self.arr = ["Start", "P1: "+self.p1UseSolver, "P2: "+self.p2UseSolver, "Depth: "+str(self.depth), "Return"]    
        self.currentSelection = 0
        self.delayTime = 200

    def on_enter(self, mainmenuState):
        self.currentSelection = 0
        self.p1UseSolver = "Human"
        self.p2UseSolver = "Human"
        self.playerUseAI = 0
        self.depth = 3
        self.arr = ["Start", "P1: "+self.p1UseSolver, "P2: "+self.p2UseSolver, "Depth: "+str(self.depth), "Return"]    

    def update(self, deltatime):
        keys = pygame.key.get_pressed()
        if self.delayTime > 0:
            self.delayTime -= deltatime

        else:

            if keys[K_UP] and self.currentSelection > 0:
                self.currentSelection -= 1
                self.delayTime = 200
            elif keys[K_DOWN] and self.currentSelection < 3:
                self.currentSelection += 1
                self.delayTime = 200
            elif keys[K_RIGHT] and self.currentSelection == 1:
                self.p1UseSolver = "Computer"
                self.arr[1] = "P1: "+self.p1UseSolver
                self.delayTime = 200
            elif keys[K_LEFT] and self.currentSelection == 1:
                self.p1UseSolver = "Human"
                self.arr[1] = "P1: "+self.p1UseSolver
                self.delayTime = 200
            elif keys[K_RIGHT] and self.currentSelection == 2:
                self.p2UseSolver = "Computer"
                self.arr[2] = "P2: "+self.p2UseSolver
                self.delayTime = 200
            elif keys[K_LEFT] and self.currentSelection == 2:
                self.p2UseSolver = "Human"
                self.arr[2] = "P2: "+self.p2UseSolver
                self.delayTime = 200     
            elif keys[K_RIGHT] and self.currentSelection == 3:
                self.depth += 1
                self.arr[3] = "Depth: "+str(self.depth)
                self.delayTime = 200
            elif keys[K_LEFT] and self.currentSelection == 3 and self.depth > 1:
                self.depth -= 1
                self.arr[3] = "Depth: "+str(self.depth)
                self.delayTime = 200 
            elif keys[K_SPACE]:
                if self.currentSelection == 0:
                    self.runner.change_state(self.nextState)
                    self.delayTime = 200
                elif self.currentSelection == 4:
                    self.runner.change_state(self.mainmenuState)
                    self.delayTime = 200

        if self.delayTime < 0:
            self.delayTime = 0

        if self.p1UseSolver == "Computer" and self.p2UseSolver != "Computer":
            self.playerUseAI = 1
        elif self.p2UseSolver == "Computer" and self.p1UseSolver != "Computer":
            self.playerUseAI = 2
        elif self.p2UseSolver == "Computer" and self.p2UseSolver == "Computer":
            self.playerUseAI = -1

    def draw(self, surface):
        self.runner.font.centre(surface, "Setup", self.runner.height * 0.3)
        for i, j in enumerate(self.arr):
            if i == self.currentSelection:
                msg = ">" + j + "<"
            else:
                msg = j
            self.runner.font.centre(surface, msg, self.runner.height * 0.5 + 25 * i)

class InGameState(GameState):
    def __init__(self, runner, mainmenuState):
        super().__init__(runner)
        self.mainmenuState = mainmenuState
        self.towersImage = [[], []]
        self.validImage = pygame.image.load("assets/valid.png")
        for i in range(8):
            self.towersImage[0].append(pygame.image.load("assets/1-{}.png".format(i+1)))
            self.towersImage[1].append(pygame.image.load("assets/2-{}.png".format(i+1)))
        
        
            
    def on_enter(self, optionmenu):
        self.board = Board()
        self.currentCell = None
        self.gameOver = False
        self.frame_count = 0
        self.startTimer = False
        self.winPlayer = 0
        self.depth = optionmenu.depth
        print(self.depth)
        self.playerUseAI = optionmenu.playerUseAI
        self.AI = solver.NegamaxAI(4)
        #print(self.playerUseAI)
        self.delayTime = 70

    def update(self, deltatime):
        if not self.gameOver and self.runner.mouseClick:
            self.startTimer = True
            x, y = self.runner.mouseClick
            i = (x - 20)// 75
            j = (y - 160)// 75
            if i >= 0 and i <= 7 and j >= 0 and j <= 7:
                cell = self.board.arr[j][i]
                #print(i, j)
                flag = False
                if self.currentCell:
                    if self.currentCell[0] == i and self.currentCell[1] == j:
                        self.currentCell = None
                    else:
                        validMoves = self.board.expand(self.currentCell[0], self.currentCell[1])
                        for x, y in validMoves:
                            if i == x and j == y:
                                flag = True
                else:
                    if cell.towerSide == self.board.currentPlayer:
                        if self.board.turns == 0 or cell.towerColor == self.board.activecolor:
                            self.currentCell = (i, j)

                if flag:
                    self.board.moves(self.currentCell[0], self.currentCell[1], i, j)
                    self.currentCell = None
                    if self.board.checkWin() != constants.NONE:
                        self.gameOver = True
                        self.winPlayer = self.board.checkWin()
                    else:
                        if self.board.skipMove():
                            self.board.skipMove()
                            if self.board.checkWin() != constants.NONE:
                                self.gameOver = True

        #AI, p1 Use AI or p2 Use AI
        elif not self.gameOver and self.playerUseAI > 0:
            if self.board.currentPlayer == self.playerUseAI:
                targetMove = self.AI.run(self.board)
                if targetMove:
                    x, y, i, j, node = targetMove
                    self.board.moves(x, y, i, j)
                    self.currentCell = None
                    if self.board.checkWin() != constants.NONE:
                        self.gameOver = True
                        self.winPlayer = self.board.checkWin()
                    else:
                        if self.board.skipMove():
                            self.board.skipMove()
                            if self.board.checkWin() != constants.NONE:
                                self.gameOver = True

                else:
                    if self.board.skipMove():
                        self.board.skipMove()
                        if self.board.checkWin() != constants.NONE:
                            self.gameOver = True

        #both player use AI
        if self.delayTime > 0:
            self.delayTime -= 1
        
        else:
            if not self.gameOver and self.playerUseAI == -1:
                targetMove = self.AI.run(self.board)
                if targetMove:
                    x, y, i, j, node = targetMove
                    self.board.moves(x, y, i, j)
                    self.delayTime = 70
                    self.currentCell = None
                    if self.board.checkWin() != constants.NONE:
                        self.gameOver = True
                        self.winPlayer = self.board.checkWin()
                    else:
                        if self.board.skipMove():
                            self.board.skipMove()
                            if self.board.checkWin() != constants.NONE:
                                self.gameOver = True

                else:
                    if self.board.skipMove():
                        self.board.skipMove()
                        if self.board.checkWin() != constants.NONE:
                            self.gameOver = True
        
        #esc button
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            self.runner.change_state(self.mainmenuState)

    def draw(self, surface):

        #timer
        if self.startTimer:
            totalSeconds = self.frame_count // 60
            minutes = totalSeconds //60
            seconds = totalSeconds % 60
            hours = minutes // 60
            if self.winPlayer == 0:
                self.frame_count += 1
            time = "{}:{}:{}".format(str(hours).zfill(2), str(minutes).zfill(2), str(seconds).zfill(2))
        else:
            time = "{}:{}:{}".format(str(0).zfill(2), str(0).zfill(2), str(0).zfill(2))


        self.runner.font.draw(surface, "Player: " + constants.PLAYER_NAMES[self.board.currentPlayer], self.runner.width * 0.04, self.runner.height * 0.04)
        self.runner.font.draw(surface, "Color: " + constants.COLOR_NAMES[self.board.activecolor], self.runner.width * 0.04, self.runner.height * 0.07)
        self.runner.font.draw(surface, time, self.runner.width * 0.81, self.runner.height * 0.04)
        self.runner.font.draw(surface, str(self.board.turns).zfill(2), self.runner.width * 0.92, self.runner.height * 0.07)
        if self.winPlayer > 0:
            self.runner.font.centre(surface, "P{} Wins!".format(self.winPlayer), self.runner.height * 0.12)
        for i in range(8):
            for j in range(8):
                x, y = j * 75 + 20, i * 75 + 160
                rect = Rect(x, y, 75, 75)
                pygame.draw.rect(surface, constants.COLOR_RGB[constants.COLORMAP[i][j]], rect)
        if self.currentCell is not None:
            validMoves = self.board.expand(self.currentCell[0], self.currentCell[1])
            #print(validMoves)
            for x, y in validMoves:
                surface.blit(self.validImage, (x * 75 + 15, y * 75 + 155, 75, 75))
        for j in range(8):
            for x in range(8):
                if self.board.arr[j][x].towerColor != constants.EMPTY:
                    color = self.board.arr[j][x].towerColor - 1
                    side = self.board.arr[j][x].towerSide - 1
                    tower = self.towersImage[side][color]
                    surface.blit(tower, (x * 75 + 25, j * 75 + 150, 75, 75))
                    

            





if __name__ == '__main__':
    runner = Runner("KamiSado", 640, 780)
    mainmenu = MainMenu(runner, None)
    optionmenu = OptionMenu(runner, mainmenu, None)
    ingamemenu = InGameState(runner, mainmenu)
    mainmenu.nextState = optionmenu
    optionmenu.nextState = ingamemenu
    runner.run(mainmenu)