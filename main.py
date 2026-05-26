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
GAME_SETTING = 6

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
SETTING_FONT_SIZE    = 28

    # --- Colors
BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
GRID_COLOR = (200, 200, 200)
X_COLOR    = (255,  80,  80)
O_COLOR    = ( 80,  80, 255)
DARK_GRAY  = ( 30,  30,  30)
MID_GRAY   = ( 70,  70,  70)

    # --- Menu
MENU_TITLE_Y   = 130
MENU_ICON_SIZE = 100
MENU_ICON_GAP  =  50
MENU_ICON_Y    = 240
MENU_TEXT_Y    = 410

    # --- Setting Panel
SETTING_BOX_W         = 380
SETTING_BOX_H         = 280
SETTING_FIELD_W       =  70
SETTING_FIELD_H       =  34
SETTING_CHECKBOX_SIZE =  26
SETTING_BTN_W         = 280
SETTING_BTN_H         =  40
DEFAULT_WIN_SCORE     =   3


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
    started       = False
    open_settings = False
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                open_settings = True
            else:
                started = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            started = True
    return started, open_settings

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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return "stay"
            elif event.key == pygame.K_q:
                return "menu"
    return None

def handling_pause(events):
    for event in events:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return True
    return False

def handling_setting(events, field_rect, cb_rect, btn_rect):
    clicked_field     = False
    clicked_outside   = False
    clicked_checkbox  = False
    clicked_btn       = False
    typed_text        = ""
    pressed_backspace = False
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if field_rect.collidepoint(event.pos):
                clicked_field = True
            elif cb_rect.collidepoint(event.pos):
                clicked_checkbox = True
            elif btn_rect.collidepoint(event.pos):
                clicked_btn = True
            else:
                clicked_outside = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                pressed_backspace = True
            elif event.key == pygame.K_RETURN:
                clicked_outside = True
            elif event.unicode.isdigit():
                typed_text += event.unicode
    return clicked_field, clicked_outside, clicked_checkbox, clicked_btn, typed_text, pressed_backspace

def handling_sound(prev_state, new_state, mark_placed, score_x, score_o, win_score):
    play_marking = mark_placed
    start_music  = (new_state == GAME_MENU and prev_state in (None, GAME_ACTION))
    stop_music   = (new_state == GAME_ACTION and prev_state != GAME_ACTION)
    play_winning = (new_state == GAME_ACTION and prev_state != GAME_ACTION
                    and (score_x >= win_score or score_o >= win_score))
    stop_winning = (prev_state == GAME_ACTION and new_state != GAME_ACTION)
    return play_marking, start_music, stop_music, play_winning, stop_winning


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

def processing_menu(started, open_settings):
    if open_settings:
        return GAME_SETTING
    if started:
        return GAME_RUNNING
    return GAME_MENU

def processing_running(click_pos, pause_pressed, board, current_player):
    mark_placed = False
    if pause_pressed:
        return GAME_PAUSE, current_player, None, None, mark_placed

    if click_pos is None:
        return GAME_RUNNING, current_player, None, None, mark_placed

    cell = processing_cell_from_click(click_pos)
    if cell is None:
        return GAME_RUNNING, current_player, None, None, mark_placed

    row, col = cell
    placed   = processing_place_mark(board, row, col, current_player)
    if not placed:
        return GAME_RUNNING, current_player, None, None, mark_placed

    mark_placed = True
    winner, winning_cells = processing_check_winner(board)
    if winner is not None:
        return GAME_ACTION, current_player, winner, winning_cells, mark_placed

    if processing_is_draw(board):
        return GAME_DRAW, "X", None, None, mark_placed

    return GAME_RUNNING, processing_switch_turn(current_player), None, None, mark_placed

def processing_action(action):
    if action == "stay":
        return GAME_RUNNING
    if action == "menu":
        return GAME_MENU
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

def processing_setting(clicked_field, clicked_outside, clicked_checkbox, clicked_btn,
                        typed_text, pressed_backspace,
                        setting_input, setting_active, win_score, show_fps):
    if clicked_btn:
        return GAME_MENU, setting_input, False, win_score, show_fps

    if clicked_field:
        setting_active = True
    elif clicked_outside:
        setting_active = False
        if setting_input.isdigit() and int(setting_input) > 0:
            win_score = int(setting_input)
        else:
            setting_input = str(win_score)

    if clicked_checkbox:
        show_fps = not show_fps

    if setting_active:
        if pressed_backspace:
            setting_input = setting_input[:-1]
        if len(setting_input) + len(typed_text) <= 2:
            setting_input += typed_text

    return GAME_SETTING, setting_input, setting_active, win_score, show_fps

