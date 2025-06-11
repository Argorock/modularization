import json
from make_sudoku_board import is_valid
import copy


# Load the board from a json file
def load_board(file_name):
    with open(f"{file_name}.json", "r") as file:
        data = json.load(file)
        return data["board"]
    
def naked_singles(board, candidates):
    """Find and place naked singles dynamically after every solving step."""
    progress = False

    while True:  # Continuously check for new naked singles
        found_naked_single = False

        for r in range(9):
            for c in range(9):
                # Skip cells that already contain a number
                if board[r][c] != 0:
                    continue

                # Ensure the cell has exactly ONE candidate before placing
                if len(candidates[r][c]) != 1:
                    continue  # Skip this cell if it has multiple candidates

                num = next(iter(candidates[r][c]))  # Extract the single number

                # **Validation Step:** Ensure placing this number doesn't break the board
                if num in board[r] or any(board[k][c] == num for k in range(9)):
                    print(f"❌ ERROR: Invalid placement attempted at ({r+1},{c+1}) for {num}")
                    continue  # Skip this placement

                print(f"Naked single placed at ({r+1},{c+1}): {num}")

                # **Commit the placement**
                board[r][c] = num
                candidates[r][c] = set()  # Clear candidates for this cell

                # **Update candidate lists for row, column, and box**
                for k in range(9):
                    if num in candidates[r][k]:
                        candidates[r][k].discard(num)
                    if num in candidates[k][c]:
                        candidates[k][c].discard(num)

                br, bc = 3 * (r // 3), 3 * (c // 3)
                for dr in range(3):
                    for dc in range(3):
                        if num in candidates[br+dr][bc+dc]:
                            candidates[br+dr][bc+dc].discard(num)

                found_naked_single = True  # A naked single was placed, so continue checking
                progress = True

        if not found_naked_single:
            break  # Exit the loop when no more naked singles are found

    return progress, board

def hidden_singles(board, candidates):
    """Find and place hidden singles, ensuring they are truly the only option for a number in a row, column, or box."""
    progress = False

    # Rows
    for r in range(9):
        for num in range(1, 10):
            places = [c for c in range(9) if board[r][c] == 0 and num in candidates[r][c]]
            if len(places) == 1:  # Hidden single detected!
                c = places[0]
                board[r][c] = num
                candidates[r][c] = set()  # Clear candidates for this cell

                # **Update candidate lists for row, column, and box**
                for k in range(9):
                    candidates[r][k].discard(num)  # Remove from row
                    candidates[k][c].discard(num)  # Remove from column

                # Remove from box
                br, bc = 3 * (r // 3), 3 * (c // 3)
                for dr in range(3):
                    for dc in range(3):
                        candidates[br+dr][bc+dc].discard(num)

                progress = True

    # Columns
    for c in range(9):
        for num in range(1, 10):
            places = [r for r in range(9) if board[r][c] == 0 and num in candidates[r][c]]
            if len(places) == 1:  # Hidden single detected!
                r = places[0]
                board[r][c] = num
                candidates[r][c] = set()  # Clear candidates for this cell

                # **Update candidate lists for row, column, and box**
                for k in range(9):
                    candidates[r][k].discard(num)  # Remove from row
                    candidates[k][c].discard(num)  # Remove from column

                # Remove from box
                br, bc = 3 * (r // 3), 3 * (c // 3)
                for dr in range(3):
                    for dc in range(3):
                        candidates[br+dr][bc+dc].discard(num)

                progress = True

    # Boxes
    for box_r in range(3):
        for box_c in range(3):
            for num in range(1, 10):
                cells = [(box_r * 3 + dr, box_c * 3 + dc) for dr in range(3) for dc in range(3)
                         if board[box_r * 3 + dr][box_c * 3 + dc] == 0 and num in candidates[box_r * 3 + dr][box_c * 3 + dc]]

                if len(cells) == 1:  # Hidden single detected!
                    r, c = cells[0]
                    board[r][c] = num
                    candidates[r][c] = set()  # Clear candidates for this cell

                    # **Update candidate lists for row, column, and box**
                    for k in range(9):
                        candidates[r][k].discard(num)  # Remove from row
                        candidates[k][c].discard(num)  # Remove from column

                    # Remove from box
                    br, bc = 3 * (r // 3), 3 * (c // 3)
                    for dr in range(3):
                        for dc in range(3):
                            candidates[br+dr][bc+dc].discard(num)

                    progress = True

    return progress, board



def find_hidden_pairs(candidates):
    """Find and eliminate hidden pairs in rows, columns, and boxes."""
    found = False
    processed_pairs = set()  # Track modified cells to avoid repeated detections

    # Rows
    for r in range(9):
        for n1 in range(1, 10):
            for n2 in range(n1+1, 10):
                cells_n1 = [c for c in range(9) if n1 in candidates[r][c]]
                cells_n2 = [c for c in range(9) if n2 in candidates[r][c]]

                if len(cells_n1) == 2 and cells_n1 == cells_n2:
                    for c in cells_n1:
                        before = set(candidates[r][c])
                        if before == {n1, n2} or (r, c, n1, n2) in processed_pairs:
                            continue  # Skip if already processed
                        candidates[r][c] = {n1, n2}
                        processed_pairs.add((r, c, n1, n2))
                        if candidates[r][c] != before:
                            print(f"Hidden pair applied at ({r+1},{c+1}): {before} → {candidates[r][c]}")
                            found = True

                    # Remove {n1, n2} from other cells in the row
                    for other_c in range(9):
                        if other_c not in cells_n1:
                            candidates[r][other_c] -= {n1, n2}

    # Columns
    for c in range(9):
        for n1 in range(1, 10):
            for n2 in range(n1+1, 10):
                cells_n1 = [r for r in range(9) if n1 in candidates[r][c]]
                cells_n2 = [r for r in range(9) if n2 in candidates[r][c]]

                if len(cells_n1) == 2 and cells_n1 == cells_n2:
                    for r in cells_n1:
                        before = set(candidates[r][c])
                        if before == {n1, n2} or (r, c, n1, n2) in processed_pairs:
                            continue
                        candidates[r][c] = {n1, n2}
                        processed_pairs.add((r, c, n1, n2))
                        if candidates[r][c] != before:
                            print(f"Hidden pair applied at ({r+1},{c+1}): {before} → {candidates[r][c]}")
                            found = True

                    # Remove {n1, n2} from other cells in the column
                    for other_r in range(9):
                        if other_r not in cells_n1:
                            candidates[other_r][c] -= {n1, n2}

    # Boxes
    for box_r in range(3):
        for box_c in range(3):
            for n1 in range(1, 10):
                for n2 in range(n1+1, 10):
                    cells_n1 = []
                    cells_n2 = []
                    for dr in range(3):
                        for dc in range(3):
                            r = box_r * 3 + dr
                            c = box_c * 3 + dc
                            if n1 in candidates[r][c]:
                                cells_n1.append((r, c))
                            if n2 in candidates[r][c]:
                                cells_n2.append((r, c))

                    if len(cells_n1) == 2 and cells_n1 == cells_n2:
                        for (r, c) in cells_n1:
                            before = set(candidates[r][c])
                            if before == {n1, n2} or (r, c, n1, n2) in processed_pairs:
                                continue
                            candidates[r][c] = {n1, n2}
                            processed_pairs.add((r, c, n1, n2))
                            if candidates[r][c] != before:
                                print(f"Hidden pair applied at ({r+1},{c+1}): {before} → {candidates[r][c]}")
                                found = True

                        # Remove {n1, n2} from other cells in the box
                        for dr in range(3):
                            for dc in range(3):
                                r = box_r * 3 + dr
                                c = box_c * 3 + dc
                                if (r, c) not in cells_n1:
                                    candidates[r][c] -= {n1, n2}

    return found

def find_naked_pairs(candidates):
    found = False
    techniques_used = set()

    # Track naked pairs
    naked_pairs_rows = [{} for _ in range(9)]
    naked_pairs_cols = [{} for _ in range(9)]
    naked_pairs_boxes = [[{} for _ in range(3)] for _ in range(3)]

    # Step 1: Identify naked pairs
    for r in range(9):
        for c in range(9):
            if len(candidates[r][c]) == 2:
                pair_key = frozenset(candidates[r][c])  # Hashable set for easy lookup
                naked_pairs_rows[r].setdefault(pair_key, []).append(c)
                naked_pairs_cols[c].setdefault(pair_key, []).append(r)
                naked_pairs_boxes[r // 3][c // 3].setdefault(pair_key, []).append((r, c))

    # Helper function to safely remove candidates
    def remove_from_candidates(targets, pair, location_type, loc1, loc2):
        for r, c in targets:
            before = set(candidates[r][c])
            if len(candidates[r][c] - pair) > 0:  # Ensure at least one value remains
                candidates[r][c] -= pair
                if candidates[r][c] != before:
                    print(f"Naked pair elimination at {location_type} ({loc1+1},{loc2+1}) affecting ({r+1},{c+1}): {before} → {candidates[r][c]}")
                    techniques_used.add("naked_pair")
                    nonlocal found
                    found = True

    # Step 2: Apply eliminations in rows
    for r in range(9):
        for pair, cols in naked_pairs_rows[r].items():
            if len(cols) == 2:  # Naked pair detected
                remove_from_candidates([(r, c) for c in range(9) if c not in cols], pair, "row", r, cols[0])

    # Step 2: Apply eliminations in columns
    for c in range(9):
        for pair, rows in naked_pairs_cols[c].items():
            if len(rows) == 2:  # Naked pair detected
                remove_from_candidates([(r, c) for r in range(9) if r not in rows], pair, "column", c, rows[0])

    # Step 2: Apply eliminations in boxes
    for box_r in range(3):
        for box_c in range(3):
            for pair, positions in naked_pairs_boxes[box_r][box_c].items():
                if len(positions) == 2:  # Naked pair detected
                    remove_from_candidates(
                        [(rr, cc) for rr in range(box_r * 3, box_r * 3 + 3) for cc in range(box_c * 3, box_c * 3 + 3) 
                         if (rr, cc) not in positions],
                        pair, "box", box_r, box_c
                    )

    return found

def find_pointing_pairs(candidates):
    """Eliminate candidates using pointing pairs/triples."""
    found = False
    for digit in range(1, 10):
        for box_r in range(3):
            for box_c in range(3):
                cells = [(box_r*3+dr, box_c*3+dc)
                         for dr in range(3) for dc in range(3)
                         if digit in candidates[box_r*3+dr][box_c*3+dc]]
                if len(cells) > 1:
                    rows = set(r for r, c in cells)
                    cols = set(c for r, c in cells)
                    if len(rows) == 1:
                        r = rows.pop()
                        for c in range(9):
                            if c // 3 != box_c and digit in candidates[r][c]:
                                candidates[r][c].remove(digit)
                                found = True
                    if len(cols) == 1:
                        c = cols.pop()
                        for r in range(9):
                            if r // 3 != box_r and digit in candidates[r][c]:
                                candidates[r][c].remove(digit)
                                found = True
    return found




def find_x_wing(candidates):
    for digit in range(1, 10):
        # Check rows
        for row1 in range(9):
            cols1 = [c for c in range(9) if digit in candidates[row1][c]]
            if len(cols1) == 2:
                for row2 in range(row1+1, 9):
                    cols2 = [c for c in range(9) if digit in candidates[row2][c]]
                    if cols1 == cols2:
                        # X-Wing found
                        for r in range(9):
                            if r != row1 and r != row2:
                                for c in cols1:
                                    if digit in candidates[r][c]:
                                        candidates[r][c].remove(digit)
                                        # Log that X-Wing was used
                        return True  # Found and applied X-Wing
    return False

def find_swordfish(candidates):
    found = False
    for digit in range(1, 10):
        # Check rows
        rows_with_digit = []
        for r in range(9):
            cols = [c for c in range(9) if digit in candidates[r][c]]
            if 2 <= len(cols) <= 3:
                rows_with_digit.append((r, cols))
        for i in range(len(rows_with_digit)):
            for j in range(i+1, len(rows_with_digit)):
                for k in range(j+1, len(rows_with_digit)):
                    cols_union = set(rows_with_digit[i][1]) | set(rows_with_digit[j][1]) | set(rows_with_digit[k][1])
                    if len(cols_union) == 3:
                        for r in range(9):
                            if r not in [rows_with_digit[i][0], rows_with_digit[j][0], rows_with_digit[k][0]]:
                                for c in cols_union:
                                    if digit in candidates[r][c]:
                                        candidates[r][c].remove(digit)
                                        found = True
    return found



def solve_with_techniques(board):
    import copy
    b = copy.deepcopy(board)
    techniques_used = set()
    error_map = {}  # Tracks placement errors

    # Step 1: Initialize candidates
    candidates = [[set() if b[r][c] != 0 else {num for num in range(1, 10) if is_valid(b, r, c, num)}
                   for c in range(9)] for r in range(9)]

    progress = True
    max_iterations = 10  # Safety limit
    iteration_count = 0

    while progress:
        iteration_count += 1
        if iteration_count > max_iterations:
            print("WARNING: Loop exceeded max iterations!")
            break

        progress = False

        # **Step 2: Apply Naked & Hidden Singles with Validation**
        for technique_func, name in [
            (naked_singles, "naked_single"),
            (hidden_singles, "hidden_single"),
            (find_naked_pairs, "naked_pair")  # Ensure it's correctly passed
        ]:
            before_board = copy.deepcopy(b)
            if technique_func(b, candidates) if technique_func is not find_naked_pairs else technique_func(candidates):
                techniques_used.add(name)
                progress = True


            # Validate all placements made in this iteration
            for r in range(9):
                for c in range(9):
                    if before_board[r][c] == 0 and b[r][c] != 0:  # Newly placed number
                        if not validate_placement(b, r, c, b[r][c]):
                            correct_number = get_correct_number(r, c, board)  # Use backwards solver
                            error_map[(r, c)] = (b[r][c], correct_number)  # Store incorrect & correct number

        # **Step 3: Verify Board Is Still Solvable**
        if not validate_sudoku(b):
            print("❌ ERROR: Board state is unsolvable at this stage!")
            break

        # **Step 4: Exit Conditions**
        if all(b[r][c] != 0 for r in range(9) for c in range(9)):
            break

    return all(b[r][c] != 0 for r in range(9) for c in range(9)), techniques_used, b, error_map
    import copy
    b = copy.deepcopy(board)
    techniques_used = set()
    error_map = {}  # Tracks placement errors

    # Step 1: Initialize candidates
    candidates = [[set() if b[r][c] != 0 else {num for num in range(1, 10) if is_valid(b, r, c, num)}
                   for c in range(9)] for r in range(9)]

    progress = True
    max_iterations = 10  # Safety limit
    iteration_count = 0

    while progress:
        iteration_count += 1
        if iteration_count > max_iterations:
            print("WARNING: Loop exceeded max iterations!")
            break

        progress = False

        # **Step 2: Apply Naked & Hidden Singles with Validation**
        for technique_func, name in [
            (naked_singles, "naked_single"),
            (hidden_singles, "hidden_single"),
        ]:
            before_board = copy.deepcopy(b)
            if technique_func(b, candidates):
                techniques_used.add(name)
                progress = True

            # Validate all placements made in this iteration
            for r in range(9):
                for c in range(9):
                    if before_board[r][c] == 0 and b[r][c] != 0:  # Newly placed number
                        if not validate_placement(b, r, c, b[r][c]):
                            correct_number = get_correct_number(r, c, board)  # Use backwards solver
                            error_map[(r, c)] = (b[r][c], correct_number)  # Store incorrect & correct number

        # **Step 3: Verify Board Is Still Solvable**
        if not validate_sudoku(b):
            print("❌ ERROR: Board state is unsolvable at this stage!")
            break

        # **Step 4: Exit Conditions**
        if all(b[r][c] != 0 for r in range(9) for c in range(9)):
            break

    return all(b[r][c] != 0 for r in range(9) for c in range(9)), techniques_used, b, error_map



def validate_placement(board, row, col, num):
    """Check if placing `num` at (row, col) follows Sudoku rules."""
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False  # Number already exists in row or column

    box_r, box_c = 3 * (row // 3), 3 * (col // 3)
    for dr in range(3):
        for dc in range(3):
            if board[box_r + dr][box_c + dc] == num:
                return False  # Number already exists in its box
                
    return True

def place_number_with_tracking(board, row, col, num, error_map):
    """Places a number and marks mistakes instead of blocking execution."""
    if validate_placement(board, row, col, num):
        board[row][col] = num  # Correct placement
    else:
        error_map[(row, col)] = num  # **Mark incorrect placement**

def test_solver_with_markers(board, techniques):
    """Runs solver techniques and tracks errors instead of stopping execution."""
    error_map = {}  # Stores incorrect placements
    
    for technique in techniques:
        technique(board, error_map)  # Apply each technique with tracking
    
    return error_map

def get_correct_number(row, col, board):
    """Use backwards solver to determine correct placement for a given cell."""
    test_board = copy.deepcopy(board)
    if solve_sudoku(test_board):
        return test_board[row][col]
    return None  # If backwards solver fails, return None

def validate_sudoku(board):
    """Checks if a valid solution exists given the current board state without placing numbers."""
    from copy import deepcopy

    test_board = deepcopy(board)  # Avoid modifying the original board
    return solve_sudoku(test_board) 

# uses mrv (minimun remaining values) to solve the sudoku board
# returns True if sovled, False if not solvable
def solve_sudoku(board):
    min_candidates = 10
    target_cell = None
    candidate_dict = {}
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                candidates = [num for num in range(1, 10) if is_valid(board, row, col, num)]
                candidate_dict[(row, col)] = candidates
                if len(candidates) < min_candidates:
                    min_candidates = len(candidates)
                    target_cell = (row, col)
                if min_candidates == 0:
                    return False
    if not target_cell:
        return True
    row, col = target_cell
    for num in candidate_dict[(row, col)]:
        board[row][col] = num
        if solve_sudoku(board):
            return True
        board[row][col] = 0
    return False

#displays the solved sudoku board in the table format
def display_board_table(board):
    print("    A B C   D E F   G H I")
    print("  -------------------------")

    for i, row in enumerate(board, start = 1):
        print(f"{i} | {row[0]} {row[1]} {row[2]} | {row[3]} {row[4]} {row[5]} | {row[6]} {row[7]} {row[8]} |")
        if i % 3 == 0 and i != 9:
            print("  -------------------------")
    print("  -------------------------")

def solve_board_main(file_name):
    board = load_board(file_name)
    solve_sudoku(board)
    display_board_table(board)


def run_tests():
    test_boards = [
        # Board 1: Tests only Naked Singles
# [
#     [5, 3, 4, 6, 7, 8, 9, 1, 2],
#     [6, 7, 2, 1, 9, 5, 3, 4, 8],
#     [1, 9, 8, 3, 4, 2, 5, 6, 7],
#     [8, 5, 9, 7, 6, 1, 4, 2, 3],  
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [7, 1, 3, 9, 2, 4, 8, 5, 6],  
#     [9, 6, 1, 5, 3, 7, 2, 8, 4],  
#     [2, 8, 7, 4, 1, 9, 6, 3, 5],  
#     [3, 4, 5, 2, 8, 6, 1, 7, 9]  
# ],
# [
#     [5, 3, 4, 6, 7, 8, 9, 0, 2],  
#     [6, 7, 2, 1, 9, 5, 3, 0, 8],  
#     [1, 9, 8, 3, 4, 2, 5, 0, 7],  
#     [8, 5, 9, 7, 6, 1, 4, 0, 3],  
#     [4, 2, 6, 8, 5, 3, 7, 0, 1],  
#     [7, 1, 3, 9, 2, 4, 8, 0, 6],  
#     [9, 6, 1, 5, 3, 7, 2, 0, 4],  
#     [2, 8, 7, 4, 1, 9, 6, 0, 5],  
#     [3, 4, 5, 2, 8, 6, 1, 0, 9]  
# ],
# [
#     [5, 3, 4, 6, 7, 8, 9, 1, 2],  
#     [6, 7, 2, 1, 9, 5, 3, 4, 8],  
#     [1, 9, 8, 3, 4, 2, 5, 6, 7],  
#     [8, 5, 9, 7, 6, 1, 4, 2, 3],  
#     [4, 2, 6, 8, 5, 3, 7, 9, 1],  
#     [7, 1, 3, 9, 2, 4, 8, 5, 6],  
#     [9, 6, 1, 5, 3, 7, 0, 0, 0],  
#     [2, 8, 7, 4, 1, 9, 0, 0, 0],  
#     [3, 4, 5, 2, 8, 6, 0, 0, 0]  
# ],
#     [
#     [5, 3, 0, 0, 7, 0, 0, 0, 0],
#     [6, 0, 0, 1, 9, 5, 0, 0, 0],
#     [0, 9, 8, 0, 0, 0, 0, 6, 0],
#     [8, 0, 0, 0, 6, 0, 0, 0, 3],
#     [4, 0, 0, 8, 0, 3, 0, 0, 1],
#     [7, 0, 0, 0, 2, 0, 0, 0, 6],
#     [0, 6, 0, 0, 0, 0, 2, 8, 0],
#     [0, 0, 0, 4, 1, 9, 0, 0, 5],
#     [0, 0, 0, 0, 8, 0, 0, 7, 9]
# ],
        # Board 3: Tests Naked Singles, Hidden Singles, & Hidden Pairs
# [
#     [0, 0, 3, 0, 2, 0, 6, 0, 0],
#     [9, 0, 0, 3, 0, 5, 0, 0, 1],
#     [0, 0, 1, 8, 0, 6, 4, 0, 0],
#     [0, 0, 8, 1, 0, 2, 9, 0, 0],
#     [7, 0, 0, 0, 0, 0, 0, 0, 8],
#     [0, 0, 6, 7, 0, 8, 2, 0, 0],
#     [0, 0, 2, 6, 0, 9, 5, 0, 0],
#     [8, 0, 0, 2, 0, 3, 0, 0, 9],
#     [0, 0, 5, 0, 1, 0, 3, 0, 0]
# ],
# [
#     [5, 3, 4, 6, 7, 8, 9, 1, 2],
#     [6, 7, 2, 1, 9, 5, 3, 4, 8],
#     [1, 9, 8, 3, 4, 2, 5, 6, 7],
#     [8, 5, 9, 0, 6, 1, 4, 2, 3],  # (4,4) removed
#     [4, 0, 6, 8, 0, 3, 7, 9, 1],  # (5,5) and (5,2) removed
#     [7, 1, 3, 9, 2, 4, 8, 5, 6],
#     [9, 6, 1, 5, 3, 7, 2, 8, 4],
#     [2, 8, 7, 4, 0, 9, 6, 3, 5],  # (8,5) removed
#     [3, 4, 5, 2, 8, 6, 1, 7, 9]
# ]

    # an eventual implementation for lots of different techniques
# [
#     [0, 0, 6, 0, 0, 0, 1, 0, 0],
#     [0, 9, 0, 0, 0, 5, 0, 0, 8],
#     [5, 0, 0, 0, 7, 0, 0, 0, 3],
#     [0, 7, 0, 0, 0, 0, 0, 0, 1],
#     [0, 0, 0, 6, 0, 2, 0, 0, 0],
#     [3, 0, 0, 0, 0, 0, 0, 7, 0],
#     [4, 0, 0, 0, 9, 0, 0, 0, 6],
#     [7, 0, 0, 3, 0, 0, 0, 2, 0],
#     [0, 0, 1, 0, 0, 0, 9, 0, 0]
# ]
[
    [0, 0, 0, 2, 0, 0, 0, 6, 3],  
    [3, 0, 0, 0, 0, 5, 4, 0, 0],  
    [0, 0, 1, 0, 0, 3, 0, 0, 0],  
    [0, 1, 0, 0, 0, 0, 0, 0, 6],  
    [0, 0, 0, 5, 0, 8, 0, 0, 0],  
    [4, 0, 0, 0, 0, 0, 0, 1, 0],  
    [0, 0, 0, 3, 0, 0, 1, 0, 0],  
    [0, 0, 5, 7, 0, 0, 0, 0, 8],  
    [9, 3, 0, 0, 0, 6, 0, 0, 0]  
]
    ]
    # Running tests dynamically
    for i, board in enumerate(test_boards, start=1):
        print(f"\n🔎 Running test on Board {i}...")
        solved, techniques_used, solved_board, error_map = solve_with_techniques(board)  # Include error tracking

        if solved:
            print(f"✅ Board {i} solved successfully! No issues detected.\n")
        else:
            print(f"❌ Board {i} not solved.")
        
        print(f"Techniques used: {techniques_used}")

        # Display error markers with correct numbers
        if error_map:
            print("⚠️ Incorrect placements detected:")
            for (r, c), (incorrect, correct) in error_map.items():
                if correct:
                    print(f"  ❌ Cell ({r+1},{c+1}) placed {incorrect} incorrectly. Expected: {correct}.")
                else:
                    print(f"  ❌ Cell ({r+1},{c+1}) placed {incorrect} incorrectly. No valid correction found.")

        display_board_table(solved_board)  # Assuming function prints board neatly



# Run the test suite
run_tests()