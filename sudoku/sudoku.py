import json


# Displays the sudoku board, while calling other functions to retrieve the board.
def display_board(file_name):
    # file_name = retrieve_valid_file_name()
    board = load_board(file_name)
    display_board_table(board)
    while True:
        coordinates = get_valid_board_values(board)
        if coordinates is None:
            break
        board = update_board_with_parsed_value(coordinates, board)
        display_board_table(board)

        
# parses the coordinate sytem input from the user, and checks if valid by updating the board.
def update_board_with_parsed_value(coordinates, board):
    if coordinates is None:
        return board
    row, col, value = coordinates
    board[row][col] = value
    return board

# Displays the sudoku board in a table format
def display_board_table(board):
    print("    A B C   D E F   G H I")
    print("  -------------------------")

    for i, row in enumerate(board, start = 1):
        display_row = [str(num) if num != 0 else '_' for num in row]
        print(f"{i} | {display_row[0]} {display_row[1]} {display_row[2]} | {display_row[3]} {display_row[4]} {display_row[5]} | {display_row[6]} {display_row[7]} {display_row[8]} |")
        if i % 3 == 0 and i != 9:
            print("  -------------------------")
    print("  -------------------------")


# Gets valid coordinates from the user
def get_valid_board_values(board):
    while True:
        coordinates = input("Enter the coordinate and value: (A1 5), or q to quit: ").upper()
        if coordinates.lower() == "q":
            save_board(board)
            return None
        parts = coordinates.split()
        if len(parts) != 2:
            print("Invalid input Format")
            continue
        cell, value = parts

        if len(cell) == 2:
            if cell[0] in "ABCDEFGHI" and cell[1] in "123456789":
                col_letter = cell[0]
                row_number = cell[1]
            elif cell[0] in "123456789" and cell[1] in "ABCDEFGHI":
                col_letter = cell[1]
                row_number = cell[0]
            else:
                print("Invalid cell coordinates ")
                continue
        else:
            print("Invalid cell coordinates ")
            continue

        try:
            col = ord(col_letter) - ord("A")
            row = int(row_number) - 1
            value = int(value)

        except Exception:
            print("Invalid input.")
            continue

        valid, message = is_valid(board, row, col, value)
        if not valid:
            print(message)
            continue

        return(row, col, value)



# Saves the current board to a new file.
def save_board(board, file_name=None):
    file_name = input("Enter the new file name of where you want to save the board: ").lower()
    with open(f"{file_name}.json", "w") as file:
        json.dump({"board": board}, file, indent=2)
    print(f"Board saved to {file_name}.")
    

# Loads the board from a JSON file
def load_board(file_name):
    try:
        with open(file_name, "r") as file:
            data = json.load(file)
            return data["board"]
    except FileNotFoundError:
        # Check for keywords and open fallback files
        if "hard" in file_name.lower():
            with open("hard.json", "r") as file:
                data = json.load(file)
                return data["board"]
        elif "medium" in file_name.lower():
            with open("medium.json", "r") as file:
                data = json.load(file)
                return data["board"]
        elif "easy" in file_name.lower():
            with open("easy.json", "r") as file:
                data = json.load(file)
                return data["board"]
        else:
            print(f"File '{file_name}' not found and no fallback available.")
            raise
    

# checks if a move is valid
def is_valid(board, row, col, value):
    if not (0 <= row < 9 and 0 <= col < 9):
        return False, "Coordinates out of range."
    if not (1 <= value <= 9):
        return False, "Invalid number. Please enter a number from 1 to 9."
    if board[row][col] != 0:
        return False, f"Cell {chr(col+ord('A'))}{row+1} is already filled with {board[row][col]}."
    if value in board[row]:
        return False, f"Number {value} already exists in this row."
    if value in [board[r][col] for r in range(9)]:
        return False, f"Number {value} already exists in this column."
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if board[r][c] == value:
                return False, f"Number {value} already exists in this region."
    return True, ""

# retrieves a valid file name from the user
def retrieve_valid_file_name():
    while True:
        file_name = input("Enter the file name for the board: ").lower()
        try:
            with open(f"{file_name}.json", 'r'):
                pass
            return file_name
        except FileNotFoundError:
            print(f"Error 404, File {file_name} not found. ")



def main():
    print("Welcome to Sudoku")
    while True:
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")
        print("4. Load Saved Game")
        print("5. Custom Board")
        print("6. Solve Board")
        print("0. Exit")
        options = input("Choose an option (1-6): ")
        if  options == "1":
            display_board("131.05.Easy.json") # sudoku/easy.json for my own testing
        elif options == "2":
            display_board("131.05.Medium.json") # sudoku/medium.json
        elif options == "3":
            display_board("131.05.Hard.json") # sudoku/hard.json
        elif options == "4":
            file_name = retrieve_valid_file_name()
            display_board(file_name)
        elif options == "5":
            import make_sudoku_board
            make_sudoku_board.custom_board_main()
            display_board("new_game.json")
        elif options == "6":
            import sudoku_solver
            file_name = retrieve_valid_file_name()
            sudoku_solver.solve_board_main(file_name)
        elif options == "0":
            print("Leaving game... ")
            break
        else:
            print("Invalid option, please try again. ")
        

if __name__ == "__main__":
    main()