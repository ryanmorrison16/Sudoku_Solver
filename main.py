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



if __name__ == "__main__":
    tracker = makeTracker(GAME_1)
    print(f"\nAttempt {BLUE}0{END}")
    printGame(tracker)
    printTracker(tracker)

    tracker, num_attempts, time_taken = RunGame(tracker)

    print()
    printGame(tracker)
    print(f"Game Solved in {BLUE}{num_attempts}{END} attempts and {BLUE}{time_taken:.6f}{END} seconds")
    solved = checkSolution(tracker)
    print(f"Checked verified: {GREEN if solved else RED}{solved}{END}\n")