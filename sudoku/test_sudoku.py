
import pytest
import make_sudoku_board
import sudoku_solver
# import random

# random.seed(42) # to enusre consistent results for testing

def test_puzzle_solves_to_original_solution():
    solution_board = make_sudoku_board.create_empty_board()
    make_sudoku_board.fill_board(solution_board)

    import copy
    original_solution = copy.deepcopy(solution_board)

    puzzle = make_sudoku_board.remove_numbers(solution_board, "expert")

    solved_puzzle = copy.deepcopy(puzzle)
    sudoku_solver.solve_sudoku(solved_puzzle)


    assert solved_puzzle == original_solution, "Solved puzzle doesn't match the original solution"

def test_count_solutions():
    # Easy
    solution_board_easy = make_sudoku_board.create_empty_board()
    make_sudoku_board.fill_board(solution_board_easy)
    puzzle_easy = make_sudoku_board.remove_numbers(solution_board_easy, "easy")
    num_zeros_easy = sum(row.count(0) for row in puzzle_easy)
    assert 36 <= num_zeros_easy <= 40, f"Easy puzzle should have between 36 and 40 zeros, has {num_zeros_easy}"

    # Medium
    solution_board_medium = make_sudoku_board.create_empty_board()
    make_sudoku_board.fill_board(solution_board_medium)
    puzzle_medium = make_sudoku_board.remove_numbers(solution_board_medium, "medium")
    num_zeros_medium = sum(row.count(0) for row in puzzle_medium)
    assert 46 <= num_zeros_medium <= 50, f"Medium puzzle should have between 46 and 50 zeros, has {num_zeros_medium}"

    # Hard
    solution_board_hard = make_sudoku_board.create_empty_board()
    make_sudoku_board.fill_board(solution_board_hard)
    puzzle_hard = make_sudoku_board.remove_numbers(solution_board_hard, "expert")
    num_zeros_hard = sum(row.count(0) for row in puzzle_hard)
    assert 61 <= num_zeros_hard <= 64, f"Hard puzzle should have between 56 and 60 zeros, has {num_zeros_hard}"

if __name__ == "__main__":
    pytest.main(["-v", "--tb=line", "-rN", __file__])
