import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors
import random
import math

# A CLASS TO STORE CARTESIAN POSITIONS
class coord:

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        if (self.x == other.x) and (self.y == other.y):
            return True
        else:
            return False
    
    def distFrom(self, point):
        return ((self.x - point.x)**2 + (self.y - point.y)**2)**0.5
    
    def __str__(self):
        return "X = " + str(self.x) + "  Y = " + str(self.y)


# A CLASS TO REPRESENT NODES OF THE BASE GRAPH (OF TERRAIN GENERATOR)
class node:

    def __init__(self, position, weight) -> None:
        self.pos = position
        self.wt = weight
        self.neighbors = []
    
    def add_neighbour(self, neighbor):
        self.neighbors.append(neighbor)

# A CLASS USED TO DEFINE A NODE THAT TRAVELS (USED DURING TERRAIN GENRATION)
class travelNode:

    def __init__(self, originPos, currPos, targetPos, iWeight, fWeight):
        self.origin = originPos
        self.pos = currPos
        self.tPos = targetPos
        self.iWt = iWeight
        self.fWt = fWeight

colors = ["black", "grey", "red", "green", "white"]
values = [0, 0.25, 0.5, 0.75, 1]
#-------  0,  1  ,  2  , 3  , 4
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", list(zip(values, colors)))

print("choose X and Y to be 1 or 2 for optimal performance\ngoing beyond these values causes the product")
print("to increase at a high rate.... product >10K causes high ping ... ~20K causes serious slow performance")
print(">30K begins to kill python and matplotlib all at once")
print("number of nodes >= 10 in all cases ... dont set x_res or y_res to be 0")
print("thickness should be lower for lower values of resolution lowest shall be taken as 7")
print("noise reduction 1 is minimum 3 gives a nice performance beyond this is useless")

x_res = int(input("ENTER X : ")) * 100
y_res = int(input("ENTER Y : ")) * 100
N = int(input("ENTER number of base nodes(>10) : "))

# CHECK
if (N < 10):
    N = 10

thickness = int(input("ENTER thickness : "))
noiseReduction = int(input("ENTER noise reduction : "))

grid = []
empty = []

for x in range(x_res):
    empty.append(0)
for y in range(y_res):
    grid.append(empty.copy())


def modifyGrid(pos, newVal):
    global grid
    try:
        grid[pos.y][pos.x] = newVal
    except:
        print(pos)
        return 1/0

state = 0
# 0 = generate points
# 1 = connect them ... (in data)
# 2 = generate travel nodes
# 3 = connect them using minimal diagonal paths and carve them ... (visually)
# 4 = select one of the points as starting and a random one as target
# 5 = initialize pathfinder
# 6 = frame-wise calculation
# 7 = display final path and end !

nodeList = []
tNodeList = []
origin, target = None, None
reached = False
paths = []
visited = []
finalPath = []
reps = 0

def getRandomPointNearby(point):
    validPoints = []
    if (point.x != 0) and (point.x != x_res-1):
        validPoints.append(coord(point.x-1,point.y))
        validPoints.append(coord(point.x+1,point.y))
    if (point.y != 0) and (point.y != y_res-1):
        validPoints.append(coord(point.x,point.y-1))
        validPoints.append(coord(point.x,point.y+1))
    if (point.x != 0) and (point.y!= 0):
        validPoints.append(coord(point.x-1,point.y-1))
    if (point.x != 0) and (point.y!= y_res-1):
        validPoints.append(coord(point.x-1,point.y+1))
    if (point.x != x_res-1) and (point.y!= 0):
        validPoints.append(coord(point.x+1,point.y-1))
    if (point.x != x_res-1) and (point.y!= y_res-1):
        validPoints.append(coord(point.x+1,point.y+1))
    
    return [validPoints[random.randint(0,len(validPoints)-1)], validPoints]

