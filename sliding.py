__author__ = 'basanta.kharel'

import random
from collections import deque
from heapq import heappush, heappop
import time
import sys

#Class
#State
#   w is width of the grid
#   h is height
#   slideMatrix is the 2D grid
#   display()
#       prints the state
#   clone()
#       returns a clone of the state
#   isSolved() checks if the state is solved or not
#   swappieces(x,y) swaps value x and y in the grid
#   normalize() normalizes the state

#functions
#compare(state,state) returns True if states are identical
#loadfile(file) returns a state that contains the grid specification from the file
#getbox(state, piece) gives the top-right position and bottom-left position of the piece
#applymove(state, move) move has to be valid. It modifies the state with the proper move
#applymovecloning(state, move) returns a new state after applying the move. state remains the same
#randomWalks(state, N) given a state it applies a valid move randomly until reaching a goal state or for N tries

def main():
    #print "Sliding Puzzle \n"
    #files = ["SBP-bricks-level2", "SBP-bricks-level3", "SBP-bricks-level4", "SBP-bricks-level5", "SBP-bricks-level6", "SBP-bricks-level7"]
    # state = loadfile(files[1])
    # print files[1]
    # BFS(state)


    #for file in files:
        #state = loadfile(file + ".txt")
    if not len(sys.argv) > 1:
        return
    file = sys.argv[1]
    #file = "SBP-bricks-level7.txt"
    state = loadfile(file)
    print file
    global winbox
    winbox = getWinBox(state)

    # tup = tuple()
    # for l in state.slideMatrix:
    #     tup += tuple(l)
    # print tup
    # print state.slideMatrix
    aStar(state)
        #manhattanDist(state)
        #print getWinBox(state)
        #state.display()




class State():
    w = 0
    h = 0
    slideMatrix = []
    parent = None
    action = []
    gCost = 0

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.slideMatrix = []
        self.action = []
        self.parent = None
        self.gCost = 0

    def __hash__(self):
        tup = tuple()
        for l in self.slideMatrix:
            tup += tuple(l)
        return hash( tup )

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def display(self):
        print str(self.w) + "," + str(self.h) + ","
        for rows in self.slideMatrix:
            print ','.join(map(str, rows)) + ','

    def clone(self):
        cloned = State(self.w, self.h)
        rows = []
        for row in self.slideMatrix:
            rows.append(list(row))
        cloned.slideMatrix = list(rows)
        cloned.gCost = self.gCost
        return cloned

    def isSolved(self):
        for rows in self.slideMatrix:
            for i in rows:
                if i == -1:
                    return False
        return True

    def swappieces(self, p1, p2):
        for i in range(self.h):
            for j in range(self.w):
                if self.slideMatrix[i][j] == p1:
                    self.slideMatrix[i][j] = p2
                elif self.slideMatrix[i][j] == p2:
                    self.slideMatrix[i][j] = p1
    def normalize(self):
        currPiece = 3
        for i in range(self.h):
            for j in range(self.w):
                if self.slideMatrix[i][j] == currPiece:
                    currPiece += 1
                elif self.slideMatrix[i][j] > currPiece:
                    self.swappieces(currPiece, self.slideMatrix[i][j])
                    currPiece += 1


#assumes states are normalized
def compare(state, state2):
    if state.w != state2.w:
        return False
    if state.h != state2.h:
        return False
    for i in range(state.h):
        for j in range(state.w):
            if state.slideMatrix[i][j] != state2.slideMatrix[i][j]:
                return False
    return True

def loadfile(filename):
    file = open(filename, 'r')
    line1 = file.readline().rstrip('\n,')
    params = line1.split(',')
    state = State(int(params[0]), int(params[1]))
    lines = file.readlines()
    file.close()
    global pieces
    pieces = [0, 1, -1]
    for i in range(state.h):
        row = lines[i].rstrip('\n,').split(',')
        rowInt = []
        for j in range(state.w):
            value = int(row[j])
            if value not in pieces:
                pieces.append(value)
            rowInt.append(value)
        state.slideMatrix.append(rowInt)
    pieces.remove(0)
    pieces.remove(1)
    pieces.remove(-1)
    return state

def getbox(state, piece):
    box = []
    for i in range(state.h):
        for j in range(state.w):
            if state.slideMatrix[i][j] == piece:
                box.append([i,j])
    if not box:
        return []
    #gives the bounding box of the piece top-right corner and bottom-left corner
    box = [box[0], box.pop()]
    return list(box)

def movelist(state, piece):
    #find boundaries
    if (piece == 1 or piece == 0 or piece == -1):
        print "doomsday machine is deployed"
        return []

    box = getbox(state, piece)

    width = box[1][1] - box[0][1] + 1
    height = box[1][0] - box[0][0] + 1
    x = box[0][0]
    y = box[0][1]
    #check up
    up = True
    xstart = x - 1 # can move only one cell at a time
    ystart = y
    if xstart < 0: #illegal position
        up = False
    else:
        for i in range(width):
            object = state.slideMatrix[xstart][ystart+i]
            if piece != 2 and object!= 0 :
                up = False
            elif piece == 2 and (object != 0 and object != -1) :
                up = False

    #check down
    down = True
    xstart = x + height
    ystart = y
    if xstart >= state.h: #again illegal
        down = False
    else:
        for i in range(width):
            object = state.slideMatrix[xstart][ystart+i]
            if piece != 2 and object!= 0 :
                down = False
            elif piece == 2 and (object != 0 and object != -1) :
                down = False

    #check left
    xstart = x
    ystart = y - 1

    left = True
    if ystart < 0 :
        left = False
    else:
        for i in range(height):
            object = state.slideMatrix[xstart+i][ystart]
            if piece != 2 and object!= 0 :
                left = False
            elif piece == 2 and (object != 0 and object != -1) :
                left = False

    #check right
    xstart = x
    ystart = y + width
    right = True
    if y >= state.w:
        right = False
    else:
        for i in range(height):
            object = state.slideMatrix[xstart+i][ystart]
            if piece != 2 and object!= 0 :
                right = False
            elif piece == 2 and (object != 0 and object != -1) :
                right = False
    thelist = []
    if up:
        thelist.append([piece, "u"])
    if down:
        thelist.append([piece, "d"])
    if right:
        thelist.append([piece, "r"])
    if left:
        thelist.append([piece, "l"])
    return thelist

