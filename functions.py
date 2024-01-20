import time


ATTEMPT = 0
SHOWSTEPS = True            #for printing tracker in between
SHOWDETAILS = True          #for troubleshooting through iterations and what not
SHOWUPDATES = False
#UNDERLINE = "\033[4m"
GREEN = "\033[32m"
RED = "\033[31m"
BLUE = "\033[34m"
PURPLE = "\033[35m"
END = "\033[0m"



def makeTracker(game : list) -> list:
    """
        turns GAME into tracker
    """
    return [[[num] if num != 0 else [1,2,3,4,5,6,7,8,9] for num in row] for row in game]



def track_time(function):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        tracker = function(*args, **kwargs)
        end_time = time.time()
        time_taken = end_time - start_time
        return tracker, time_taken
    return wrapper



def printGame(tracker : list) -> None:
    """
        From the tracker, print the game (only show solved nums)
    """
    print(f"SOLVED: {GREEN}{numSolved(tracker)}{END} \t LEFT: {RED}{optionsLeft(tracker)}{END}")      #can probably calc once before sending to solve and use, then recalc once after solve, continue until done

    count = 0
    for row in tracker:
        for cell in row:
            if (count % 27 == 0) and (count != 0):
                print()
                print("-"*23)
            elif count % 9 == 0: print()
            elif count % 3 == 0: print(" |", end="")
            
            if len(cell) == 1: print(f" {cell[0]}", end="")
            else: print ("  ", end="")
            count += 1

    print("\n")



def printTracker(tracker : list) -> None:
    """
        prints the tracker
    """
    count = 0
    for row in tracker:
        for cell in row:
            if (count % 27 == 0) and (count != 0):
                print()
                print("-"*119)
            elif count % 9 == 0: print()
            elif count % 3 == 0: print(" |", end="")

            numStr = "".join(str(num) for num in cell)
            print(f"   {numStr: <9}", end="")
            count += 1

    print("\n")



def numSolved(tracker : list) -> int:
    return sum(1 for row in tracker for cell in row if len(cell) == 1)



def optionsLeft(tracker : list) -> int:
    options = sum(len(cell) for row in tracker for cell in row) - 81

    return 0 if options <= 0 else options



def checkSolution(tracker):
    rows = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[]}
    cols = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[]}
    sqrs = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[]}

    for r, row in enumerate(tracker):
        for c, col in enumerate(row):
            cols[c].append(col[0])
            rows[r].append(col[0])
            sqrs[(r // 3)*3 + (c // 3)].append(col[0])

    if any(sorted(row) != [1,2,3,4,5,6,7,8,9] for row in rows.values()): return False
    if any(sorted(col) != [1,2,3,4,5,6,7,8,9] for col in cols.values()): return False
    if any(sorted(sq) != [1,2,3,4,5,6,7,8,9] for sq in sqrs.values()): return False

    return True



if __name__ == "__main__":
    from main import GAME_1
    printTracker(makeTracker(GAME_1))
    print("*** PASSED ***")