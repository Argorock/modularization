import json
import random
import copy


def create_empty_board():
    return [[0 for _ in range(9)] for _ in range(9)]

def is_valid(board, row, col, num):
    for c in range(9):
        if board[row][c] == num:
            return False
    for r in range(9):
        if board[r][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if board[r][c] == num:
                return False
    return True

def fill_board(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if fill_board(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def save_board(board):
    with open("new_game.json", 'w') as file:
        json.dump({"board": board}, file, indent=2)

def count_solutions(board, limit=2):
    def helper(b, count):
        min_candidates = 10
        target_cell = None
        candidate_dict = {}
        for row in range(9):
            for col in range(9):
                if b[row][col] == 0:
                    candidates = [num for num in range(1, 10) if is_valid(b, row, col, num)]
                    candidate_dict[(row, col)] = candidates
                    if len(candidates) < min_candidates:
                        min_candidates = len(candidates)
                        target_cell = (row, col)
        if not target_cell:
            return count + 1
        row, col = target_cell
        for num in candidate_dict[(row, col)]:
            b[row][col] = num
            count = helper(b, count)
            if count >= limit:
                b[row][col] = 0
                return count
            b[row][col] = 0
        return count
    return helper(copy.deepcopy(board), 0)

def remove_numbers(board, difficulty="easy"):
    if difficulty == "easy" or difficulty == "1":
        cells_to_remove = random.randint(36, 40)
        max_empty_per_box = 4
    elif difficulty == "medium" or difficulty == "2":
        cells_to_remove = random.randint(46, 50)
        max_empty_per_box = 6
    elif difficulty == "hard" or difficulty == "3":
        cells_to_remove = random.randint(56, 60)
        max_empty_per_box = 9
    elif difficulty == "expert":
        cells_to_remove = random.randint(60, 64)
    else:
        cells_to_remove = random.randint(36, 40)
        max_empty_per_box = 4

    positions = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(positions)
    removed = 0

    def empty_in_box(row, col):
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        return sum(
            1 for r in range(start_row, start_row + 3)
              for c in range(start_col, start_col + 3)
              if board[r][c] == 0
        )

    for row, col in positions:
        if removed >= cells_to_remove:
            break
        if board[row][col] != 0:
            backup = board[row][col]
            board[row][col] = 0
            if count_solutions(board, limit=2) == 1:
                removed += 1
            else:
                board[row][col] = backup
    return board


def custom_board_main():
    board = create_empty_board()
    fill_board(board)
    difficulty = input("Choose difficulty (easy, medium, hard) (1-3): ").lower()
    board = remove_numbers(board, difficulty)
    save_board(board)
    print("Custom board created and saved as 'new_game'.")

