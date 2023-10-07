import tkinter as tk
import random

def makeMaze(cv,mX,mY):

    mX = int(mX/10)  # getting cell count on each axes
    mY = int(mY/10)
    total = mX*mY

    arr = []
    subArr = []

    def getPossiblePaths(cell, visited):
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

    def srcDead(cell, visited):
        k = getPossiblePaths(cell, visited)
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
            j = 10
            if k == 0:
                j = 20

            # LOOP
            for iPl in range(j):
                # here s consists of arrays of points that are in the path
                pathHead = s[-1]
                # get all possible paths
                paths = getPossiblePaths(pathHead,visited)
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

def drawMaze(mze, mX, mY, cv):
    # normalizing mX and mY
    mX = int(mX/10)
    mY = int(mY/10)

    # manipulate maze for keeping the entry and exit open
    mze[0][0] += 'l'
    mze[mY-1][mX-1] += 'r'

    for y in range(mY):
        for x in range(mX):
            id = mze[y][x]
            if 'l' not in id:
                Xi = 10 + 10*x
                Yi = 10 + 10*y
                Xf = 10 + 10*x
                Yf = 10 + 10*(y+1)
                k = cv.create_line(Xi, Yi, Xf, Yf ,fill="black")
            if 'r' not in id:
                Xi = 10 + 10*(x+1)
                Yi = 10 + 10*y
                Xf = 10 + 10*(x+1)
                Yf = 10 + 10*(y+1)
                k = cv.create_line(Xi, Yi, Xf, Yf ,fill="black")
            if 't' not in id:
                Xi = 10 + 10*x
                Yi = 10 + 10*y
                Xf = 10 + 10*(x+1)
                Yf = 10 + 10*y
                k = cv.create_line(Xi, Yi, Xf, Yf ,fill="black")
            if 'b' not in id:
                Xi = 10 + 10*x
                Yi = 10 + 10*(y+1)
                Xf = 10 + 10*(x+1)
                Yf = 10 + 10*(y+1)
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

def drawPath(cv, mX, mY, path):
    mX = int(mX/10)
    mY = int(mY/10)

    if len(path) > 1:
        for i in range(1,len(path)):
            Xi = path[i-1][0]*10 + 15
            Yi = path[i-1][1]*10 + 15
            Xf = path[i][0]*10 + 15
            Yf = path[i][1]*10 + 15

            k = cv.create_line(Xi, Yi, Xf, Yf, fill="green")


mX = int(input("ENTER X dimension of maze : ")) * 10
mY = int(input("ENTER Y dimension of maze : ")) * 10

# declaring basic window
root = tk.Tk()
root.title("pathFinder !!")
root.geometry(str(mX+20)+"x"+str(mY+20))

cv = tk.Canvas(root, width=mX+20, height=mY+20)
cv.pack()

# MAKE MAZE
out = makeMaze(cv,mX,mY)
mzArr = out[0]
sol = out[1]

# DRAW SOLUTION
#drawPath(cv,mX,mY,sol)  # remove comment to see solution

# DEBUG : display web
# displayWeb(mzArr, mX, mY, cv)

# DRAW MAZE
drawMaze(mzArr,mX,mY,cv)

tk.mainloop()
