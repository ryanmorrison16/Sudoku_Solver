import copy

from functions import *



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
            if r == row_num:
                options_removed += updateRow(tracker, r, [col_num], value)
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

    return options_removed



def updateColumn(tracker, row_nums : list, col_num : int, value : int):
    options_removed = 0

    for r, row in enumerate(tracker):
        if (r not in row_nums) and (value in row[col_num]):
            row[col_num].remove(value)
            options_removed += 1
            if len(row[col_num]) == 1: 
                options_removed += updateGame(tracker, r, col_num, row[col_num][0])

    return options_removed



def updateSquare(tracker, cells : list, values : list):
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
                        if len(tracker[r][c]) == 1: 
                            options_removed += updateGame(tracker, r, c, num)

    return options_removed



def simpleSolve(tracker):
    """
        Solves loners in rows, columns, and squares

        Solving all axis at same time creates issues (eg. solving a row loner messes up col loners)
    """

    def solveRowLoners(tracker) -> int:
        all_row_loners = []

        for r, row in enumerate(tracker):
            row_loners = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]}
            for c, cell in enumerate(row):
                if len(cell) > 1:
                    for value in cell:
                        if value in row_loners.keys():
                            if not row_loners[value]: row_loners[value].append((r,c))
                            else: del row_loners[value]
                else: del row_loners[cell[0]]

            if row_loners: all_row_loners.extend({value : cell[0]} for value, cell in row_loners.items())

        return updateFor(all_row_loners, "row")

        
    def solveColLoners(tracker) -> int:
        col_loners = {c : {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]} 
                      for c in range(0,9)}

        for r, row in enumerate(tracker):
            for c, cell in enumerate(row):
                if len(cell) > 1:
                    for value in cell:
                        if value in col_loners[c].keys():
                            if len(col_loners[c][value]) == 0: col_loners[c][value].append((r,c))
                            else: del col_loners[c][value]
                else: del col_loners[c][cell[0]]

        all_col_loners = [{value : cell[0]} for col_num in col_loners.values() for value, cell in col_num.items()]

        return updateFor(all_col_loners, "column")
    

    def solveSquareLoners(tracker) -> int:
        all_square_loners = []

        for square_row in [0,3,6]:
            for square_col in [0,3,6]:
                square_loners = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]}

                for r in range(square_row, square_row+3):
                    for c in range(square_col, square_col +3):
                        if len(tracker[r][c]) > 1:
                            for num in tracker[r][c]:
                                if num in square_loners.keys():
                                    if len(square_loners[num]) == 0: square_loners[num].append((r,c))
                                    else: del square_loners[num]
                        else: del square_loners[tracker[r][c][0]]

                all_square_loners.extend({value : cell[0]} for value, cell in square_loners.items())

        return updateFor(all_square_loners, "square")
    

    def updateFor(all_loners : list, plane : str):
        solved = 0
        options_removed = 0

        if len(all_loners) != 0:
            if SHOWDETAILS: print(f"{plane.upper()} LONERS: {all_loners}")
              
            for loner in all_loners:
                (value, cell), = loner.items()
                row, col = cell
                options_removed += len(tracker[row][col]) - 1
                tracker[row][col] = [value]
                solved += 1
                options_removed += updateGame(tracker, row, col, value)
                
            if SHOWDETAILS and options_removed: print(f"Removed {RED}{options_removed}{END} options")
            if SHOWSTEPS: print(f"Solved {GREEN}{solved}{END} {plane.title()} Loners")

        return options_removed

    return solveRowLoners(tracker) + solveColLoners(tracker) + solveSquareLoners(tracker)



