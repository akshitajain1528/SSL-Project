import pygame
import sys
import numpy as np

pygame.init()

# Screen
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Othello")

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

    # Draw grid lines
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


def main():
    global player

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                col = mouseX // SQUARE_SIZE
                row = mouseY // SQUARE_SIZE

                # Place piece only if empty
                if board[row, col] == 0:
                    board[row, col] = player
                    player *= -1  # switch turns

        draw_board()
        draw_elements()
        pygame.display.update()


if __name__ == "__main__":
    main()