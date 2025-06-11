import pygame
import sys
import make_sudoku_board
import sudoku_solver
from make_sudoku_board import is_valid

# --- Settings ---
BOARD_MARGIN = 170
WIDTH, HEIGHT = 540, 600
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE
BUTTON_HEIGHT = 40
BUTTON_MARGIN = 20
BOTTOM_MARGIN = 2 * (BUTTON_HEIGHT + BUTTON_MARGIN)
FONT_SIZE = 36

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (90, 90, 90)

pygame.init()
screen = pygame.display.set_mode((WIDTH + 2 * BOARD_MARGIN, HEIGHT + BOTTOM_MARGIN + BOARD_MARGIN))
pygame.display.set_caption("Sudoku")
font = pygame.font.SysFont(None, FONT_SIZE)
button_font = pygame.font.SysFont(None, 28)
note_font = pygame.font.SysFont(None, 20)

def is_board_correct(user_board, solution, fixed_cells):
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if not fixed_cells[r][c]:
                if user_board[r][c] != solution[r][c]:
                    return False
    return True

def draw_board(board, selected, user_board=None, show_solution=False, check_solution=False, solution=None, fixed_cells=None, notes=None, hint_cells=None, highlight_number=None):
    screen.fill(WHITE)
    # Draw cell backgrounds and numbers first
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            rect = pygame.Rect(
                BOARD_MARGIN + c * CELL_SIZE,
                BOARD_MARGIN + r * CELL_SIZE,
                CELL_SIZE, CELL_SIZE
            )
            num = board[r][c]
            if highlight_number is not None and num != highlight_number:
                continue 
            # Shade hint cells green
            if hint_cells and (r, c) in hint_cells:
                pygame.draw.rect(screen, (180, 255, 180), rect)
            # Shade incorrect entries in red when showing solution
            elif show_solution and user_board is not None and solution is not None:
                if user_board[r][c] != 0 and user_board[r][c] != solution[r][c]:
                    pygame.draw.rect(screen, (255, 100, 100), rect)
                elif fixed_cells and fixed_cells[r][c]:
                    pygame.draw.rect(screen, (220, 220, 255), rect)
            # Shade incorrect entries in red when showing solution or checking solution
            elif (show_solution or check_solution) and user_board is not None and solution is not None:
                if user_board[r][c] != 0 and user_board[r][c] != solution[r][c]:
                    pygame.draw.rect(screen, (255, 100, 100), rect)
                elif fixed_cells and fixed_cells[r][c]:
                    pygame.draw.rect(screen, (220, 220, 255), rect)
            # Shade fixed cells (when not showing incorrect)
            elif fixed_cells and fixed_cells[r][c]:
                pygame.draw.rect(screen, (220, 220, 255), rect)
            # Shade invalid entries (live validity check)
            elif user_board is not None and not fixed_cells[r][c] and user_board[r][c] != 0:
                val = user_board[r][c]
                user_board[r][c] = 0
                invalid = not is_valid(user_board, r, c, val)
                user_board[r][c] = val
                if invalid:
                    pygame.draw.rect(screen, (255, 200, 80), rect)  # Orange for invalid

            num = board[r][c]
            if (show_solution or check_solution) and user_board is not None and solution is not None:
                # Show user's incorrect number in red cell
                if user_board[r][c] != 0 and user_board[r][c] != solution[r][c]:
                    txt = font.render(str(user_board[r][c]), True, BLACK)
                    screen.blit(txt, (rect.x + 20, rect.y + 10))
                    continue

            # Draw notes (pencil marks)
            if user_board is not None and notes is not None and user_board[r][c] == 0 and notes[r][c]:
                for note in notes[r][c]:
                    note_txt = note_font.render(str(note), True, DARK_GRAY)
                    nx = rect.x + ((note - 1) % 3) * (CELL_SIZE // 3) + 5
                    ny = rect.y + ((note - 1) // 3) * (CELL_SIZE // 3) + 5
                    screen.blit(note_txt, (nx, ny))

            if num != 0:
                txt = font.render(str(num), True, BLACK)
                screen.blit(txt, (rect.x + 20, rect.y + 10))

    # Draw cell borders after all shading and numbers
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            rect = pygame.Rect(
                BOARD_MARGIN + c * CELL_SIZE,
                BOARD_MARGIN + r * CELL_SIZE,
                CELL_SIZE, CELL_SIZE
            )
            if selected == (r, c):
                pygame.draw.rect(screen, BLUE, rect, 3)
            else:
                pygame.draw.rect(screen, BLACK, rect, 1)

    # Draw thicker lines for boxes
    for i in range(0, GRID_SIZE + 1, 3):
        pygame.draw.line(
            screen, BLACK,
            (BOARD_MARGIN, BOARD_MARGIN + i * CELL_SIZE),
            (BOARD_MARGIN + WIDTH, BOARD_MARGIN + i * CELL_SIZE), 3
        )
        pygame.draw.line(
            screen, BLACK,
            (BOARD_MARGIN + i * CELL_SIZE, BOARD_MARGIN),
            (BOARD_MARGIN + i * CELL_SIZE, BOARD_MARGIN + WIDTH), 3
        )

def draw_top_buttons(check_solution=False, user_board=None, solution=None, fixed_cells=None):
    # Top buttons: Solve and Show Solution
    button_w = 150
    button_h = BUTTON_HEIGHT
    gap = 30
    y = 20  # Move buttons higher above the board

    labels = [("Solve Board", "solve"), ("Show Solution", "show"), ("Check Solution", "check")]    
    
    total_width = len(labels) * button_w + (len(labels) - 1) * gap
    start_x = (WIDTH + 2 * BOARD_MARGIN - total_width) // 2

    rects = []
    for i, (label, key) in enumerate(labels):
        rect = pygame.Rect(
            start_x + i * (button_w + gap),
            y,
            button_w,
            button_h
        )
        # Highlight Check Solution if toggled
        if key == "check" and check_solution:
            if user_board is not None and solution is not None and fixed_cells is not None and is_board_correct(user_board, solution, fixed_cells):
                color = (120, 220, 120)  # Green if correct
            else:
                color = (120, 180, 255)  # Blue if toggled but not correct
        else:
            color = LIGHT_GRAY
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        txt = button_font.render(label, True, BLACK)
        screen.blit(txt, (rect.x + 10, rect.y + 7))
        rects.append((rect, key))
    return rects[0][0], rects[1][0], rects[2][0]

def draw_bottom_buttons(selected_difficulty, notes_mode=False):
    y = HEIGHT + BOARD_MARGIN

    button_w = 110
    button_h = BUTTON_HEIGHT
    gap = 15

    button_labels = [
        ("Easy", "easy"),
        ("Medium", "medium"),
        ("Hard", "hard"),
        ("Expert", "expert"),
        ("New Game", "new_game"),
        ("Hint", "hint"),
        ("Notes", "notes"),
    ]
    total_width = len(button_labels) * button_w + (len(button_labels) - 1) * gap
    start_x = (WIDTH + 2 * BOARD_MARGIN - total_width) // 2

    rects = []
    for i, (label, key) in enumerate(button_labels):
        rect = pygame.Rect(
            start_x + i * (button_w + gap),
            y,
            button_w,
            button_h
        )
        # Highlight selected difficulty and notes mode
        if key == selected_difficulty:
            color = (180, 220, 180)
        elif key == "notes" and notes_mode:
            color = (180, 200, 255)
        else:
            color = LIGHT_GRAY
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        txt = button_font.render(label, True, BLACK)
        screen.blit(txt, (rect.x + 8, rect.y + 7))
        rects.append((rect, key))

    diff_rects = [r for r in rects if r[1] in ("easy", "medium", "hard")]
    new_game_rect = next(r[0] for r in rects if r[1] == "new_game")
    hint_rect = next(r[0] for r in rects if r[1] == "hint")
    notes_rect = next(r[0] for r in rects if r[1] == "notes")
    return diff_rects, new_game_rect, hint_rect, notes_rect

def generate_puzzle(difficulty):
    board = make_sudoku_board.create_empty_board()
    make_sudoku_board.fill_board(board)
    puzzle = make_sudoku_board.remove_numbers([row[:] for row in board], difficulty)
    return puzzle, board

def draw_number_tracker(user_board, solution, fixed_cells, highlight_number=None):
    x_start = BOARD_MARGIN
    y = HEIGHT + BOARD_MARGIN + BUTTON_HEIGHT + 10
    box_size = 40
    gap = 15
    rects = []
    for n in range(1, 10):
        count = sum(user_board[r][c] == n for r in range(GRID_SIZE) for c in range(GRID_SIZE))
        complete = count == 9 and all(
            (user_board[r][c] == n) == (solution[r][c] == n)
            for r in range(GRID_SIZE) for c in range(GRID_SIZE)
        )
        if highlight_number == n:
            color = (DARK_GRAY)  # Highlighted color
        elif complete:
            color = (180, 255, 180)
        else:
            color = LIGHT_GRAY
        rect = pygame.Rect(x_start + (n-1)*(box_size+gap), y, box_size, box_size)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        txt = font.render(str(n), True, BLACK)
        tw, th = txt.get_size()
        screen.blit(txt, (rect.x + (box_size-tw)//2, rect.y + (box_size-th)//2))
        rects.append(rect)
    return rects

def main():
    selected_difficulty = "easy"
    puzzle, solution = generate_puzzle(selected_difficulty)
    user_board = [row[:] for row in puzzle]
    fixed_cells = [[puzzle[r][c] != 0 for c in range(GRID_SIZE)] for r in range(GRID_SIZE)]
    selected = None
    show_solution = False
    running = True
    notes = [[set() for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    notes_mode = False  # Toggle this with the Notes button
    hint_cells = set()
    check_solution = False
    highlight_number = None
    number_button_rects = draw_number_tracker(user_board, solution, fixed_cells, highlight_number)

    while running:
        draw_board(
        solution if show_solution else user_board,
        selected,
        user_board=user_board,
        show_solution=show_solution,
        check_solution=check_solution,
        solution=solution,
        fixed_cells=fixed_cells,
        notes=notes,
        hint_cells=hint_cells,
        highlight_number=highlight_number
)

        solve_rect, show_rect, check_rect = draw_top_buttons(check_solution, user_board, solution, fixed_cells)
        diff_rects, new_game_rect, hint_rect, notes_rect = draw_bottom_buttons(selected_difficulty, notes_mode)
        draw_number_tracker(user_board, solution, fixed_cells)
        number_button_rects = draw_number_tracker(user_board, solution, fixed_cells)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Top buttons
                if solve_rect.collidepoint(x, y):
                    sudoku_solver.solve_sudoku(user_board)
                    show_solution = False
                    check_solution = False
                elif show_rect.collidepoint(x, y):
                    show_solution = not show_solution
                    check_solution = False
                elif check_rect.collidepoint(x, y):
                    check_solution = not check_solution
                    show_solution = False
                # Difficulty selection (bottom)
                for rect, diff in diff_rects:
                    if rect.collidepoint(x, y):
                        selected_difficulty = diff
                        puzzle, solution = generate_puzzle(selected_difficulty)
                        user_board = [row[:] for row in puzzle]
                        fixed_cells = [[puzzle[r][c] != 0 for c in range(GRID_SIZE)] for r in range(GRID_SIZE)]
                        selected = None
                        show_solution = False
                        hint_cells = set()
                        notes = [[set() for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
                if new_game_rect.collidepoint(x, y):
                    puzzle, solution = generate_puzzle(selected_difficulty)
                    user_board = [row[:] for row in puzzle]
                    fixed_cells = [[puzzle[r][c] != 0 for c in range(GRID_SIZE)] for r in range(GRID_SIZE)]
                    selected = None
                    show_solution = False
                    hint_cells = set()
                    notes = [[set() for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
                if notes_rect.collidepoint(x, y):
                    notes_mode = not notes_mode
                    # if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    #     notes[r][c] = set()
                if hint_rect.collidepoint(x, y):
                    for r in range(GRID_SIZE):
                        for c in range(GRID_SIZE):
                            if not fixed_cells[r][c] and user_board[r][c] == 0:
                                user_board[r][c] = solution[r][c]
                                hint_cells.add((r, c))
                                break  # Only fill one cell per hint
                        else:
                            continue
                        break
                # Board selection
                if (BOARD_MARGIN <= x < BOARD_MARGIN + WIDTH and
                    BOARD_MARGIN <= y < BOARD_MARGIN + WIDTH):
                    selected = ((y - BOARD_MARGIN) // CELL_SIZE, (x - BOARD_MARGIN) // CELL_SIZE)
                for idx, rect in enumerate(number_button_rects):
                    if rect.collidepoint(x, y):
                        if highlight_number == idx + 1:
                            highlight_number = None  # Toggle off
                        else:
                            highlight_number = idx + 1
                        break
            elif event.type == pygame.KEYDOWN and selected and not show_solution:
                r, c = selected
                if not fixed_cells[r][c]:
                    if notes_mode:
                        num = None
                        if event.key == pygame.K_1: num = 1
                        if event.key == pygame.K_2: num = 2
                        if event.key == pygame.K_3: num = 3
                        if event.key == pygame.K_4: num = 4
                        if event.key == pygame.K_5: num = 5
                        if event.key == pygame.K_6: num = 6
                        if event.key == pygame.K_7: num = 7
                        if event.key == pygame.K_8: num = 8
                        if event.key == pygame.K_9: num = 9
                        if num:
                            if num in notes[r][c]:
                                notes[r][c].remove(num)
                            else:
                                notes[r][c].add(num)
                        if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                            notes[r][c] = set()
                    else:
                        if event.key == pygame.K_1: user_board[r][c] = 1
                        if event.key == pygame.K_2: user_board[r][c] = 2
                        if event.key == pygame.K_3: user_board[r][c] = 3
                        if event.key == pygame.K_4: user_board[r][c] = 4
                        if event.key == pygame.K_5: user_board[r][c] = 5
                        if event.key == pygame.K_6: user_board[r][c] = 6
                        if event.key == pygame.K_7: user_board[r][c] = 7
                        if event.key == pygame.K_8: user_board[r][c] = 8
                        if event.key == pygame.K_9: user_board[r][c] = 9
                        if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                            user_board[r][c] = 0
                            notes[r][c] = set()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()