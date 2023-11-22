# maze.py

It uses `random` and `tkinter` to generate and display the maze alongwith the simulation of the algorithm solving the maze

When the file runs it will take the following inputs

- `ENTER cell size <5>` :  this defines the side length of one cell of the maze to be generated the bigger the value the larger the maze will look but also restrict the size of maze you can get (easily displayed on your computer screen) ... A value of `5` works quite well

- `X dimension input` : it is the number of cells in horizontal direction ... i have a 3K display with 200% zoom a `maximum of 120` fits quite well ... keep it on the lower side though for faster maze genrations

- `Y dimension input` : it is the number of cells in vertical direction `maximum of 80` worked quite well for me

> NOTE : there is absolutely no need to keep X and Y equal. unequal values will result in generation of a recangular maze.

- `deltaTime(in seconds)` : it is the time after which next step of the algorithm takes place it is necessary for visualization purposes. a value of `0.01` gives a good and fast visualization, one may increase this value to view simulation at a slower rate. setting the value to `0` will result in instantaneous results. 

maze solving starts a few seconds after the maze is genrated this is so as to give the user time to bring the outpuot window in focus. the green travelling lines in the simulation are the branches of algorithm currently exploring. As soon as one of the branch reaches the end a thick red lines displays the final path.

# terrain.py

this uses `random`, `math`, `matplotlib` to generate a organic playground in which the algorithm finds shortest route between the two paths.

The terrain thus generated is very high resolution and forces python to store a huge amount of values which might result in slowing down of calculations at certain points when the `product` increases above certain limits

the algorithm takes in following inputs

- `ENTER X`, `ENTER Y` : here you need to enter the size of terrain in horizontal and vertical directions. a value of `1` refers to `50` points. thus the values you enter will be multiplied by `50` to comeup with actual height and widht of the playArea. One must avoid going above `x=2,y=2` beyond these values things become slow

- `ENTER number of base nodes(>10)` : it is the number of nodes to be used to generate the playground ... play with it to figure out !!!

- `ENTER thickness` : it is the thickness of the paths connecting the generated nodes keep `7` as the lowest value and increase the number with higher resolution. But you are free to write any integer there ... 🙃

- `ENTER noise reduction` : a value of `3` works well. lower the value the noisier the graph. yet again you are free to write absolutely any integer ... DONT GET CARRIED AWAY

when the algorithm begins to clculate the path the console is logged with `"a" * "b" = "a*b"` here `a` = the number of paths currently exploring the maze and `b` signifies the length of each path. `a*b` gives the number of values stored in the values. 
> HIGHER the value of `a*b` the slower the things get

> NOTE : this algorithm considers distance between (0,0) and (0,1) to be the same as (0,0) and (1,1) 

> ALSO there might comeup a out of range error ... just rerun the code it goes away !!! it comes up veryy rarely ...