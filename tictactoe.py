import pygame
import sys
import numpy as np

pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic tac toe")

# Grid dimensions
LINE_WIDTH = 3
BOARD_ROWS = 10
BOARD_COLS = 10
SQUARE_SIZE = WIDTH // BOARD_COLS

# Element dimensions
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 5
CROSS_WIDTH = 8
SPACE = SQUARE_SIZE // 4

# Colors
PINK = (255, 0, 102)
PURPLE = (153, 51, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Background
background = pygame.image.load("Origin.jpg").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# numpy array representing the board
board = np.zeros((BOARD_ROWS, BOARD_COLS), dtype=int)

#initial values
player = 1
game_over = False
winning_line = None


def draw_grid():
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, BLACK, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
    for col in range(1, BOARD_COLS):
        pygame.draw.line(screen, BLACK, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT), LINE_WIDTH)


def draw_elements():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(
                    screen, PINK,
                    (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                     row * SQUARE_SIZE + SQUARE_SIZE // 2),
                    CIRCLE_RADIUS, CIRCLE_WIDTH
                )
            elif board[row][col] == -1:
                pygame.draw.line(
                    screen, PURPLE,
                    (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                    (col * SQUARE_SIZE + SQUARE_SIZE - SPACE,
                     row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                    CROSS_WIDTH
                )
                pygame.draw.line(
                    screen, PURPLE,
                    (col * SQUARE_SIZE + SPACE,
                     row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                    (col * SQUARE_SIZE + SQUARE_SIZE - SPACE,
                     row * SQUARE_SIZE + SPACE),
                    CROSS_WIDTH
                )


def draw_winning_line():
    if winning_line:
        pygame.draw.line(screen, GREEN, winning_line[0], winning_line[1], 8)


def mark_square(row, col, player):
    board[row][col] = player


def available_square(row, col):
    return board[row][col] == 0


def check_win(player):
    global winning_line

    # Horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 4):
            if board[row][col:col+5].tolist() == [player] * 5:
                x1 = col * SQUARE_SIZE + SQUARE_SIZE // 2
                y = row * SQUARE_SIZE + SQUARE_SIZE // 2
                x2 = (col + 4) * SQUARE_SIZE + SQUARE_SIZE // 2
                winning_line = ((x1, y), (x2, y))
                return True

    # Vertical
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 4):
            if board[row:row+5, col].tolist() == [player] * 5:
                x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                y1 = row * SQUARE_SIZE + SQUARE_SIZE // 2
                y2 = (row + 4) * SQUARE_SIZE + SQUARE_SIZE // 2
                winning_line = ((x, y1), (x, y2))
                return True

    # Diagonal down
    for row in range(BOARD_ROWS - 4):
        for col in range(BOARD_COLS - 4):
            if board[row:row+5, col:col+5].diagonal().tolist() == [player] * 5:
                x1 = col * SQUARE_SIZE + SQUARE_SIZE // 2
                y1 = row * SQUARE_SIZE + SQUARE_SIZE // 2
                x2 = (col + 4) * SQUARE_SIZE + SQUARE_SIZE // 2
                y2 = (row + 4) * SQUARE_SIZE + SQUARE_SIZE // 2
                winning_line = ((x1, y1), (x2, y2))
                return True

    # Diagonal up
    for row in range(4, BOARD_ROWS):
        for col in range(BOARD_COLS - 4):
            if np.fliplr(board[row-4:row+1, col:col+5]).diagonal().tolist() == [player] * 5:
                x1 = col * SQUARE_SIZE + SQUARE_SIZE // 2
                y1 = row * SQUARE_SIZE + SQUARE_SIZE // 2
                x2 = (col + 4) * SQUARE_SIZE + SQUARE_SIZE // 2
                y2 = (row - 4) * SQUARE_SIZE + SQUARE_SIZE // 2
                winning_line = ((x1, y1), (x2, y2))
                return True

    return False


def main():
    global player, game_over

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX, mouseY = event.pos
                col = mouseX // SQUARE_SIZE
                row = mouseY // SQUARE_SIZE

                if available_square(row, col):
                    mark_square(row, col, player)

                    if check_win(player):
                        game_over = True

                    #
                    player = -player

        screen.blit(background, (0, 0))
        draw_grid()
        draw_elements()
        draw_winning_line()
        pygame.display.update()


if __name__ == "__main__":
    main()