def processing_sound(play_marking, start_music, stop_music, play_winning, stop_winning,
                     marking_sfx, winning_sfx):
    if play_marking:
        marking_sfx.play()
    if stop_music:
        pygame.mixer.music.stop()
    if start_music:
        pygame.mixer.music.play(-1)
    if play_winning:
        winning_sfx.play(-1)
    if stop_winning:
        winning_sfx.stop()


# ================================================================
# MAIN
# ================================================================

def main():
    pygame.init()
    _icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "image", "cờ_caro_icon.png")
    pygame.display.set_icon(pygame.image.load(_icon_path))
    screen     = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock      = pygame.time.Clock()
    font         = pygame.font.SysFont("arial", FONT_SIZE)
    score_font   = pygame.font.SysFont("arial", SCORE_FONT_SIZE)
    menu_font    = pygame.font.SysFont("arial", MENU_TITLE_FONT_SIZE, bold=True)
    setting_font = pygame.font.SysFont("arial", SETTING_FONT_SIZE)

    img_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "image")
    icon1   = pygame.transform.scale(
                  pygame.image.load(os.path.join(img_dir, "cờ_caro_icon.png")).convert_alpha(),
                  (MENU_ICON_SIZE, MENU_ICON_SIZE))
    icon2   = pygame.transform.scale(
                  pygame.image.load(os.path.join(img_dir, "ClaudeCode_logo.png")).convert_alpha(),
                  (MENU_ICON_SIZE, MENU_ICON_SIZE))

    dim_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    dim_overlay.fill((0, 0, 0, 160))

    snd_dir     = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "sounds")
    marking_sfx = pygame.mixer.Sound(os.path.join(snd_dir, "marking_SFX.wav"))
    winning_sfx = pygame.mixer.Sound(os.path.join(snd_dir, "winning_SFX.wav"))
    pygame.mixer.music.load(os.path.join(snd_dir, "background_music.wav"))

    setting_box_x    = (SCREEN_WIDTH  - SETTING_BOX_W) // 2
    setting_box_y    = (SCREEN_HEIGHT - SETTING_BOX_H) // 2
    setting_field_rect = pygame.Rect(
        setting_box_x + 220, setting_box_y + 63, SETTING_FIELD_W, SETTING_FIELD_H)
    setting_cb_rect  = pygame.Rect(
        setting_box_x + 220, setting_box_y + 117, SETTING_CHECKBOX_SIZE, SETTING_CHECKBOX_SIZE)
    setting_btn_rect = pygame.Rect(
        setting_box_x + (SETTING_BOX_W - SETTING_BTN_W) // 2,
        setting_box_y + SETTING_BOX_H - SETTING_BTN_H - 20,
        SETTING_BTN_W, SETTING_BTN_H)

    board           = processing_board_init()
    current_player  = "X"
    winner          = None
    winning_cells   = None
    score_x         = 0
    score_o         = 0
    game_state      = GAME_MENU
    draw_start_time = 0
    win_score       = DEFAULT_WIN_SCORE
    show_fps        = False
    setting_input   = str(DEFAULT_WIN_SCORE)
    setting_active  = False

    while True:
        events      = pygame.event.get()
        prev_state  = game_state
        mark_placed = False

        if handling_quit(events):
            pygame.quit()
            sys.exit()

        if game_state == GAME_MENU:
            started, open_settings = handling_menu(events)
            game_state = processing_menu(started, open_settings)

        elif game_state == GAME_RUNNING:
            click_pos, pause_pressed                                       = handling_running(events)
            game_state, current_player, winner, winning_cells, mark_placed = processing_running(
                click_pos, pause_pressed, board, current_player
            )
            if game_state == GAME_ACTION:
                score_x, score_o = processing_update_score(score_x, score_o, winner)
            elif game_state == GAME_DRAW:
                draw_start_time = pygame.time.get_ticks()

        elif game_state == GAME_ACTION:
            action     = handling_action(events)
            game_state = processing_action(action)
            if game_state in (GAME_RUNNING, GAME_MENU):
                board          = processing_board_init()
                current_player = "X"
                winner         = None
                winning_cells  = None
            if game_state == GAME_RUNNING and (score_x >= win_score or score_o >= win_score):
                score_x = 0
                score_o = 0
            if game_state == GAME_MENU:
                score_x = 0
                score_o = 0

        elif game_state == GAME_PAUSE:
            resume     = handling_pause(events)
            game_state = processing_pause(resume)

        elif game_state == GAME_DRAW:
            game_state = processing_draw(draw_start_time)
            if game_state == GAME_RUNNING:
                board          = processing_board_init()
                current_player = "X"

        elif game_state == GAME_SETTING:
            (clicked_field, clicked_outside, clicked_checkbox,
             clicked_btn, typed_text, pressed_backspace) = handling_setting(
                events, setting_field_rect, setting_cb_rect, setting_btn_rect)
            (game_state, setting_input, setting_active,
             win_score, show_fps) = processing_setting(
                clicked_field, clicked_outside, clicked_checkbox, clicked_btn,
                typed_text, pressed_backspace,
                setting_input, setting_active, win_score, show_fps)

        elif game_state == EXIT:
            pygame.quit()
            sys.exit()

        # Sound
        (play_marking, start_music, stop_music,
         play_winning, stop_winning) = handling_sound(
            prev_state, game_state, mark_placed, score_x, score_o, win_score)
        processing_sound(play_marking, start_music, stop_music, play_winning, stop_winning,
                         marking_sfx, winning_sfx)

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
                text = font.render("Press any keys to play (Press S to open Setting)", True, WHITE)
                screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, MENU_TEXT_Y)))

        elif game_state == GAME_ACTION:
            text = font.render("SPACE to play again  |  Q to return to menu", True, WHITE)
            screen.blit(text, text.get_rect(
                center=(SCREEN_WIDTH // 2, GRID_OFFSET_Y + GRID_PIXEL_SIZE + 30)
            ))

        elif game_state == GAME_PAUSE:
            text = font.render("PAUSED  -  ESC to resume", True, WHITE)
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

        elif game_state == GAME_DRAW:
            text = font.render("Draw", True, WHITE)
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, GRID_OFFSET_Y + FONT_SIZE // 2 - 25)))

        elif game_state == GAME_SETTING:
            title  = menu_font.render("Caro Chess", True, WHITE)
            icon1_x = SCREEN_WIDTH // 2 - MENU_ICON_SIZE - MENU_ICON_GAP // 2
            icon2_x = SCREEN_WIDTH // 2 + MENU_ICON_GAP // 2
            screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, MENU_TITLE_Y)))
            screen.blit(icon1, (icon1_x, MENU_ICON_Y))
            screen.blit(icon2, (icon2_x, MENU_ICON_Y))
            screen.blit(dim_overlay, (0, 0))

            pygame.draw.rect(screen, DARK_GRAY,
                             (setting_box_x, setting_box_y, SETTING_BOX_W, SETTING_BOX_H))
            pygame.draw.rect(screen, WHITE,
                             (setting_box_x, setting_box_y, SETTING_BOX_W, SETTING_BOX_H), 2)

            s_title = setting_font.render("Setting", True, WHITE)
            screen.blit(s_title, s_title.get_rect(
                center=(SCREEN_WIDTH // 2, setting_box_y + 30)))

            win_label = setting_font.render("Win score :", True, WHITE)
            screen.blit(win_label, win_label.get_rect(
                midleft=(setting_box_x + 20, setting_field_rect.centery)))
            field_color = MID_GRAY if setting_active else DARK_GRAY
            pygame.draw.rect(screen, field_color, setting_field_rect)
            pygame.draw.rect(screen, WHITE, setting_field_rect, 1)
            input_surf = setting_font.render(setting_input, True, WHITE)
            screen.blit(input_surf, input_surf.get_rect(center=setting_field_rect.center))

            fps_label = setting_font.render("Show FPS :", True, WHITE)
            screen.blit(fps_label, fps_label.get_rect(
                midleft=(setting_box_x + 20, setting_cb_rect.centery)))
            pygame.draw.rect(screen, MID_GRAY, setting_cb_rect)
            pygame.draw.rect(screen, WHITE, setting_cb_rect, 2)
            if show_fps:
                p = 4
                pygame.draw.line(screen, WHITE,
                                 (setting_cb_rect.left   + p, setting_cb_rect.centery),
                                 (setting_cb_rect.centerx, setting_cb_rect.bottom - p), 3)
                pygame.draw.line(screen, WHITE,
                                 (setting_cb_rect.centerx, setting_cb_rect.bottom - p),
                                 (setting_cb_rect.right  - p, setting_cb_rect.top    + p), 3)

            pygame.draw.rect(screen, MID_GRAY, setting_btn_rect)
            pygame.draw.rect(screen, WHITE, setting_btn_rect, 2)
            btn_surf = setting_font.render("<- Return to Menu", True, WHITE)
            screen.blit(btn_surf, btn_surf.get_rect(center=setting_btn_rect.center))

        if show_fps:
            fps_surf = font.render(str(int(clock.get_fps())), True, WHITE)
            screen.blit(fps_surf, (8, SCREEN_HEIGHT - FONT_SIZE - 8))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()