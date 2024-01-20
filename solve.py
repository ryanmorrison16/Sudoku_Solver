from functions import *

import copy


def updateGame(tracker, row_num : int, col_num : int, value : int) -> int:
    """
    Updates tracker for provided solved value
        If a cells options is reduced to 1 during update, this solution is also updated in tracker
    """
    options_removed = 0
    square_row = row_num // 3
    square_col = (col_num // 3) * 3

    for r, row in enumerate(tracker):
        if r // 3 == square_row:
            if r == row_num:                #same row
                for c, cell in enumerate(row):
                    if value in cell and c != col_num:
                        cell.remove(value)
                        options_removed += 1
                        if len(cell) == 1: 
                            options_removed += updateGame(tracker, r, c, cell[0])
            else:                           #same square
                for c in range(square_col, square_col + 3):
                    if value in row[c]:
                        row[c].remove(value)
                        options_removed += 1
                        if len(row[c]) == 1:
                            options_removed += updateGame(tracker, r, c, row[c][0])

        elif value in row[col_num]:         #same column
            row[col_num].remove(value)
            options_removed += 1
            if len(row[col_num]) == 1: 
                options_removed += updateGame(tracker, r, col_num, row[col_num][0])

    if SHOWUPDATES: print("Updated", options_removed)

    return options_removed
    


def updateRow(tracker, row_num : int, col_nums : list, value : int):
    """
        vlaue has to be in col included in col_nums
        so remove it as an option from all other cols in the row
    """
    options_removed = 0

    for c, cell in enumerate(tracker[row_num]):
        if (c not in col_nums) and (value in cell):
            cell.remove(value)
            options_removed += 1
            if len(cell) == 1: 
                options_removed += updateGame(tracker, row_num, c, cell[0])

    if SHOWUPDATES: print("Updated", options_removed)

    return options_removed



def updateCol(tracker, row_nums : list, col_num : int, value : int):
    options_removed = 0

    for r, row in enumerate(tracker):
        if (r not in row_nums) and (value in row[col_num]):
            row[col_num].remove(value)
            options_removed += 1
            if len(row[col_num]) == 1: 
                options_removed += updateGame(tracker, r, col_num, row[col_num][0])

    if SHOWUPDATES: print("Updated", options_removed)

    return options_removed



def updateSquare(tracker, cells : list, values):
    options_removed = 0
    square_row = (cells[0][0] // 3) * 3
    square_col = (cells[0][1] // 3) * 3

    for r in range(square_row, square_row + 3):
        for c in range(square_col, square_col + 3):
            if (r,c) not in cells:
                for num in values:
                    if num in tracker[r][c]:
                        tracker[r][c].remove(num)
                        options_removed += 1

    if SHOWUPDATES: print("Updated",options_removed)

    return options_removed



def simpleSolve(tracker):
    """
        Solves loners in rows, columns, and squares

        Solving all axis at same time creates issues (eg. solving a row loner messes up col loners)
    """
    def solveRowLoners(tracker):
        # start with row_unsolved = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]}
            #and then check if key exists
            #if it does and v=len(values) == 0 append
            #else delete the key (because theres >1 occurence in row)
        solved = 0
        options_removed = 0
        for r, row in enumerate(tracker):
            row_loners = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]}
            for c, cell in enumerate(row):
                if len(cell) > 1:
                    for value in cell:
                        if value in row_loners.keys():
                            if not row_loners[value]: row_loners[value].append((r,c))
                            else: del row_loners[value]
                else:
                    del row_loners[cell[0]]

            if row_loners:
                if SHOWDETAILS: print(f"ROW LONERS: {row_loners}")
                for value, coordinates in row_loners.items():
                    coordinates = coordinates[0]
                    options_removed += len(row[coordinates[1]]) - 1
                    row[coordinates[1]] = [value]
                    options_removed += updateGame(tracker, r, coordinates[1], value)
                    solved += 1

        if SHOWSTEPS: print(f"Solved {GREEN}{solved}{END} Row Loners")

        return options_removed

        
    def solveColLoners(tracker):
        solved = 0
        options_removed = 0
        col_loners = {c : {v : [] for v in range(1,10)} for c in range(0,9)}

        for r, row in enumerate(tracker):
            for c, cell in enumerate(row):
                if len(cell) > 1:
                    for value in cell:
                        if c in col_loners.keys():                      #col_loners
                            if value in col_loners[c].keys():
                                if len(col_loners[c][value]) == 0:
                                    col_loners[c][value].append((r,c))
                                else: 
                                    del col_loners[c][value]
                else: del col_loners[c][cell[0]]
                if c in col_loners and len(col_loners[c]) == 0: del col_loners[c]

        
        for c, loner in col_loners.items():
            if SHOWDETAILS: print(f"COLUMN LONERS: {list(col_loners.values())}")
            for loner_key, loner_values in loner.items():
                loner_values = loner_values[0]
                options_removed += len(tracker[loner_values[0]][loner_values[1]]) - 1
                tracker[loner_values[0]][loner_values[1]] = [loner_key]
                options_removed += updateGame(tracker, loner_values[0], loner_values[1], loner_key)
                solved += 1

        if SHOWSTEPS: print(f"Solved {GREEN}{solved}{END} Column Loners")

        return options_removed
    

    def solveSquareLoners(tracker): 
        solved = 0
        options_removed = 0
        all_square_loners = {}
        for square_row in [0,3,6]:
            for square_col in [0,3,6]:
                square_loners = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]}

                for r in range(square_row, square_row+3):
                    for c in range(square_col, square_col +3):
                        if len(tracker[r][c]) > 1:
                            for num in tracker[r][c]:
                                if num in square_loners.keys():
                                    if not square_loners[num]: square_loners[num].append((r,c))
                                    else: del square_loners[num]
                        else: del square_loners[tracker[r][c][0]]

                if square_loners:
                    for num, cell in square_loners.items():
                        all_square_loners[(cell[0][0], cell[0][1])] = num

        if SHOWDETAILS: print(f"SQUARE LONERS: {all_square_loners}")
        for cell, value in all_square_loners.items():
            options_removed += len(tracker[cell[0]][cell[1]]) - 1
            tracker[cell[0]][cell[1]] = [value]
            options_removed += updateGame(tracker, cell[0], cell[1], value)
            solved += 1

        if SHOWSTEPS: print(f"Solved {GREEN}{len(all_square_loners)}{END} Square Loners")

        return options_removed

    options_removed = 0                        
    options_removed += solveRowLoners(tracker)
    options_removed += solveColLoners(tracker)
    options_removed += solveSquareLoners(tracker)

    return options_removed



