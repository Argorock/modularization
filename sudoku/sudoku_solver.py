import json
from make_sudoku_board import is_valid
import copy


# Load the board from a json file
def load_board(file_name):
    with open(f"{file_name}.json", "r") as file:
        data = json.load(file)
        return data["board"]

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

