main.py      -  creates tracker, starts game, and prints results
solve.py     -  is used by main.py to solve games, sends results to main
functions.py -  is used by main.py and solve.py for tasks like printing the game, counting optionsLeft, and anything else that doesn't alter tracker
games.py     -  stores games as tuples to be used by main.py in initialization of game

tracker is a 2D lists that tracks what options are left for each cell in the game, based on other cells in the row/col/square