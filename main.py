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

    # --- Colors
BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
GRID_COLOR = (200, 200, 200)


# ================================================================
# FUNCTIONS
# ================================================================

    # --- Handling Functions (Controller)

def handling_quit(events):
    for event in events:
        if event.type == pygame.QUIT:
            return True
    return False


    # --- Processing Functions (Model)

def processing_board_init():
    return [[None, None, None],
            [None, None, None],
            [None, None, None]]


# ================================================================
# MAIN
# ================================================================

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    board = processing_board_init()

    while True:
        events = pygame.event.get()

        if handling_quit(events):
            pygame.quit()
            sys.exit()

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

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