# Define the function to generate the data
def generate_data():
    global grid
    global state
    global tNodeList
    global origin
    global target
    global reached
    global paths
    global visited
    global finalPath
    global nodeList
    global reps

    if (state == 0):
        def getRandomPos():
            while True:
                x = random.randint(0, x_res-1)
                y = random.randint(0, x_res-1)
                j = coord(x, y)
                check = True
                for n in nodeList:
                    if (j == n.pos):
                        check = False
                        break
                if check:
                    break 
            return coord(x, y)

        for i in range(N):
            pos = getRandomPos()
            wt = random.randint(1,7)
            nodeList.append(node(pos, wt))
            # mark nodes on the grid
            modifyGrid(pos, 4)
        
        # END STATE
        state = 1
    elif (state == 1):
        for n2 in nodeList:
            nodeListCopy = nodeList.copy()
            dist = []
            for n1 in nodeListCopy:
                dist.append(n2.pos.distFrom(n1.pos))
            for k in range(n2.wt + 1):
                if (k==0):
                    ind = dist.index(0)
                    dist.pop(ind)
                    nodeListCopy.pop(ind)
                else:
                    ind = dist.index(min(dist))
                    n2.add_neighbour(nodeListCopy[ind])
                    dist.pop(ind)
                    nodeListCopy.pop(ind)
        
        # END STATE
        state = 2
    elif (state == 2):
        tNodeList = []
        for n in nodeList:
            neighbors = n.neighbors
            for nb in neighbors:
                tNodeList.append(travelNode(n.pos,n.pos,nb.pos,n.wt,nb.wt))
        
        # END STATE
        state = 3
    elif (state == 3):
        allDone = True
        for tNode in tNodeList:
            dX = tNode.tPos.x - tNode.pos.x
            dY = tNode.tPos.y - tNode.pos.y
            if (dX == 0) and (dY == 0):
                delta = [0,0]
            else:
                allDone = False
                if (dX == 0):
                    if dY > 0:
                        angle = 90
                    else:
                        angle = -90
                else:
                    angle = (180 / math.pi) * math.atan(dY/dX)
                # fix angle
                if dX < 0:
                    angle += 180
                # get newPos
                if (angle > (315+360)/2) and (angle <= (0+45)/2):
                    delta = [1, 0]
                elif (angle > (0+45)/2) and (angle <= (45+90)/2):
                    delta = [1, 1]
                elif (angle > (45+90)/2) and (angle <= (90+135)/2):
                    delta = [0,1]
                elif (angle > (90+135)/2) and (angle <= (135+180)/2):
                    delta = [-1,1]
                elif (angle > (135+180)/2) and (angle <= (180+225)/2):
                    delta = [-1,0]
                elif (angle > (180+225)/2) and (angle <= (225+270)/2):
                    delta = [-1,-1]
                elif (angle > (225+270)/2) and (angle <= (270+315)/2):
                    delta = [0,-1]
                else:
                    delta = [1,-1]
            
            newPos = coord(tNode.pos.x + delta[0], tNode.pos.y + delta[1])
            tNode.pos = newPos

            # painting new point
            modifyGrid(newPos, 4)

            # getting weight
            currWt = (tNode.pos.distFrom(tNode.origin) / tNode.tPos.distFrom(tNode.origin))*(tNode.fWt - tNode.iWt) + tNode.iWt
            
            for recur in range(noiseReduction):
                point = tNode.pos
                for counter in range(random.randint(4,thickness)):
                    # print(point)
                    point = getRandomPointNearby(point)[0]

                    # paint the point
                    modifyGrid(point, 4)
        
        if allDone:
            # END STATE
            state = 4
    elif (state == 4):
        origin = nodeList[random.randint(0,len(nodeList)-1)]
        target = nodeList[0]
        mDist = target.pos.distFrom(origin.pos)
        for rN in nodeList:
            m = rN.pos.distFrom(origin.pos)
            if m > mDist:
                mDist = m
                target = rN
        
        # DISPLAYING THESE NODES
        modifyGrid(origin.pos, 2)
        modifyGrid(target.pos, 2)

        # END STATE
        state = 5
    elif (state == 5):
        # clear unnecessary data
        tNodeList = []
        nodeList = []

        origin = origin.pos
        target = target.pos

        # make required lists
        paths = [[origin]]

        # END STATE
        state = 6
    elif (state == 6):
        reps += 1
        if len(paths) > 0:
            addPath = []
            delLis = []
            for ind in range(len(paths)):
                path = paths[ind]

                endPoint = path[-1]
                nearby = getRandomPointNearby(endPoint)[1]

                if target in nearby:
                    finalPath = path.copy()
                    finalPath.append(target)
                    reached = True
                    break

                # purify nearby list
                purifiedList = []
                for n in nearby:
                    if (n not in visited) and (grid[n.y][n.x] == 4):
                        purifiedList.append(n)

                if len(purifiedList) == 0:
                    # path is dead and hasn't reached target
                    delLis.append(path)
                else:
                    savePath = path.copy()
                    for nInd in range(len(purifiedList)):
                        if nInd == 0:
                            path.append(purifiedList[nInd])
                        else:
                            newPath = savePath.copy()
                            newPath.append(purifiedList[nInd])
                            addPath.append(newPath)
                        modifyGrid(purifiedList[nInd], 1)
                        visited.append(purifiedList[nInd])
            if reached:
                # clearing big variables
                paths = []
            else:
                # deleting dead paths
                for dI in delLis:
                    paths.remove(dI)
                # adding new paths
                for aI in addPath:
                    paths.append(aI)
        else:
            # END
            state = 7
        
        print(str(len(paths)) + " * " + str(reps) + " = " + str(reps*len(paths)))
    elif (state == 7):
        # final path display
        for n in finalPath:
            modifyGrid(n,3)
        # END
        state = 8
    else:
        pass

# Define the function to update the plot
def update_plot(i, ax, fig):
    global grid
    ax.clear()
    generate_data()
    ax.pcolormesh(grid, cmap=cmap)

# Create a figure and an axis
fig, ax = plt.subplots()

# Create an animation object
ani = animation.FuncAnimation(fig, update_plot, interval=100, frames=10, fargs=(ax, fig))

# Show the animation
plt.show()


