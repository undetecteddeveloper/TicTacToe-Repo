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

    # --- Colors
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)


# ================================================================
# FUNCTIONS
# ================================================================

    # --- Handling Functions (Controller)

def handling_quit(events):
    for event in events:
        if event.type == pygame.QUIT:
            return True
    return False


# ================================================================
# MAIN
# ================================================================

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    while True:
        events = pygame.event.get()

        if handling_quit(events):
            pygame.quit()
            sys.exit()

        screen.fill(BLACK)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
