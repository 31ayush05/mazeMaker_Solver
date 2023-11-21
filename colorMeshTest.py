# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation

# fig = plt.figure()
# ax = fig.add_subplot(111)
# xdata, ydata = [], []
# ln, = plt.plot([], [], 'ro')

# def init():
#     ax.set_xlim(0, 10)
#     ax.set_ylim(0, 1)
#     return ln,

# def update(frame):
#     xdata.append(frame)
#     ydata.append(np.random.random())
#     ln.set_data(xdata, ydata)
#     return ln,

# ani = FuncAnimation(fig, update, frames=np.linspace(0, 10, 100),
#                     init_func=init, blit=True)
# plt.show()

# Import the required modules
import random
import shapely.geometry as geom
import matplotlib.pyplot as plt

# Define a function to generate a random polygon with a given number of vertices
def random_polygon(n):
    # Generate n random points in the unit square
    points = [(random.random(), random.random()) for _ in range(n)]
    # Create a shapely polygon from the points
    polygon = geom.Polygon(points)
    # Return the polygon
    return polygon

# Ask the user for the number of polygons to generate
n = int(input("How many polygons do you want to generate? "))

# Create an empty list to store the polygons
polygons = []

# Loop n times
for i in range(n):
    # Generate a random number of vertices between 3 and 10
    k = random.randint(3, 10)
    # Generate a random polygon with k vertices
    polygon = random_polygon(k)
    # Add the polygon to the list
    polygons.append(polygon)

# Create a matplotlib figure and axis
fig, ax = plt.subplots()

# Loop through the polygons
for polygon in polygons:
    # Plot the polygon on the axis
    x, y = polygon.exterior.xy
    ax.plot(x, y)

# Set the axis limits to the unit square
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# Show the figure
plt.show()