def complexSolve(tracker):
    """
        For complex techniques such as the X-Wing, Skyscraper, etc
    """
    def inLineSquare(tracker):
        options_removed = 0
        solved = 0
        for square_row in [0,3,6]:
            for square_col in [0,3,6]:
                square = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]}
                for r in range(square_row, square_row + 3):
                    for c in range(square_col, square_col + 3):
                        if len(tracker[r][c]) > 1:
                            for value in tracker[r][c]:
                                if value in square.keys():
                                    square[value].append((r,c))
                        else: del square[tracker[r][c][0]]

                for value, cells in square.items():
                    if all(cell[0] == cells[0][0] for cell in cells):
                        removed_from_row = updateRow(tracker, cells[0][0], [cell[1] for cell in cells], value)
                        if removed_from_row: 
                            solved += 1
                            options_removed += removed_from_row
                            if SHOWDETAILS: print(f"Inline Row {cells[0][0]}: {value}")
                    if all(cell[1] == cells[0][1] for cell in cells):
                        removed_from_col = updateCol(tracker, [cell[0] for cell in cells], cells[0][1], value)
                        if removed_from_col: 
                            solved += 1
                            options_removed += removed_from_col
                            if SHOWDETAILS: print(f"Inline Column {cells[0][1]}: {value}")

        if SHOWSTEPS: print(f"Found {GREEN}{solved}{END} In-Line Square Duplicates")

        return options_removed
    
    def samePairInSquare(tracker):
        """
        if two cells in the same square have ONLY the same two values (eg, 5 and 7) then 5 and 7 can be removed from other cells in the square
            -same if 3 cells share same 3 values and so on.
        """
        options_removed = 0
        solved = 0
        
        for square_row in [0,3,6]:
            for square_col in [0,3,6]:
                square = {}
                found = []
                for r in range(square_row, square_row + 3):
                    for c in range(square_col, square_col + 3):
                        square[(r,c)] = tracker[r][c]
        
                for values in square.values():
                    num = list(square.values()).count(values)
                    if (num > 1 and num == len(values)) and (values not in found):
                        options_removed += updateSquare(tracker, [cell for cell, vals in square.items() if vals == values], values)
                        found.append(values)
                        solved += 1
                        if SHOWDETAILS: print(f"Square {(square_row + 1) + (square_col // 3)} Duplicates: {values}")
        
        if SHOWSTEPS: print(f"Found {GREEN}{solved}{END} Square Duplicate")

        return options_removed


    options_removed = 0
    options_removed += samePairInSquare(tracker)
    options_removed += inLineSquare(tracker)

    return options_removed
    