def complexSolve(tracker):  # CAN COMBINE THESE
    """
        For complex techniques such as the X-Wing, Skyscraper, etc
    """

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
                for r in range(square_row, square_row + 3):
                    for c in range(square_col, square_col + 3):
                        if tuple(tracker[r][c]) in square.keys(): square[tuple(tracker[r][c])].append((r,c))
                        else: square[tuple(tracker[r][c])] = [(r,c)]

                for values, cells in square.items():
                    if (len(cells) > 1) and (len(values) == len(cells)):
                        options_removed += updateSquare(tracker, cells, values)
                        solved += 1
                        if SHOWDETAILS: print(f"Square {(square_row + 1) + (square_col // 3)} Duplicates: {values}")
        
        if SHOWSTEPS and solved: print(f"Found {GREEN}{solved}{END} Square Duplicates")

        return options_removed
    

    def inLineSquare(tracker):
        options_removed = 0
        solved = 0
        if SHOWDETAILS: all_inline = []

        for square_row in [0,3,6]:
            for square_col in [0,3,6]:
                square = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]}
                for r in range(square_row, square_row + 3):
                    for c in range(square_col, square_col + 3):
                        if len(tracker[r][c]) > 1:
                            for value in tracker[r][c]:
                                square[value].append((r,c))

                for value, cells in square.items():
                    removed_from_row = 0
                    removed_from_col = 0

                    if len(cells) > 1:
                        if all(cell[0] == cells[0][0] for cell in cells):
                            removed_from_row = updateRow(tracker, cells[0][0], [cell[1] for cell in cells], value)
                            if removed_from_row:
                                solved += 1
                                if SHOWDETAILS: all_inline.append(f"Row {cells[0][0]}: {value}")
                        if all(cell[1] == cells[0][1] for cell in cells):
                            removed_from_col = updateColumn(tracker, [cell[0] for cell in cells], cells[0][1], value)
                            if removed_from_col:
                                solved += 1
                                if SHOWDETAILS: all_inline.append(f"Col {cells[0][1]}: {value}")

                        options_removed += removed_from_row + removed_from_col

        if SHOWSTEPS and solved: print(f"Found {GREEN}{solved}{END} In-Line Square Duplicates")
        if SHOWDETAILS and all_inline: print(f"ALL INLINES: {all_inline}")

        return options_removed
    

    return samePairInSquare(tracker) + inLineSquare(tracker)
    


def makeGuesses(tracker, attempt_num):
    """
    Only guessing from one cell (with the fewest guesses) - guesses from other cells can be made in recursive calls (but 1 of cell_to_guess_from values HAS to be correct)
    """
    options_removed = 0
    cell_to_guess_from = ["(r,c)", "[1,2,3,4,5,6,7,8,9]"]   #template, is replaced on first iteration (by cell with less values)

    for r, row in enumerate(tracker):
        for c, cell in enumerate(row):
            if (len(cell) > 1) and (len(cell) < len(cell_to_guess_from[1])):
                cell_to_guess_from = [(r, c), cell]
                if len(cell) == 2: break

    if SHOWDETAILS: print(f"POSSIBLE GUESSES FOR {cell_to_guess_from[0]} - {cell_to_guess_from[1]}")
    cell, possible_guesses = cell_to_guess_from
    row, col = cell

    for guess in possible_guesses:
        if SHOWSTEPS: print(f"{PURPLE}GUESS{END}: {cell} - {guess}")
        attempt = copy.deepcopy(tracker)
        attempt[row][col] = [guess]
        options_removed += len(possible_guesses) - 1
        options_removed += updateGame(attempt, row, col, guess)
        if SHOWDETAILS: print(f"Removed {RED}{options_removed}{END} options with guess\n")

        try:
            solveGame(attempt)
        except Exception as e:
            if SHOWSTEPS:
                print(f"\n{PURPLE}PREVIOUS GUESS FAILED{END} - {e}")
                if guess != possible_guesses[-1]: print(f"{PURPLE}NEXT ", end="")
            continue

        if checkSolution(attempt):
            for r, row in enumerate(attempt):
                for c in range(len(row)):
                    tracker[r][c] = [attempt[r][c][0]]
            return options_removed
    
    raise Exception(f"ALL GUESSES FAILED - GOING BACK A GUESS")



def solveGame(tracker, attempt_num):
    options_left = optionsLeft(tracker)
    options_removed = 0
    
    while options_left:
        attempt_num += 1
        if SHOWSTEPS:
            print(f"\nAttempt {BLUE}{attempt_num}{END}")
            print(f"SOLVED: {GREEN}{numSolved(tracker)}{END} \t LEFT: {RED}{options_left}{END}")
            if True: printTracker(tracker)

        options_removed = simpleSolve(tracker)
        if not options_removed: options_removed += complexSolve(tracker)
        if SHOWSTEPS: print(f"\nRemoved {RED}{options_removed}{END} options\n")

        if options_removed:
            options_left -= options_removed
            if options_left < 0: 
                raise Exception(f"{RED}ERROR{END} | solveGame | {RED}NEGATIVE OPTIONS_LEFT{END}")
            continue
        else:
            options_removed = makeGuesses(tracker)
            break


if __name__ == "__main__":
    from games import *
    test_game = GAMES["MED"]
    test = makeTracker(test_game)
    printBoard(test)
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
    print(checkSolution(test))
    print(checkAltered(test, test_game))
    print("\n***PASSED***")