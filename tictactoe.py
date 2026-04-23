import pygame
import sys
import numpy as np
from game import Game

from configuration import *
from renderer import *



screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic tac toe")


# Background
background = pygame.image.load("Assets_MC/nether.jpeg").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))



class TicTacToe(Game):

    def __init__(self):
        self.board_shape = (ROWS_TTT,COLS_TTT)
        self.reset()
        self.winning_line = None
        self.win_anim_progress = 0.0


    def draw_winning_line(self):
        if self.winning_line:
            pygame.draw.line(screen, GREEN, self.winning_line[0], self.winning_line[1], 5)


    def mark_square(self,row, col):
        # global player
        self.board[row][col] = self.player   


    def available_square(self,row, col):
        return self.board[row][col] == 0


    def check_win(self):

        # horizontal
        horizontal = self.board[:,:-4] + self.board[:,1:-3] + self.board[:,2:-2] + self.board[:,3:-1] + self.board[:,4:]
        rows, cols = np.where(horizontal == 5 * self.player)
        if len(rows) > 0:
            r, c = rows[0], cols[0]
            self.winning_line = (
                (X_OFFSET_TTT + c * SQUARESIZE_TTT, Y_OFFSET_TTT + 55 + r * SQUARESIZE_TTT + SQUARESIZE_TTT // 2),
                (X_OFFSET_TTT + (c + 5) * SQUARESIZE_TTT, Y_OFFSET_TTT + 55 + r * SQUARESIZE_TTT + SQUARESIZE_TTT // 2)
            )
            return self.player

        # vertical
        vertical = self.board[:-4,:] + self.board[1:-3,:] + self.board[2:-2,:] + self.board[3:-1,:] + self.board[4:,:]
        rows, cols = np.where(vertical == 5 * self.player)
        if len(rows) > 0:
            r, c = rows[0], cols[0]
            self.winning_line = (
                (X_OFFSET_TTT + c * SQUARESIZE_TTT + SQUARESIZE_TTT // 2,Y_OFFSET_TTT + 55 + r * SQUARESIZE_TTT),
                (X_OFFSET_TTT + c * SQUARESIZE_TTT + SQUARESIZE_TTT // 2,Y_OFFSET_TTT + 55 + (r + 5) * SQUARESIZE_TTT)
            )
            return self.player

        # diagonal  (top-left to bottom-right)
        diag_off = self.board[:-4,:-4] + self.board[1:-3,1:-3] + self.board[2:-2,2:-2] + self.board[3:-1,3:-1] + self.board[4:,4:]
        rows, cols = np.where(diag_off == 5 * self.player)
        if len(rows) > 0:
            r, c = rows[0], cols[0]
            self.winning_line = (
                (X_OFFSET_TTT + c * SQUARESIZE_TTT,Y_OFFSET_TTT + 55 + r * SQUARESIZE_TTT),
                (X_OFFSET_TTT + (c + 5) * SQUARESIZE_TTT,Y_OFFSET_TTT + 55 + (r + 5) * SQUARESIZE_TTT)
            )
            return self.player

        # off diagonal  (top-right to bottom-left)
        diag_main = self.board[:-4,4:] + self.board[1:-3,3:-1] + self.board[2:-2,2:-2] + self.board[3:-1,1:-3] + self.board[4:,:-4]
        rows, cols = np.where(diag_main == 5 * self.player)
        if len(rows) > 0:
            r, c = rows[0], cols[0]
            self.winning_line = (
                (X_OFFSET_TTT + (c + 5) * SQUARESIZE_TTT,Y_OFFSET_TTT + 55 + r * SQUARESIZE_TTT),
                (X_OFFSET_TTT + c * SQUARESIZE_TTT,Y_OFFSET_TTT + 55 + (r + 5) * SQUARESIZE_TTT)
            )
            return self.player

        return False


def main(screen, player1, player2):
    my_game = TicTacToe()
    

    # global game_over, player

    clock = pygame.time.Clock()
    # game_over = False  
    winner,win_color = None,None
    while True:

        ttt_frame(screen,my_game,background,player1,player2,winner,win_color)
        clock.tick(60)

        # --- LINE ---
        if my_game.winning_line and my_game.game_over:
            my_game.win_anim_progress = min(1.0,my_game.win_anim_progress+0.05,)

        
        # --- EVENTS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # --- BACK TO HUB ---
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return # exits this game and goes back

            if event.type == pygame.MOUSEBUTTONDOWN and not my_game.game_over:
                mouseX, mouseY = event.pos
                if X_OFFSET_TTT<=mouseX<=WIDTH-X_OFFSET_TTT and Y_OFFSET_TTT+30<mouseY<=HEIGHT-20:
                    col = (mouseX - X_OFFSET_TTT)//SQUARESIZE_TTT
                    row = (mouseY - 55 - Y_OFFSET_TTT) // SQUARESIZE_TTT

                    if my_game.available_square(row, col):
                        my_game.mark_square(row, col)

                        if my_game.check_win() == 1:
                            my_game.game_over = True
                            winner = player1
                            win_color = BLUE_RGBA
                        elif my_game.check_win() == -1:
                            my_game.game_over = True
                            winner = player2
                            win_color = YELLOW

                        my_game.switch_turns()


if __name__ == "__main__":
    main(screen, None, None)