from solve import *
from functions import *
from games import *



@track_time
def RunGame(tracker):
    """
        does initial reduction of tracker options with given cells, then solveGame()
    """
    options_removed = 0
    for r, row in enumerate(tracker):
        for c, cell in enumerate(row):
            if len(cell) == 1:
                options_removed += updateGame(tracker, r, c, cell[0])
    if SHOWSTEPS: print(f"Removed {RED}{options_removed}{END} options\n\n")

    tracker, num_attempts = solveGame(tracker, 0)
    
    return tracker, num_attempts