def makeGuesses(tracker, attempt_num):
    """
    Only guessing from one cell (with the fewest guesses) - guesses from other cells can be made in recursive calls (but 1 of cell_to_guess_from values HAS to be correct)
    """
    options_removed = 0
    cell_to_guess_from = {0: [1,2,3,4,5,6,7,8,9,10]}
    for r, row in enumerate(tracker):
        for c, cell in enumerate(row):
            if (len(cell) > 1) and (len(cell) < len(next(iter(cell_to_guess_from.values())))):
                cell_to_guess_from = {(r, c) : cell}

    cell, possible_guesses = next(iter(cell_to_guess_from.items()))
    if SHOWDETAILS and False: print(f"POSSIBLE GUESSES for {cell}: {possible_guesses}")
    row = cell[0]
    col = cell[1]
    
    for guess in possible_guesses:
        if SHOWSTEPS or True: print(f"{PURPLE}GUESS{END}: {cell} - {guess}")
        attempt = copy.deepcopy(tracker)
        options_removed += len(possible_guesses) - 1
        attempt[row][col] = [guess]
        options_removed += updateGame(attempt, row, col, guess)
        if SHOWDETAILS or True: print(f"Removed {RED}{options_removed}{END} options with guess\n")

        try: result, attempt_num = solveGame(attempt, attempt_num)
        except Exception as e: 
            print(f"{PURPLE}PREVIOUS GUESS FAILED{END} - {e}\n{PURPLE}NEXT ", end="")
            continue

        if checkSolution(result):
            tracker = copy.deepcopy(result)
            break

    return tracker, attempt_num



def solveGame(tracker, attempt_num):
    options_left = optionsLeft(tracker)
    while options_left:
        attempt_num += 1
        if SHOWSTEPS:
            print(f"\nAttempt {BLUE}{attempt_num}{END}")
            print(f"SOLVED: {GREEN}{numSolved(tracker)}{END} \t LEFT: {RED}{options_left}{END}")
            printTracker(tracker)
        options_removed = simpleSolve(tracker)

        if not options_removed:
            options_removed += complexSolve(tracker)
        if SHOWSTEPS: print(f"\nRemoved {RED}{options_removed}{END} options\n")

        if not options_removed:
            #exit("EXIT - Had to make Guesses\n")
            tracker, attempt_num = makeGuesses(tracker, attempt_num) #Could be unnecessary to have variable
            break

        options_left = optionsLeft(tracker)

    return tracker, attempt_num



if __name__ == "__main__":
    from games import *
    test = makeTracker(MED)
    printTracker(test)
    for r, row in enumerate(test):
        for c, cell in enumerate(row):
            if len(cell) == 1:
                updateGame(test, r, c, cell[0])
    printTracker(test)
    simpleSolve(test)
    printTracker(test)
    complexSolve(test)
    printTracker(test)
    print("\n***PASSED***")