import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800,800
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

# Colors used
PINK= (255, 0, 102)
PURPLE=(153, 51, 255)
BLACK = (0, 0, 0)

# background image
background = pygame.image.load("Origin.jpg").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# board state: 0 - empty, 1 - player 1, 2 - player 2
board = [[0 for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
player = 1
game_over = False
winning_line = None  # stores coordinates


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
            elif board[row][col] == 2:
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
        pygame.draw.line(screen, (0, 255, 0),
                         winning_line[0], winning_line[1], 8)


def mark_square(row, col, player):
    board[row][col] = player


def available_square(row, col):
    return board[row][col] == 0


def check_win(player):
    # gobal is used because we need to update the winning_line variable defined outside this function
    global winning_line

    # Horizontal
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 4):
            if all(board[row][col + i] == player for i in range(5)):
                y = row * SQUARE_SIZE + SQUARE_SIZE // 2
                x1 = col * SQUARE_SIZE + SQUARE_SIZE // 2
                x2 = (col + 4) * SQUARE_SIZE + SQUARE_SIZE // 2
                winning_line = ((x1, y), (x2, y))
                return True

    # Vertical
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 4):
            if all(board[row + i][col] == player for i in range(5)):
                x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                y1 = row * SQUARE_SIZE + SQUARE_SIZE // 2
                y2 = (row + 4) * SQUARE_SIZE + SQUARE_SIZE // 2
                winning_line = ((x, y1), (x, y2))
                return True

    # Diagonal down
    for row in range(BOARD_ROWS - 4):
        for col in range(BOARD_COLS - 4):
            if all(board[row + i][col + i] == player for i in range(5)):
                x1 = col * SQUARE_SIZE + SQUARE_SIZE // 2
                y1 = row * SQUARE_SIZE + SQUARE_SIZE // 2
                x2 = (col + 4) * SQUARE_SIZE + SQUARE_SIZE // 2
                y2 = (row + 4) * SQUARE_SIZE + SQUARE_SIZE // 2
                winning_line = ((x1, y1), (x2, y2))
                return True

    # Diagonal up
    for row in range(4, BOARD_ROWS):
        for col in range(BOARD_COLS - 4):
            if all(board[row - i][col + i] == player for i in range(5)):
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
                        print(f"Player {player} wins!")
                        game_over = True

                    player = 2 if player == 1 else 1

        screen.blit(background, (0, 0))
        draw_grid()
        draw_elements()
        draw_winning_line()
        pygame.display.update()


if __name__ == "__main__":
    main()
