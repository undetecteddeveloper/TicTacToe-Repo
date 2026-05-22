# ================================================================
# IMPORTS
# ================================================================
import pygame
import sys


# ================================================================
# CONSTANTS
# ================================================================

    # --- Window
SCREEN_WIDTH  = 600
SCREEN_HEIGHT = 600
FPS           = 60
TITLE         = "Tic-Tac-Toe"

    # --- Grid
GRID_SIZE       = 3
GRID_PIXEL_SIZE = 350
CELL_SIZE       = GRID_PIXEL_SIZE // GRID_SIZE
LINE_WIDTH      = 4
GRID_OFFSET_X   = (SCREEN_WIDTH  - GRID_PIXEL_SIZE) // 2
GRID_OFFSET_Y   = (SCREEN_HEIGHT - GRID_PIXEL_SIZE) // 2

    # --- Marks
MARK_WIDTH   = 6
MARK_PADDING = 20

    # --- Win Line
WIN_LINE_COLOR = (255, 215,   0)
WIN_LINE_WIDTH = 8

    # --- Colors
BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
GRID_COLOR = (200, 200, 200)
X_COLOR    = (255,  80,  80)
O_COLOR    = ( 80,  80, 255)


# ================================================================
# FUNCTIONS
# ================================================================

    # --- Handling Functions (Controller)

def handling_quit(events):
    for event in events:
        if event.type == pygame.QUIT:
            return True
    return False

def handling_cell_click(events):
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return event.pos
    return None


    # --- Processing Functions (Model)

def processing_board_init():
    return [[None, None, None],
            [None, None, None],
            [None, None, None]]

def processing_cell_from_click(mouse_pos):
    x, y = mouse_pos
    col = (x - GRID_OFFSET_X) // CELL_SIZE
    row = (y - GRID_OFFSET_Y) // CELL_SIZE
    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
        return row, col
    return None

def processing_place_mark(board, row, col, current_player):
    if board[row][col] is None:
        board[row][col] = current_player
        return True
    return False

def processing_switch_turn(current_player):
    return "O" if current_player == "X" else "X"

def processing_check_winner(board):
    lines = [
        [(0,0), (0,1), (0,2)],
        [(1,0), (1,1), (1,2)],
        [(2,0), (2,1), (2,2)],
        [(0,0), (1,0), (2,0)],
        [(0,1), (1,1), (2,1)],
        [(0,2), (1,2), (2,2)],
        [(0,0), (1,1), (2,2)],
        [(0,2), (1,1), (2,0)],
    ]
    for line in lines:
        marks = [board[r][c] for r, c in line]
        if marks[0] is not None and marks[0] == marks[1] == marks[2]:
            return marks[0], line
    return None, None

def processing_win_line_coords(winning_cells):
    r1, c1 = winning_cells[0]
    r2, c2 = winning_cells[-1]
    start = (GRID_OFFSET_X + c1 * CELL_SIZE + CELL_SIZE // 2,
             GRID_OFFSET_Y + r1 * CELL_SIZE + CELL_SIZE // 2)
    end   = (GRID_OFFSET_X + c2 * CELL_SIZE + CELL_SIZE // 2,
             GRID_OFFSET_Y + r2 * CELL_SIZE + CELL_SIZE // 2)
    return start, end


# ================================================================
# MAIN
# ================================================================

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    board          = processing_board_init()
    current_player = "X"
    winner         = None
    winning_cells  = None

    while True:
        events = pygame.event.get()

        if handling_quit(events):
            pygame.quit()
            sys.exit()

        if winner is None:
            mouse_pos = handling_cell_click(events)
            if mouse_pos is not None:
                cell = processing_cell_from_click(mouse_pos)
                if cell is not None:
                    row, col = cell
                    placed = processing_place_mark(board, row, col, current_player)
                    if placed:
                        winner, winning_cells = processing_check_winner(board)
                        if winner is None:
                            current_player = processing_switch_turn(current_player)

        screen.fill(BLACK)

        for i in range(1, GRID_SIZE):
            pygame.draw.line(screen, GRID_COLOR,
                             (GRID_OFFSET_X + i * CELL_SIZE, GRID_OFFSET_Y),
                             (GRID_OFFSET_X + i * CELL_SIZE, GRID_OFFSET_Y + GRID_PIXEL_SIZE),
                             LINE_WIDTH)
            pygame.draw.line(screen, GRID_COLOR,
                             (GRID_OFFSET_X, GRID_OFFSET_Y + i * CELL_SIZE),
                             (GRID_OFFSET_X + GRID_PIXEL_SIZE, GRID_OFFSET_Y + i * CELL_SIZE),
                             LINE_WIDTH)

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                mark = board[row][col]
                x    = GRID_OFFSET_X + col * CELL_SIZE
                y    = GRID_OFFSET_Y + row * CELL_SIZE

                if mark == "X":
                    pygame.draw.line(screen, X_COLOR,
                                     (x + MARK_PADDING,             y + MARK_PADDING),
                                     (x + CELL_SIZE - MARK_PADDING, y + CELL_SIZE - MARK_PADDING),
                                     MARK_WIDTH)
                    pygame.draw.line(screen, X_COLOR,
                                     (x + CELL_SIZE - MARK_PADDING, y + MARK_PADDING),
                                     (x + MARK_PADDING,             y + CELL_SIZE - MARK_PADDING),
                                     MARK_WIDTH)

                elif mark == "O":
                    center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
                    radius = CELL_SIZE // 2 - MARK_PADDING
                    pygame.draw.circle(screen, O_COLOR, center, radius, MARK_WIDTH)

        if winning_cells is not None:
            start, end = processing_win_line_coords(winning_cells)
            pygame.draw.line(screen, WIN_LINE_COLOR, start, end, WIN_LINE_WIDTH)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
