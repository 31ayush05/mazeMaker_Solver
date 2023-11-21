import tkinter as tk
import random

def getPossiblePaths(cell, visited, mX, mY):
    nebors = ""
    # L
    if (cell[0] > 0) and (cell[0] <= (mX - 1)):
        if [cell[0]-1, cell[1]] not in visited:
            nebors += "l"
    # R
    if (cell[0] >= 0) and (cell[0] < (mX - 1)):
        if [cell[0]+1, cell[1]] not in visited:
            nebors += "r"
    # T
    if (cell[1] > 0) and (cell[1] <= (mY - 1)):
        if [cell[0], cell[1]-1] not in visited:
            nebors += "t"
    # B
    if (cell[1] >= 0) and (cell[1] < (mY - 1)):
        if [cell[0], cell[1]+1] not in visited:
            nebors += "b"
    
    return nebors

def makeMaze(mX,mY,sc=10):

    mX = int(mX/sc)  # getting cell count on each axes
    mY = int(mY/sc)
    total = mX*mY

    arr = []
    subArr = []

    def srcDead(cell, visited):
        k = getPossiblePaths(cell, visited,mX,mY)
        if len(k) == 0:
            return True
        else:
            return False

    def shouldRun():
        pr = random.randint(0,2)
        if pr == 1:
            return True
        else:
            return False

    # make maze Array
    for x in range(mX):
        subArr.append("")
    for y in range(mY):
        arr.append(subArr.copy())
    
    # defining list for the vine
    # storing paths as arrays of points
    # EX
    # [
    #   [[x1,y1],[x2,y2]],
    #   [[x1,y1]]
    # ]
    src = [[[0,0]]]  # cell data stored in X,Y format
    visited = [[0,0]]
    # new sources shall be added in this and added to main array later so as to prevent causing errors in loop
    newSrc = []

    # PROGRESS INITIALIZE
    print("PROGRESS :", end="")
    pCent = 0
    curr = 0

    solution = []  # array to store the solution path

    while(len(src) > 0):
        # begin looping for each source's each possible pathway
        #      after every pathway production add new sources
        #      a source dies if all its neghboring cells are visited

        for k in range(len(src)):
            # getting the actual path in s
            s = src[k]

            # initial PathLooping
            j = 30
            if k == 0:
                j = 5

            # LOOP
            for iPl in range(j):
                # here s consists of arrays of points that are in the path
                pathHead = s[-1]
                # get all possible paths
                paths = getPossiblePaths(pathHead,visited,mX,mY)
                # foreach path 50-50 chance for it to be made or not

                if len(paths) > 0:
                    farPaths = []
                    # fill the farPaths Array
                    for path in paths:
                        # calculate displacement for each path
                        nxtCell = []
                        if path == "l":
                            nxtCell = [pathHead[0]-1,pathHead[1]]
                        elif path == "r":
                            nxtCell = [pathHead[0]+1,pathHead[1]]
                        elif path == "t":
                            nxtCell = [pathHead[0],pathHead[1]-1]
                        else:
                            nxtCell = [pathHead[0],pathHead[1]+1]
                        
                        disp = len(s)/((nxtCell[0]**2 + nxtCell[1]**2)**0.5)

                        farPaths.append([path,disp])

                    # sort the array
                    sortedArr = []
                    while len(farPaths) > 0:
                        a = []
                        for fP in farPaths:
                            a.append(fP[1])
                        a = a.index(max(a))
                        sortedArr.append(farPaths[a])
                        farPaths.pop(a)
                    
                    farPaths.extend(sortedArr)
                    sortedArr.clear()

                    # make probability distribution
                    pDist = []
                    # if 1 path = [1]
                    # if 2 path = [0.8,0.2]
                    # if 3 path = [0.7,0.2,0.1]
                    if len(farPaths) == 3:
                        pDist = [7,9,10]
                    elif len(farPaths) == 2:
                        pDist = [8,10]
                    else:
                        pDist = [6]
                    
                    # choose a path using random randint
                    rand = random.randint(0,9)
                    chosenPath = ""
                    if len(pDist) == 1:
                        if rand < pDist[0]:
                            chosenPath = farPaths[0][0]
                    elif len(pDist) == 2:
                        if rand < pDist[0]:
                            chosenPath = farPaths[0][0]
                        elif rand < pDist[1]:
                            chosenPath = farPaths[1][0]
                        else:
                            pass
                    else:
                        if rand < pDist[0]:
                            chosenPath = farPaths[0][0]
                        elif rand < pDist[1]:
                            chosenPath = farPaths[1][0]
                        elif rand < pDist[2]:
                            chosenPath = farPaths[2][0]
                        else:
                            pass
                    
                    # implement the path chosen
                    nxtCell = []
                    if (len(chosenPath) > 0) and shouldRun():
                        if chosenPath == "l":
                            arr[pathHead[1]][pathHead[0]] += "l"
                            nxtCell = [pathHead[0]-1,pathHead[1]]

                            # including refrence to parent
                            arr[pathHead[1]][pathHead[0]-1] += "r"
                        elif chosenPath == "r":
                            arr[pathHead[1]][pathHead[0]] += "r"
                            nxtCell = [pathHead[0]+1,pathHead[1]]

                            # including refrence to parent
                            arr[pathHead[1]][pathHead[0]+1] += "l"
                        elif chosenPath == "t":
                            arr[pathHead[1]][pathHead[0]] += "t"
                            nxtCell = [pathHead[0],pathHead[1]-1]

                            # including refrence to parent
                            arr[pathHead[1]-1][pathHead[0]] += "b"
                        else:
                            arr[pathHead[1]][pathHead[0]] += "b"
                            nxtCell = [pathHead[0],pathHead[1]+1]

                            # including refrence to parent
                            arr[pathHead[1]+1][pathHead[0]] += "t"
                        # the nextcell now is marked both as visited
                        visited.append(nxtCell)

                        # current path is retained as a new path
                        tempPath = s.copy()
                        newSrc.append(tempPath)

                        # nxtCell is added to the original path
                        s.append(nxtCell)
            # if due to marking of nxtCell as visited causes any src to die it will automatically return as 0 paths
            # available to pass through thus 'if' struct will skip it automatically
            # still in order to clean up all the waste sources after all sources are checked purification shall be done
            # if this does not happen the while loop wont be able to end
        src.extend(newSrc)
        newSrc.clear()

        # finding the solution in src
        for s in src:
            if s[-1] == [mX-1,mY-1]:
                solution = s.copy()

        # purify source : add true sources to newSrc then later pass it over to src back again
        for s in src:
            if not srcDead(s[-1], visited):
                newSrc.append(s)
        
        src.clear()
        src.extend(newSrc)
        newSrc.clear()

        # PROGRESS
        pCent = int(30*(len(visited) / total))
        print("."*(pCent-curr),end="")
        curr = pCent
    print("") # END PROGRESS
    
    # DEBUG
    # for a in arr:
    #     print(a)
    
    return (arr, solution)

