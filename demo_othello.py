import pygame
import sys
import numpy as np

pygame.init()

# Screen
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Othello")

# Load win images (ADD THIS)
black_win_img = pygame.image.load("black_win.jpeg")
white_win_img = pygame.image.load("white_win.jpeg")
tie_img = pygame.image.load("tie.jpeg")

# Optional scaling
black_win_img = pygame.transform.scale(black_win_img, (WIDTH, HEIGHT))
white_win_img = pygame.transform.scale(white_win_img, (WIDTH, HEIGHT))
tie_img = pygame.transform.scale(tie_img, (WIDTH, HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 150, 0)

# Grid
BOARD_ROWS = 8
BOARD_COLS = 8
SQUARE_SIZE = WIDTH // BOARD_COLS

# Circle
CIRCLE_RADIUS = SQUARE_SIZE // 3

# Board (0 = empty, 1 = black, -1 = white)
board = np.zeros((BOARD_ROWS, BOARD_COLS), dtype=int)

# Initial board
board[3, 3] = -1
board[3, 4] = 1
board[4, 3] = 1
board[4, 4] = -1

# Current player
player = 1  # 1 = black, -1 = white


def draw_board():
    screen.fill(GREEN)

    for row in range(BOARD_ROWS):
        pygame.draw.line(screen, BLACK, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), 2)
    for col in range(BOARD_COLS):
        pygame.draw.line(screen, BLACK, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT), 2)


def draw_elements():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row, col] == 1:
                pygame.draw.circle(
                    screen,
                    BLACK,
                    (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                     row * SQUARE_SIZE + SQUARE_SIZE // 2),
                    CIRCLE_RADIUS
                )
            elif board[row, col] == -1:
                pygame.draw.circle(
                    screen,
                    WHITE,
                    (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                     row * SQUARE_SIZE + SQUARE_SIZE // 2),
                    CIRCLE_RADIUS
                )


def switch_possible(row, col, dr, dc, player):
    r, c = row + dr, col + dc
    has_opponent_piece = False    
    while 0 <= r < BOARD_ROWS and 0 <= c < BOARD_COLS:
        if board[r, c] == -player:
            has_opponent_piece = True
        elif board[r, c] == player:
            return has_opponent_piece
        else:
            break
        r += dr
        c += dc
    return False    


def switch_pieces(row, col, player):
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            if switch_possible(row, col, dr, dc, player):
                r, c = row + dr, col + dc
                while board[r, c] == -player:
                    board[r, c] = player
                    r += dr
                    c += dc


def board_full():
    return np.all(board != 0)


def win_count(player):
    return np.sum(board == player)


def win_check(player):
    black_count = win_count(1)
    white_count = win_count(-1)
    if black_count + white_count == BOARD_ROWS * BOARD_COLS or black_count == 0 or white_count == 0:
        if black_count > white_count:
            return 1
        elif white_count > black_count:
            return -1
        else:
            return 0
    return None


def main():
    global player

    game_over = False
    winner = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX, mouseY = event.pos
                col = mouseX // SQUARE_SIZE
                row = mouseY // SQUARE_SIZE

                if board[row, col] == 0:
                    board[row, col] = player
                    switch_pieces(row, col, player)   # FIX: flip pieces
                    player *= -1

                    # CHECK WIN AFTER MOVE (ADD THIS)
                    winner = win_check(player)
                    if winner is not None:
                        game_over = True

        draw_board()
        draw_elements()

        # SHOW WIN SCREEN (ADD THIS)
        if game_over:
            if winner == 1:
                screen.blit(black_win_img, (0, 0))
            elif winner == -1:
                screen.blit(white_win_img, (0, 0))
            else:
                screen.blit(tie_img, (0, 0))

        pygame.display.update()


if __name__ == "__main__":
    main()