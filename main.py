from solve import *
from functions import *
from games import *



@track_time
def RunGame(tracker, attempt_num):
    """
        does initial reduction of tracker options with given cells, then solveGame()
    """
    options_removed = 0
    for r, row in enumerate(tracker):
        for c, cell in enumerate(row):
            if len(cell) == 1:
                options_removed += updateGame(tracker, r, c, cell[0])

    if SHOWSTEPS: print(f"Removed {RED}{options_removed}{END} options\n")
    
    return solveGame(tracker, attempt_num)



if __name__ == "__main__":
    print()
    for chosen_game in GAMES.keys():
    #for chosen_game in ["GAME_1"]:
        attempt_num = 0 
        tracker = makeTracker(GAMES[chosen_game])

        print(f"{BLUE}{f'{UNDERLINE} {chosen_game} {END}':^95}{END}")
        if SHOWSTEPS: 
            print(f"Attempt {BLUE}0{END}")
            printBoard(tracker)
        if SHOWDETAILS: printTracker(tracker)

        attempt_num, time_taken = RunGame(tracker, attempt_num)

        if SHOWSTEPS: 
            print()
            printBoard(tracker)
        print(f"Game Solved in {BLUE}{attempt_num}{END} attempts and {BLUE}{time_taken:.6f}{END} seconds")
        solved = checkSolution(tracker, attempt_num)
        print(f"Checked: {GREEN if solved else RED}{solved}{END}")
        if solved:
            unaltered = checkAltered(tracker, GAMES[chosen_game])
            print(f"Checked unaltered: {GREEN if unaltered else RED}{unaltered}{END}")
        print()