def drawMaze(mze, mX, mY, cv, sc=10):
    # normalizing mX and mY
    mX = int(mX/sc)
    mY = int(mY/sc)

    # manipulate maze for keeping the entry and exit open
    mze[0][0] += 'l'
    mze[mY-1][mX-1] += 'r'

    for y in range(mY):
        for x in range(mX):
            id = mze[y][x]
            if 'l' not in id:
                Xi = 10 + sc*x
                Yi = 10 + sc*y
                Xf = 10 + sc*x
                Yf = 10 + sc*(y+1)
                k = cv.create_line(Xi, Yi, Xf, Yf ,fill="black")
            if 'r' not in id:
                Xi = 10 + sc*(x+1)
                Yi = 10 + sc*y
                Xf = 10 + sc*(x+1)
                Yf = 10 + sc*(y+1)
                k = cv.create_line(Xi, Yi, Xf, Yf ,fill="black")
            if 't' not in id:
                Xi = 10 + sc*x
                Yi = 10 + sc*y
                Xf = 10 + sc*(x+1)
                Yf = 10 + sc*y
                k = cv.create_line(Xi, Yi, Xf, Yf ,fill="black")
            if 'b' not in id:
                Xi = 10 + sc*x
                Yi = 10 + sc*(y+1)
                Xf = 10 + sc*(x+1)
                Yf = 10 + sc*(y+1)
                k = cv.create_line(Xi, Yi, Xf, Yf ,fill="black")

def displayWeb(mze, mX, mY, cv):
    # normalizing mX and mY
    mX = int(mX/10)
    mY = int(mY/10)

    for y in range(mY):
        for x in range(mX):
            id = mze[y][x]
            Xi = 15 + 10*x
            Yi = 15 + 10*y
            if 'l' in id:
                Xf = 15 + 10*(x-1)
                Yf = 15 + 10*y
                k = cv.create_line(Xi, Yi, Xf, Yf ,fill="blue")
            if 'r' in id:
                Xf = 15 + 10*(x+1)
                Yf = 15 + 10*y
                k = cv.create_line(Xi, Yi, Xf, Yf ,fill="blue")
            if 't' in id:
                Xf = 15 + 10*x
                Yf = 15 + 10*(y-1)
                k = cv.create_line(Xi, Yi, Xf, Yf ,fill="blue")
            if 'b' in id:
                Xf = 15 + 10*x
                Yf = 15 + 10*(y+1)
                k = cv.create_line(Xi, Yi, Xf, Yf ,fill="blue")

def drawPath(cv, mX, mY, path, sc=10, width=1, fill="green"):
    mX = int(mX/sc)
    mY = int(mY/sc)

    if len(path) > 1:
        for i in range(1,len(path)):
            Xi = path[i-1][0]*sc + 10 + int(sc/2)
            Yi = path[i-1][1]*sc + 10 + int(sc/2)
            Xf = path[i][0]*sc + 10 + int(sc/2)
            Yf = path[i][1]*sc + 10 + int(sc/2)

            k = cv.create_line(Xi, Yi, Xf, Yf, fill=fill, width=width)

