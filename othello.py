import pygame
import sys
import numpy as np
from game import Game

from configuration import *
from renderer import *

screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Tic tac toe")

# Background
background = pygame.image.load("Assets_MC/othellobackdrop.jpeg").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))


class Othello(Game):

    def __init__(self):
        self.board_shape = (ROWS_OTHELLO,COLS_OTHELLO)
        self.reset()
        self.board[3, 3] = -1
        self.board[3, 4] = 1
        self.board[4, 3] = 1
        self.board[4, 4] = -1 

    def switch_possible(self, row, col, dr, dc, player):
        # Check if we can flip pieces in direction (dr, dc)
        r, c = row + dr, col + dc
        has_opponent_piece = False    
        while 0 <= r < ROWS_OTHELLO and 0 <= c < COLS_OTHELLO:
    
            if self.board[r, c] == -player:
                has_opponent_piece = True
            elif self.board[r, c] == player:
                return has_opponent_piece
            else:
                break
            r += dr
            c += dc
        return False    


    def switch_pieces(self, row, col, player):
        # Flip pieces in all 8 directions
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
          
                if self.switch_possible(row, col, dr, dc, player):
                    r, c = row + dr, col + dc
                    while self.board[r, c] == -player:
                        self.board[r, c] = player
                        r += dr
                        c += dc 

    def has_any_valid_move(self, player):
        for r in range(ROWS_OTHELLO):
            for c in range(ROWS_OTHELLO):
                if self.board[r, c] == 0:
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            if self.switch_possible(r, c, dr, dc, player):
                                return True 
        return False  
        

    def board_full(self):
        return np.all(self.board != 0)

    def win_count(self, player):
        return np.sum(self.board == player)

    def win_check(self, player):
        black_count = self.win_count(1)
        white_count = self.win_count(-1)
        
        if black_count + white_count == ROWS_OTHELLO * COLS_OTHELLO or black_count == 0 or white_count == 0:
            if black_count > white_count:
                return 1
            elif white_count > black_count:
                return -1
            else:
                return 0  # tie
        return None  # game not over


def main(screen, player1, player2):

    my_game = Othello()
    clock = pygame.time.Clock()
    winner, win_color = None, None
    

    display_message = ""
    message_timer = 0
    font = pygame.font.Font(None, 48)

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return winner

         
            if event.type == pygame.MOUSEBUTTONDOWN and not my_game.game_over:
                mouseX, mouseY = event.pos
                if X_OFFSET_OTHELLO <= mouseX <= WIDTH - X_OFFSET_OTHELLO and Y_OFFSET_OTHELLO + 30 < mouseY <= HEIGHT - 20:
                    col = (mouseX - X_OFFSET_OTHELLO) // SQUARESIZE_OTHELLO
                    row = (mouseY - 55 - Y_OFFSET_OTHELLO) // SQUARESIZE_OTHELLO

                    if my_game.board[row, col] == 0:
                        valid_move = False

                        for dr in [-1, 0, 1]:
                            for dc in [-1, 0, 1]:
                                if dr == 0 and dc == 0:
                                    continue
                                if my_game.switch_possible(row, col, dr, dc, my_game.player):
                                    valid_move = True

                        if valid_move:
                            my_game.board[row, col] = my_game.player
                            my_game.switch_pieces(row, col, my_game.player)
                            my_game.player *= -1

                            if not my_game.has_any_valid_move(my_game.player) and not my_game.board_full():
                                p_name = player1 if my_game.player == 1 else player2
                                display_message = f"No moves for {p_name}! Turn skipped."
                                message_timer = pygame.time.get_ticks()
                                my_game.player *= -1 


        winner_code = my_game.win_check(my_game.player)
        
        if winner_code is not None:
            my_game.game_over = True
            
            if winner_code == 1:
                winner = player1            
                win_color = (0, 200, 255)    
                
            elif winner_code == -1:
                winner = player2            
                win_color = (255, 215, 0)    
                
            else:
                winner = "draw"            
                win_color = (255, 255, 255) 

        othello_frame(screen, my_game, background, player1, player2, winner, win_color)
        
        if display_message:
            current_time = pygame.time.get_ticks()
            if current_time - message_timer < 3000: 
                

                    banner = pygame.Surface((WIDTH, 150))
                    banner.set_alpha(220)
                    banner.fill(BLACK)
                    screen.blit(banner, (0, HEIGHT//2 - 75))
    
                    text_with_shadow(screen,display_message, medium_font, WIDTH//2, HEIGHT//2 - 20, WHITE)
                
            else:
                display_message = ""

        pygame.display.update()


if __name__ == "__main__":
    main(screen, None, None)