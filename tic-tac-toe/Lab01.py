# 1. Name:
#      -Daniel Wahlquist-
# 2. Assignment Name:
#      Lab 01: Tic-Tac-Toe
# 3. Assignment Description:
#      Play the game of Tic-Tac-Toe
# 4. What was the hardest part? Be as specific as possible.
#      -The hardest part for me was just trying to understand the logic of the existing pieces to the program, and then work with those pieces to create the 
#       new logic for it to complete the assignment. so intergration was essentially the hardest part, another hard part for me was just trying to see if the 
#       .json file was empty to begin with, and start with a new board, and so i asked co-pilot, what is a way i can tell if a file is empty in python, and it 
#       told me to use the .strip method to check. i also was unsure about whether we could add functions or not, but i did add a clear_board function to make 
#       clearing the board when someone wins, easier-
# 5. How long did it take for you to complete the assignment?
#      -it took me about two hours to complete, its somewhere around that time frame, give or take 30 min-

import json

# The characters used in the Tic-Tac-Too board.
# These are constants and therefore should never have to change.
X = 'X'
O = 'O'
BLANK = ' '

# A blank Tic-Tac-Toe board. We should not need to change this board;
# it is only used to reset the board to blank. This should be the format
# of the code in the JSON file.
blank_board = {  
            "board": [
                BLANK, BLANK, BLANK,
                BLANK, BLANK, BLANK,
                BLANK, BLANK, BLANK ]
        }

def read_board(filename):
    '''Read the previously existing board from the file if it exists.'''
    # Put file reading code here.
    
    with open("board.json", 'rt') as file:
        board_data = file.read()
        if not board_data.strip():
            board = blank_board["board"]
        else:
            board = json.loads(board_data)["board"]
    return board


def save_board(filename, board):
    '''Save the current game to a file.'''
    # Put file writing code here.
    with open(filename, 'wt') as file:
        board_data = json.dumps({"board": board})
        file.write(board_data)



def display_board(board):
    '''Display a Tic-Tac-Toe board on the screen in a user-friendly way.'''
    # Put display code here.
    print("current board: ")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print(f"---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")  
    print(f"---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")



def is_x_turn(board):
    '''Determine whose turn it is.'''
    # Put code here determining if it is X's turn.
    x_count = board.count(X)
    o_count = board.count(O)
    if x_count <= o_count:
        return True
    else:
        return False
    
def clear_board(board):
    '''Clear the board to a blank state.'''
    # Put code here to clear the board.
    board = blank_board["board"]
    save_board("board.json", board)
    return board

def play_game(board):
    '''Play the game of Tic-Tac-Toe.'''
    # Put game play code here. Return False when the user has indicated they are done.
    running = True
    while running and not game_done(board):
        display_board(board)
        print("Enter q to quit, of number 1-9:")
        if is_x_turn(board):
            move = input("X> ")
        else: 
            move = input("O> ")
        if move.lower() == 'q':
            save_board("board.json", board)
            print("Game Saved")
            running = False
            
        elif move.isdigit() and 1 <= int(move) <= 9:
            move = int(move) - 1
            if board[move] == BLANK:
                if is_x_turn(board):
                    board[move] = X
                else:
                    board[move] = O
            else:
                print("That square is already taken!")
    return False

def game_done(board, message=False):
    '''Determine if the game is finished.
       Note that this function is provided as-is.
       You do not need to edit it in any way.
       If message == True, then we display a message to the user.
       Otherwise, no message is displayed. '''

    # Game is finished if someone has completed a row.
    for row in range(3):
        if board[row * 3] != BLANK and board[row * 3] == board[row * 3 + 1] == board[row * 3 + 2]:
            if message:
                print("The game was won by", board[row * 3])
            return True

    # Game is finished if someone has completed a column.
    for col in range(3):
        if board[col] != BLANK and board[col] == board[3 + col] == board[6 + col]:
            if message:
                print("The game was won by", board[col])
            return True

    # Game is finished if someone has a diagonal.
    if board[4] != BLANK and (board[0] == board[4] == board[8] or
                              board[2] == board[4] == board[6]):
        if message:
            print("The game was won by", board[4])
        return True

    # Game is finished if all the squares are filled.
    tie = True
    for square in board:
        if square == BLANK:
            tie = False
    if tie:
        if message:
            print("The game is a tie!")
        return True


    return False

# These user-instructions are provided and do not need to be changed.
print("Enter 'q' to suspend your game. Otherwise, enter a number from 1 to 9")
print("where the following numbers correspond to the locations on the grid:")
print(" 1 | 2 | 3 ")
print("---+---+---")
print(" 4 | 5 | 6 ")
print("---+---+---")
print(" 7 | 8 | 9 \n")
print("The current board is:")

if __name__ == "__main__":

    board = read_board("board.json")
    game_running = True
    while game_running:
        game_running = play_game(board)
    display_board(board)
    if game_done(board, True):
        clear_board(board)

# The file read code, game loop code, and file close code goes here.
