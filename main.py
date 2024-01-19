import copy

from functions import *
from solve import *
from games import *



@track_time
def RunGame(tracker):
    """
        0. do initial update of the tracker
        1. then continue to solve (and update game for solved cells) until solved
        2. if can't be solved, make a guess and continue 1. If guess unsolvable, restart 2 with new guess
    """
    options_removed = 0
    for r, row in enumerate(tracker):
        for c, cell in enumerate(row):
            if len(cell) == 1:
                options_removed += updateGame(tracker, r, c, cell[0])
    if SHOWSTEPS: print(f"Removed {RED}{options_removed}{END} options\n\n")

    tracker, num_attempts = solveGame(tracker, 0)
    
    return tracker, num_attempts

    

if __name__ == "__main__":
    tracker = makeTracker(EXPERT)
    print(f"\nAttempt {BLUE}0{END}")
    printGame(tracker)
    printTracker(tracker)

    tracker, num_attempts, time_taken = RunGame(tracker)

    print()
    printGame(tracker)
    print(f"Game Solved in {BLUE}{num_attempts}{END} attempts and {BLUE}{time_taken:.6f}{END} seconds")
    print(f"Checked solution: {checkSolution(tracker)}\n")