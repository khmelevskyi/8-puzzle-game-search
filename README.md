# 8-puzzle-game-search
In this project we have implementations of LDFS and RBFS searching algorithms to solve 8-puzzle game.
Also, after running the program, you will see the statistics for each algorithm.

In this program the initial state of the game is calculated automatically by moving the blank space in random
order for some amount of these moves. This way we ensure that the solution exists and this way we can approximately
decide the depth of the search.

### RBFS
This is an informed search algorithm.
For this algorithm you can choose the heuristic function. The function can be calculated either by the number of misplaced plates or by the distanced of each plate between its current state and goal state.

### LDFS
This is a not informed search algorithm.

### Based on
The inspiration: [NiloofarShahbaz's project](https://github.com/NiloofarShahbaz/8-puzzle-search-implementation)

