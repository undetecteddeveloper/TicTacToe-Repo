# ================================================================
# IMPORTS
# ================================================================
import pygame
import sys
import os


# ================================================================
# CONSTANTS
# ================================================================

    # --- Window
SCREEN_WIDTH  = 600
SCREEN_HEIGHT = 600
FPS           = 60
TITLE         = "Tic-Tac-Toe"

    # --- Game States
GAME_MENU    = 0
GAME_RUNNING = 1
GAME_ACTION  = 2
GAME_PAUSE   = 3
GAME_DRAW    = 4
EXIT         = 5

    # --- Timing
DRAW_DISPLAY_TIME = 2000
FLASH_INTERVAL    =  600

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

    # --- Fonts
FONT_SIZE            = 32
SCORE_FONT_SIZE      = 48
MENU_TITLE_FONT_SIZE = 52

    # --- Colors
BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
GRID_COLOR = (200, 200, 200)
X_COLOR    = (255,  80,  80)
O_COLOR    = ( 80,  80, 255)

    # --- Menu
MENU_TITLE_Y  = 130
MENU_ICON_SIZE = 100
MENU_ICON_GAP  =  50
MENU_ICON_Y    = 240
MENU_TEXT_Y    = 410


# ================================================================
# FUNCTIONS
# ================================================================

    # --- Handling Functions (Controller)

def handling_quit(events):
    for event in events:
        if event.type == pygame.QUIT:
            return True
    return False

def handling_menu(events):
    for event in events:
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
            return True
    return False

def handling_running(events):
    click_pos     = None
    pause_pressed = False
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click_pos = event.pos
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pause_pressed = True
    return click_pos, pause_pressed

def handling_action(events):
    for event in events:
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
            return True
    return False

def handling_pause(events):
    for event in events:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return True
    return False


    # --- Processing Functions (Model)

def processing_board_init():
    return [[None, None, None],
            [None, None, None],
            [None, None, None]]

