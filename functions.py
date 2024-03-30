import time
import sys



ATTEMPT = 0
SHOWSTEPS = True            #shows actions and tracker in between iterations
SHOWDETAILS = False          #shows details of actions
UNDERLINE = "\033[4m"
GREEN = "\033[32m"
RED = "\033[31m"
BLUE = "\033[34m"
PURPLE = "\033[35m"
END = "\033[0m"



def makeTracker(game : tuple) -> list:
    return [[[num] if num != 0 else [1,2,3,4,5,6,7,8,9] for num in row] for row in game]



def track_time(function):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        function(*args, **kwargs)
        end_time = time.time()
        time_taken = end_time - start_time
        return time_taken
    return wrapper



def printBoard(tracker : list) -> None:
    print(f"SOLVED: {GREEN}{numSolved(tracker)}{END} \t LEFT: {RED}{optionsLeft(tracker)}{END}")      #can probably calc once before sending to solve and use, then recalc once after solve, continue until done
    count = 0

    for row in tracker:
        for cell in row:
            if (count % 27 == 0) and (count != 0): print("\n"+"-"*23)
            elif count % 9 == 0: print()
            elif count % 3 == 0: print(" |", end="")
            if len(cell) == 1: print(f" {cell[0]}", end="")
            else: print ("  ", end="")
            count += 1
    print("\n")



def printTracker(tracker : list) -> None:
    count = 0

    for row in tracker:
        for cell in row:
            if (count % 27 == 0) and (count != 0): print("\n"+"-"*95)
            elif count % 9 == 0: print()
            elif count % 3 == 0: print(" |", end="")
            numStr = "".join(str(num) for num in cell)
            print(f" {numStr: <9}", end="")
            count += 1
    print("\n")



def numSolved(tracker : list) -> int:
    return sum(1 for row in tracker for cell in row if len(cell) == 1)



def optionsLeft(tracker : list) -> int:
    return max(0,  sum(len(cell) for row in tracker for cell in row) - 81)



def checkSolution(tracker, attempt_num):
    rows = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[]}
    cols = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[]}
    sqrs = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[]}

    for r, row in enumerate(tracker):
        for c, col in enumerate(row):
            if len(col) == 0: 
                raise Exception(f"{RED}ERROR{END} | checkSolution | {RED}BLANK CELL{END} - ({r}, {c})") #move to UpdateGame()?
            cols[c].append(col[0])
            rows[r].append(col[0])
            sqrs[(r // 3)*3 + (c // 3)].append(col[0])

    for plane, solutions in {"ROW": rows, "COL" : cols, "SQR" : sqrs}.items():
        for num, values in solutions.items():
            if sorted(values) != [1,2,3,4,5,6,7,8,9]:
                if SHOWDETAILS: print(f"{RED}{plane} {num} is incorrect{END}")
                return False

    return True



def checkAltered(tracker, og_game):
    for r, row in enumerate(og_game):
        for c, cell in enumerate(row):
            if cell != 0 and cell != tracker[r][c][0]:
                print(f"ALTERED: ({r},{c}): {cell} - {tracker[r][c]}")
                return False
    return True



if __name__ == "__main__":
    import os
    files = ["main.py", "solve.py", "functions.py"]
    all_with = 0
    all_without = 0

    print("\nNUMBER OF LINES IN:")
    longest = max(len(file) for file in files)

    for file in files:
        with open(os.path.join(os.path.dirname(__file__), file), "r") as f:
            lines = [line.strip() for line in f.readlines()]
            with_spaces = len(lines)
            without_spaces = 0
            for l, line in enumerate(lines):
                if (len(line) > 0) and (line[0] != "#"):
                    without_spaces += 1
                if line[0:3] == '"""':
                    if line.find('"""', 3) == -1: without_spaces -= 1
                    else: without_spaces -= (lines[l+1:].find('"""') + 2)
                if file != "main.py" and line == 'if __name__ == "__main__":': break

        all_with += with_spaces
        all_without += without_spaces
        
        print(f"{" "*(longest-len(file))}{file}: {f'{with_spaces} | {without_spaces}':^9}")

    print(f"\n{' '*(longest-5)}TOTAL: {f'{all_with} | {all_without}':^9}\n")