def allmovelist(state):
    thelist = []
    global pieces
    for piece in pieces:
        thelist = list(thelist + movelist(state, piece))
    return thelist

def applymove(state, move):
    #moves are all legal so no need to check again
    piece = move[0]
    box = getbox(state, piece)

    width = box[1][1] - box[0][1] + 1
    height = box[1][0] - box[0][0] + 1
    x = box[0][0]
    y = box[0][1]

    direction = move[1]

    if direction == "u":
        #swap top layer to one above
        top = []
        for k in range(width):
            val = state.slideMatrix[x-1][y+k]
            if val == -1:
                val = 0
            top.append(val)
        #print top
        for i in range(height):
            for j in range(width):
                state.slideMatrix[x-1+i][y+j] = state.slideMatrix[x+i][y+j]
        for k in range(width):
            state.slideMatrix[x+height-1][y+k] = top[k]

    if direction == "d":
        #swap bottom layer to one below
        bottom = []
        for k in range(width):
            val = state.slideMatrix[x+height][y+k]
            if val == -1:
                val = 0
            bottom.append(val)
        for i in reversed(range(height)):
            for j in range(width):
                state.slideMatrix[x+i+1][y+j] = state.slideMatrix[x+i][y+j]
        for k in range(width):
            state.slideMatrix[x][y+k] = bottom[k]

    if direction == "l":
        #swap left layer to one left
        left = []
        for k in range(height):
            val = state.slideMatrix[x+k][y-1]
            if val == -1:
                val = 0
            left.append(val)
        for i in range(height):
            for j in range(width):
                state.slideMatrix[x+i][y-1+j] = state.slideMatrix[x+i][y+j]
        for k in range(height):
            state.slideMatrix[x+k][y+width-1] = left[k]

    if direction == "r":
        #swap left layer to one left
        right = []
        for k in range(height):
            val = state.slideMatrix[x+k][y+width]
            if val == -1:
                val = 0
            right.append(val)
        for i in range(height):
            for j in reversed(range(width)):
                state.slideMatrix[x+i][y+j+1] = state.slideMatrix[x+i][y+j]
        for k in range(height):
            state.slideMatrix[x+k][y] = right[k]

def applymovecloning(state, move):
    newstate = state.clone()
    applymove(newstate, move)
    newstate.action = move
    newstate.parent = state
    #increase
    newstate.gCost += 1
    return newstate


def addtoClosedList(list, state):
    normState = state.clone()
    normState.normalize()
    list.add(normState)

def getWinBox(state):
    winbox = getbox(state, -1)
    width = winbox[1][1] - winbox[0][1] + 1
    height = winbox[1][0] - winbox[0][0] + 1

    if winbox[0][0] == 0:
        return ['top', list(winbox)]
    elif winbox[0][0] == state.h -1:
        return ['bottom', list(winbox)]
    elif winbox[0][1] == 0:
        return ['left', list(winbox)]
    elif winbox[0][0] == state.w -1:
        return ['right', list(winbox)]
    else:
        print "something is wrong here"


def manhattanDist(state):
    #get the box of 2
    piecebox = getbox(state, 2)

    global winbox

    length = 0
    width  = 0
    if winbox[0] == "top" or winbox[0] == "left":
        width = abs(piecebox[0][1] - winbox[1][0][1])
        length = abs(piecebox[0][0] - winbox[1][0][0])
        #print length , width, length+width
    elif winbox[0] == "bottom" or winbox[0] == "right":
        width = abs(piecebox[1][1] - winbox[1][1][1])
        length = abs(piecebox[1][0] - winbox[1][1][0])
        #print length , width, length+width

    return length + width

def aStar(initState):
    start = time.time()
    closed = set()
    open = []
    cost = initState.gCost + manhattanDist(initState)
    heappush(open, (cost, initState))
    addtoClosedList(closed, initState)

    while open:
        state = heappop(open)[1]
        if state.isSolved():
            end = time.time()
            printSolution(state)
            print "Nodes Explored  :", len(closed)
            print "Time            :", end - start, "seconds"
            return

        #addtoClosedList(closed, state)

        moves = allmovelist(state)
        for move in moves:
            child = applymovecloning(state, move)
            if not containsInClosed(closed, child):
                addtoClosedList(closed, child)
                cost = child.gCost + manhattanDist(child)
                heappush(open, (cost, child))

    end = time.time()
    print "No Solution"
    print "Nodes Explored :", len(closed)
    print "Time           :", end - start


def containsInClosed(list, state):
    #assumes that the list is normalized
    stateNorm = state.clone()
    stateNorm.normalize()
    if stateNorm in list:
        return True
    else:
        return False


def printSolution(state):
    seq = []
    solved = state.clone()
    while(state.parent != None):
        seq.append(state.action)
        state = state.parent
    length = len(seq)
    while seq:
        print seq.pop()
    solved.display()
    print "Solution Length :", length

    return


if __name__ == '__main__':
    main()