def processing_cell_from_click(mouse_pos):
    x, y = mouse_pos
    col  = (x - GRID_OFFSET_X) // CELL_SIZE
    row  = (y - GRID_OFFSET_Y) // CELL_SIZE
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
    start  = (GRID_OFFSET_X + c1 * CELL_SIZE + CELL_SIZE // 2,
              GRID_OFFSET_Y + r1 * CELL_SIZE + CELL_SIZE // 2)
    end    = (GRID_OFFSET_X + c2 * CELL_SIZE + CELL_SIZE // 2,
              GRID_OFFSET_Y + r2 * CELL_SIZE + CELL_SIZE // 2)
    return start, end

def processing_is_draw(board):
    for row in board:
        if None in row:
            return False
    return True

def processing_update_score(score_x, score_o, winner):
    if winner == "X":
        score_x += 1
    elif winner == "O":
        score_o += 1
    return score_x, score_o

def processing_menu(started):
    if started:
        return GAME_RUNNING
    return GAME_MENU

def processing_running(click_pos, pause_pressed, board, current_player):
    if pause_pressed:
        return GAME_PAUSE, current_player, None, None

    if click_pos is None:
        return GAME_RUNNING, current_player, None, None

    cell = processing_cell_from_click(click_pos)
    if cell is None:
        return GAME_RUNNING, current_player, None, None

    row, col = cell
    placed   = processing_place_mark(board, row, col, current_player)
    if not placed:
        return GAME_RUNNING, current_player, None, None

    winner, winning_cells = processing_check_winner(board)
    if winner is not None:
        return GAME_ACTION, current_player, winner, winning_cells

    if processing_is_draw(board):
        return GAME_DRAW, "X", None, None

    return GAME_RUNNING, processing_switch_turn(current_player), None, None

def processing_action(confirmed):
    if confirmed:
        return GAME_RUNNING
    return GAME_ACTION

def processing_pause(resume):
    if resume:
        return GAME_RUNNING
    return GAME_PAUSE

def processing_draw(draw_start_time):
    if pygame.time.get_ticks() - draw_start_time >= DRAW_DISPLAY_TIME:
        return GAME_RUNNING
    return GAME_DRAW

def processing_flash_text(interval):
    return (pygame.time.get_ticks() // interval) % 2 == 0


# ================================================================
# MAIN
# ================================================================

def main():
    pygame.init()
    screen     = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock      = pygame.time.Clock()
    font       = pygame.font.SysFont("arial", FONT_SIZE)
    score_font = pygame.font.SysFont("arial", SCORE_FONT_SIZE)
    menu_font  = pygame.font.SysFont("arial", MENU_TITLE_FONT_SIZE, bold=True)

    img_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "image")
    icon1   = pygame.transform.scale(
                  pygame.image.load(os.path.join(img_dir, "cờ_caro_icon.png")).convert_alpha(),
                  (MENU_ICON_SIZE, MENU_ICON_SIZE))
    icon2   = pygame.transform.scale(
                  pygame.image.load(os.path.join(img_dir, "ClaudeCode_logo.png")).convert_alpha(),
                  (MENU_ICON_SIZE, MENU_ICON_SIZE))

    board           = processing_board_init()
    current_player  = "X"
    winner          = None
    winning_cells   = None
    score_x         = 0
    score_o         = 0
    game_state      = GAME_MENU
    draw_start_time = 0

    while True:
        events = pygame.event.get()

        if handling_quit(events):
            pygame.quit()
            sys.exit()

        if game_state == GAME_MENU:
            started    = handling_menu(events)
            game_state = processing_menu(started)

        elif game_state == GAME_RUNNING:
            click_pos, pause_pressed                          = handling_running(events)
            game_state, current_player, winner, winning_cells = processing_running(
                click_pos, pause_pressed, board, current_player
            )
            if game_state == GAME_ACTION:
                score_x, score_o = processing_update_score(score_x, score_o, winner)
            elif game_state == GAME_DRAW:
                draw_start_time = pygame.time.get_ticks()

        elif game_state == GAME_ACTION:
            confirmed  = handling_action(events)
            game_state = processing_action(confirmed)
            if game_state == GAME_RUNNING:
                board          = processing_board_init()
                current_player = "X"
                winner         = None
                winning_cells  = None

        elif game_state == GAME_PAUSE:
            resume     = handling_pause(events)
            game_state = processing_pause(resume)

        elif game_state == GAME_DRAW:
            game_state = processing_draw(draw_start_time)
            if game_state == GAME_RUNNING:
                board          = processing_board_init()
                current_player = "X"

        elif game_state == EXIT:
            pygame.quit()
            sys.exit()

        # View
        screen.fill(BLACK)

        if game_state in (GAME_RUNNING, GAME_ACTION, GAME_PAUSE, GAME_DRAW):
            score_y_label = GRID_OFFSET_Y // 2 - SCORE_FONT_SIZE // 2 + 4
            score_y_num   = GRID_OFFSET_Y // 2 + FONT_SIZE  // 2 + 4

            x_label = font.render("Red Player",  True, WHITE)
            o_label = font.render("Blue Player", True, WHITE)
            x_score = score_font.render(str(score_x), True, X_COLOR)
            o_score = score_font.render(str(score_o), True, O_COLOR)

            screen.blit(x_label, x_label.get_rect(center=(SCREEN_WIDTH // 4,     score_y_label)))
            screen.blit(o_label, o_label.get_rect(center=(SCREEN_WIDTH * 3 // 4, score_y_label)))
            screen.blit(x_score, x_score.get_rect(center=(SCREEN_WIDTH // 4,     score_y_num)))
            screen.blit(o_score, o_score.get_rect(center=(SCREEN_WIDTH * 3 // 4, score_y_num)))

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

        if game_state == GAME_MENU:
            title = menu_font.render("Caro Chess", True, WHITE)
            screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, MENU_TITLE_Y)))

            icon1_x = SCREEN_WIDTH // 2 - MENU_ICON_SIZE - MENU_ICON_GAP // 2
            icon2_x = SCREEN_WIDTH // 2 + MENU_ICON_GAP // 2
            screen.blit(icon1, (icon1_x, MENU_ICON_Y))
            screen.blit(icon2, (icon2_x, MENU_ICON_Y))

            if processing_flash_text(FLASH_INTERVAL):
                text = font.render("Press any keys to play", True, WHITE)
                screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, MENU_TEXT_Y)))

        elif game_state == GAME_ACTION:
            text = font.render("Click to restart", True, WHITE)
            screen.blit(text, text.get_rect(
                center=(SCREEN_WIDTH // 2, GRID_OFFSET_Y + GRID_PIXEL_SIZE + 30)
            ))

        elif game_state == GAME_PAUSE:
            text = font.render("PAUSED  -  ESC to resume", True, WHITE)
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

        elif game_state == GAME_DRAW:
            text = font.render("Draw", True, WHITE)
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, GRID_OFFSET_Y + FONT_SIZE // 2 + 5)))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()