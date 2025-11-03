import pygame, sys

pygame.init()

# --- Game Constants ---
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH, CROSS_WIDTH = 15, 25
SPACE = SQUARE_SIZE // 4

# --- Colors ---
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (84, 84, 84)

# --- Screen setup ---
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe (AI / 2 Player)")
screen.fill(BG_COLOR)

# --- Fonts ---
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 50)

# --- Board ---
board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def draw_lines():
    # Horizontal
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Vertical
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_menu():
    screen.fill((20, 20, 20))
    title = font.render("Tic Tac Toe", True, (255, 255, 255))
    ai_text = small_font.render("Press A: Player vs AI", True, (0, 255, 0))
    player_text = small_font.render("Press P: Player vs Player", True, (0, 255, 0))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))
    screen.blit(ai_text, (WIDTH // 2 - ai_text.get_width() // 2, 300))
    screen.blit(player_text, (WIDTH // 2 - player_text.get_width() // 2, 400))
    pygame.display.update()

def mark_square(row, col, player): board[row][col] = player
def available_square(row, col): return board[row][col] == ''
def is_full(): return all(board[r][c] != '' for r in range(BOARD_ROWS) for c in range(BOARD_COLS))

def draw_figures():
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            if board[r][c] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR,
                    (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2),
                    CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[r][c] == 'X':
                start_desc = (c * SQUARE_SIZE + SPACE, r * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                end_desc = (c * SQUARE_SIZE + SQUARE_SIZE - SPACE, r * SQUARE_SIZE + SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
                start_asc = (c * SQUARE_SIZE + SPACE, r * SQUARE_SIZE + SPACE)
                end_asc = (c * SQUARE_SIZE + SQUARE_SIZE - SPACE, r * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

# --- Winning lines ---
def draw_vertical_winning_line(col, player):
    color = CIRCLE_COLOR if player == 'O' else CROSS_COLOR
    x = col * SQUARE_SIZE + SQUARE_SIZE // 2
    pygame.draw.line(screen, color, (x, 15), (x, HEIGHT - 15), 15)

def draw_horizontal_winning_line(row, player):
    color = CIRCLE_COLOR if player == 'O' else CROSS_COLOR
    y = row * SQUARE_SIZE + SQUARE_SIZE // 2
    pygame.draw.line(screen, color, (15, y), (WIDTH - 15, y), 15)

def draw_asc_diagonal(player):
    color = CIRCLE_COLOR if player == 'O' else CROSS_COLOR
    pygame.draw.line(screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), 15)

def draw_desc_diagonal(player):
    color = CIRCLE_COLOR if player == 'O' else CROSS_COLOR
    pygame.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), 15)

def check_winner(player):
    # vertical
    for c in range(BOARD_COLS):
        if board[0][c] == board[1][c] == board[2][c] == player:
            draw_vertical_winning_line(c,player)
            return True
    # horizontal
    for r in range(BOARD_ROWS):
        if board[r][0] == board[r][1] == board[r][2] == player:
         draw_horizontal_winning_line(r,player)
         return True
    # diagonals
    if board[0][0] == board[1][1] == board[2][2] == player:
        draw_desc_diagonal(player)
        return True
    if board[2][0] == board[1][1] == board[0][2] == player:
         draw_asc_diagonal(player)
         return True
    return False

def restart():
    screen.fill(BG_COLOR)
    draw_lines()
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            board[r][c] = ''

# --- Minimax AI ---
def minimax(board_state, depth, is_maximizing):
    if check_winner('O'): return 1
    if check_winner('X'): return -1
    if is_full(): return 0

    if is_maximizing:
        best = -float('inf')
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                if board_state[r][c] == '':
                    board_state[r][c] = 'O'
                    val = minimax(board_state, depth + 1, False)
                    board_state[r][c] = ''
                    best = max(best, val)
        return best
    else:
        best = float('inf')
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                if board_state[r][c] == '':
                    board_state[r][c] = 'X'
                    val = minimax(board_state, depth + 1, True)
                    board_state[r][c] = ''
                    best = min(best, val)
        return best

def ai_move():
    best_score, best_move = -float('inf'), None
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            if board[r][c] == '':
                board[r][c] = 'O'
                score = minimax(board, 0, False)
                board[r][c] = ''
                if score > best_score:
                    best_score, best_move = score, (r, c)
    if best_move:
        mark_square(best_move[0], best_move[1], 'O')

# --- Main Loop ---
draw_lines()
player = 'X'
game_over = False
mode = None  # "AI" or "PVP"

while True:
    if mode is None:
        draw_menu()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_a:
                    mode = "AI"; restart()
                if e.key == pygame.K_p:
                    mode = "PVP"; restart()
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = event.pos
            r, c = y // SQUARE_SIZE, x // SQUARE_SIZE
            if available_square(r, c):
                mark_square(r, c, player)
                draw_figures()
                if check_winner(player):
                    game_over = True
                else:
                    player = 'O' if player == 'X' else 'X'

                # --- AI Turn ---
                if mode == "AI" and not game_over and player == 'O':
                    pygame.display.update()
                    pygame.time.delay(400)
                    ai_move()
                    draw_figures()
                    if check_winner('O'):
                        game_over = True
                    player = 'X'

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart(); player = 'X'; game_over = False
            if event.key == pygame.K_m:
                mode = None; restart(); player = 'X'; game_over = False

    pygame.display.update()
