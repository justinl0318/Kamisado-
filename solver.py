import pickle
from game import Board
import constants
import sys

selected = None

def deepcopy(obj):
    return pickle.loads(pickle.dumps(obj))

def generateSuccessor(board: Board):
    result = []
    
    activeTower = getActiveTower(board)
    if board.checkWin() > 0:
        return []
    for x, y in activeTower:
        availableMoves = board.expand(x, y)
        for i, j in availableMoves:
            board2 = deepcopy(board)
            board2.moves(x, y, i, j)
            board2.parent = board
            result.append((x, y, i, j, board2))

    return result


def getActiveTower(board: Board):
    playerSide = board.currentPlayer
    activeColor = board.activecolor
    result = []
    for i in range(8):
        for j in range(8):
            if board.arr[i][j].towerSide == playerSide:
                if board.turns == 0:
                    result.append((j, i))
                elif board.arr[i][j].towerColor == activeColor:
                    result.append((j, i))
                    break

    return result

def getAllTowers(board: Board):
    result = []
    for i in range(8):
        for j in range(8):
            if board.arr[i][j].towerSide != constants.NONE:
                result.append((i, j, board.arr[i][j].towerSide))

    return result

def heuristic(board: Board, side):

    checkWin = board.checkWin()
    if checkWin != constants.NONE:
        if checkWin == side:
            return sys.maxsize - 1
        else:
            return -sys.maxsize + 1

    allTowers = getAllTowers(board)
    score = 0
    for y, x, towerSide in allTowers:
        if towerSide == constants.pwhite:
            score += (7-y) * 2
            if blocked(board, x, y, towerSide):
                score -= 10

        elif towerSide == constants.pblack:
            score -= y * 2
            if blocked(board, x, y, towerSide):
                score += 10
        
    if side == constants.pblack:
        score = -score
    return score

def heuristic3(board: Board, side):

    checkWin = board.checkWin()
    if checkWin != constants.NONE:
        if checkWin == side:
            return sys.maxsize - 1
        else:
            return -sys.maxsize + 1

    allTowers = getAllTowers(board)
    score = 0
    for y, x, towerSide in allTowers:
        if towerSide == constants.pwhite:
            score += (7-y) * 2
            if blocked(board, x, y, towerSide):
                score -= 10

        elif towerSide == constants.pblack:
            score -= y * 2
            if blocked(board, x, y, towerSide):
                score += 50
        
    if side == constants.pblack:
        score = -score
    return score

def heuristic2(board: Board, side):

    checkWin = board.checkWin()
    if checkWin != constants.NONE:
        if checkWin == side:
            return 99999
        else:
            return -99999

    allTowers = getAllTowers(board)
    score = 0
    for y, x, towerSide in allTowers:
        if towerSide == constants.pwhite and towerSide == side:
            score += (7-y) * 2
            if blocked(board, x, y, towerSide):
                score -= 3
                
        elif towerSide == constants.pblack and towerSide == side:
            score += y * 2
            if blocked(board, x, y, towerSide):
                score -= 3
        
   #if side == constants.pblack:
        #score = -score
    return score

def blocked(board: Board, x, y, side):
    if side == constants.pwhite:
        blocked = False
        while y > 0:
            y -= 1
            if board.arr[y][x].towerColor != constants.EMPTY:
                blocked = True      
        return blocked

    elif side == constants.pblack:
        blocked = False
        while y < 7:
            y += 1
            if board.arr[y][x].towerColor != constants.EMPTY:
                blocked = True
        return blocked


class NegamaxAI:
    def __init__(self, depth=3):
        self.selected = None
        self.depth = depth
        #print(self.depth)

    def run(self, board: Board):
        self.selected = None
        self.negamax(board, self.depth, board.currentPlayer, -sys.maxsize, sys.maxsize)
        return self.selected

    def negamax(self, board: Board, depth, side, alpha, beta, color=1):
        if depth == 0 or board.checkWin() > constants.NONE:
            result = color * heuristic3(board, side)
            #print(depth, color, result)
            return result
        
        childNodes = generateSuccessor(board)
        for x, y, i, j, node in childNodes:
            prev = alpha
            nega = -self.negamax(node, depth-1, side, -beta, -alpha, -color)
            #print(">", alpha, end=" ")
            alpha = max(alpha, nega)
            #print(alpha, nega)
            if board.parent is None and prev != alpha:
                self.selected = (x, y, i, j, node)

            if alpha >= beta:
                break
        return alpha


        
    







                    
        



