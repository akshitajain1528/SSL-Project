import pygame
import sys
import numpy as np
from game import Game

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
player=1

# Background
background = pygame.image.load("Origin.jpg").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# numpy array representing the board
board = np.zeros((BOARD_ROWS, BOARD_COLS), dtype=int)


# Game object
g = Game()

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


def mark_square(row, col):
    global player
    board[row][col] = player   


def available_square(row, col):
    return board[row][col] == 0


def check_win(player):
    global winning_line

    # horizontal
    horizontal = board[:,:-4] + board[:,1:-3] + board[:,2:-2] + board[:,3:-1] + board[:,4:]
    rows, cols = np.where(horizontal == 5 * player)
    if len(rows) > 0:
        r, c = rows[0], cols[0]
        winning_line = (
            (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE // 2),
            ((c + 5) * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE // 2)
        )
        return True

    # vertical
    vertical = board[:-4,:] + board[1:-3,:] + board[2:-2,:] + board[3:-1,:] + board[4:,:]
    rows, cols = np.where(vertical == 5 * player)
    if len(rows) > 0:
        r, c = rows[0], cols[0]
        winning_line = (
            (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE),
            (c * SQUARE_SIZE + SQUARE_SIZE // 2, (r + 5) * SQUARE_SIZE)
        )
        return True

    # diagonal  (top-left to bottom-right)
    diag_off = board[:-4,:-4] + board[1:-3,1:-3] + board[2:-2,2:-2] + board[3:-1,3:-1] + board[4:,4:]
    rows, cols = np.where(diag_off == 5 * player)
    if len(rows) > 0:
        r, c = rows[0], cols[0]
        winning_line = (
            (c * SQUARE_SIZE, r * SQUARE_SIZE),
            ((c + 5) * SQUARE_SIZE, (r + 5) * SQUARE_SIZE)
        )
        return True

    # off diagonal  (top-right to bottom-left)
    diag_main = board[:-4,4:] + board[1:-3,3:-1] + board[2:-2,2:-2] + board[3:-1,1:-3] + board[4:,:-4]
    rows, cols = np.where(diag_main == 5 * player)
    if len(rows) > 0:
        r, c = rows[0], cols[0]
        winning_line = (
            ((c + 5) * SQUARE_SIZE, r * SQUARE_SIZE),
            (c * SQUARE_SIZE, (r + 5) * SQUARE_SIZE)
        )
        return True

    return False


def main(screen, player1, player2):
    global game_over, player

    clock = pygame.time.Clock()
    game_over = False 
    player=1 

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # --- BACK TO HUB ---
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return # exits this game and goes back

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX, mouseY = event.pos
                col = mouseX // SQUARE_SIZE
                row = mouseY // SQUARE_SIZE
            

                if available_square(row, col):
                    mark_square(row, col)

                    if check_win(player):
                        game_over = True

                    player *= -1

        # Drawing
        screen.blit(background, (0, 0))
        draw_grid()
        draw_elements()
        draw_winning_line()
        pygame.display.update()


if __name__ == "__main__":
    main(screen, None, None)