def cutMaze(mz):

    def cut():
        ratio = 0 # out of 100

        j = random.randint(1,100)
        if j <= ratio:
            return True
        else:
            return False
    
    def addToTx(txt, add):
        if add in txt:
            return txt
        else:
            return txt + add

    mY = len(mz)
    mX = len(mz[0])

    # HORIZONTAL CUTS
    for y in range(mY):
        for x in range(1, mX):
            c1 = mz[y][x-1]
            c2 = mz[y][x]

            if cut():
                c2 = addToTx(c2, 'l')
                c1 = addToTx(c1, 'r')
            
            mz[y][x-1] = c1
            mz[y][x] = c2
    # VERTICAL CUTS
    for x in range(mX):
        for y in range(1, mY):
            c1 = mz[y-1][x]
            c2 = mz[y][x]

            if cut():
                c2 = addToTx(c2, 't')
                c1 = addToTx(c1, 'b')
            
            mz[y-1][x] = c1
            mz[y][x] = c2
    return mz

# CROSS FRAME VARIABLES
dT = 100  # default = 0.1s
paths = [
    [[0,0]]
]  # initially the solver is at 0,0
end = False
sVisited = []  # stores all visited points

def solve(root,cv,mX,mY,mzArr,sc):

    def getTurnsInMaze(cell):
        turns = getPossiblePaths(cell, sVisited, mX, mY)
        # purify turns : remove turns that are not possible due to maze constraints
        mzeTurns = mzArr[cell[1]][cell[0]]
        # get intersection i.e. turns x mzeTurns
        intersection = []
        for x in mzeTurns:
            if x in turns:
                intersection.append(x)
        return intersection
    
    def displayEndPath(dispPath):
        drawPath(cv, mX, mY, dispPath, sc=sc, width=3, fill='red')

    global dT
    global paths
    global end
    global sVisited

    if not end:
        # <FRAME>
        killPathIndices = []  # containes the paths to be ended
        newPaths = []  # new paths that are formed due to turning
        reached = False  # goes true if at any moment the target is reached
        solPath = []  # holds the solution path once its found
        for path in paths:
            # getting each path in list of paths
            endCell = path[-1]
            newPathsStr = getTurnsInMaze(endCell)
            if len(newPathsStr) == 0:
                killPathIndices.append(path)  # adding path index to kill the path as it is useless now
            else:
                for turn in newPathsStr:
                    nxtCell = []
                    if turn == 'l':
                        nxtCell = [endCell[0]-1, endCell[1]]
                    elif turn == 'r':
                        nxtCell = [endCell[0]+1, endCell[1]]
                    elif turn == 't':
                        nxtCell = [endCell[0], endCell[1]-1]
                    else:
                        nxtCell = [endCell[0], endCell[1]+1]
                    
                    # DRAW the extra Line
                    subPath = [endCell, nxtCell]
                    drawPath(cv, mX*sc, mY*sc, subPath, sc)

                    # check if reached
                    if nxtCell == [mX-1,mY-1]:
                        reached = True

                        solPath = path.copy()
                        solPath.append(nxtCell)

                    if turn == newPathsStr[-1]:
                        # this is the last possible turn
                        # extend the original path
                        path.append(nxtCell)
                    else:
                        # it is one of the initial turns
                        # copy the original path and extend it so as to be added after all paths are traversed
                        copyPath = path.copy()
                        copyPath.append(nxtCell)
                        newPaths.append(copyPath)
                    # marking nxtCell as visited
                    sVisited.append(nxtCell)
        # killing dead Paths
        for path in killPathIndices:
            paths.remove(path)
        # adding newPaths
        paths.extend(newPaths)

        # check if reached
        if reached:
            end = True
            displayEndPath(solPath)

        # </FRAME>

        # SOLVE SCHEDULING
        root.after(dT, solve, root,cv,mX,mY,mzArr,sc)
    else:
        # loop has ended
        pass

sc = int(input("ENTER cell size <5> : ")) * 2
mX = int(input("ENTER X dimension of maze <0-120 for 3K resolution> : ")) * sc
mY = int(input("ENTER Y dimension of maze <0-80 for 3K resolution> : ")) * sc
dT = int(float(input("ENTER deltaTime(in seconds) <0.01> : ")) * 1000)

# declaring basic window
root = tk.Tk()
root.title("pathFinder !!")
root.geometry(str(mX+20)+"x"+str(mY+20))

cv = tk.Canvas(root, width=mX+20, height=mY+20)
cv.pack()

# MAKE MAZE
out = makeMaze(mX,mY,sc)
mzArr = cutMaze(out[0])
sol = out[1]

# DEBUG : display web
# displayWeb(mzArr, mX, mY, cv)
# DRAW SOLUTION
# drawPath(cv,mX,mY,sol, sc)  # remove comment to see solution

# DRAW MAZE
drawMaze(mzArr,mX,mY,cv,sc)

# adjust mX n mY for SOLVE LOOP
mX = int(mX/sc)
mY = int(mY/sc)
# SOLVE SCHEDULING
root.after(3000, solve, root,cv,mX,mY,mzArr,sc)

# Tk WINDOW
root.mainloop()
