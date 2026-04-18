import numpy as np
import pygame
import sys
import math
from game import Game

ROWS = 6
COLUMNS = 7
SQUARESIZE = 100
RADIUS = int(100/2 - 5)

BLUE = (0,0,255)
RED = (255,0,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)

class Connect4(Game):
    

    def __init__(self):
        self.board_shape = (ROWS,COLUMNS)

        self.reset()

    # --- Specific functions for connect4 ---

    def get_available_row(self,col):
        indices = np.where(self.board[:,col]==0)[0]
        if len(indices) > 0:
            return indices[-1]
        else:
            return None        
    
    def drop_piece(self,row,col):
        self.board[row,col] = self.player

    

    def check_win(self):
        # horizontal
        horizontal = self.board[:,:-3] + self.board[:,1:-2] + self.board[:,2:-1] + self.board[:,3:]
        if np.any(horizontal == 4): return 1
        if np.any(horizontal == -4): return -1


        #vertical
        vertical = self.board[:-3,:] + self.board[1:-2,:] + self.board[2:-1,:] + self.board[3:,:]
        if np.any(vertical == 4): return 1
        if np.any(vertical == -4): return -1

        #off-diagonal
        diag_off = self.board[:-3,:-3] + self.board[1:-2,1:-2] + self.board[2:-1,2:-1] + self.board[3:,3:]
        if np.any(diag_off == 4): return 1
        if np.any(diag_off == -4): return -1

        #main-diagonal
        diag_main = self.board[:-3,3:] + self.board[2:-1,1:-2] + self.board[1:-2,2:-1] + self.board[3:,:-3]
        if np.any(diag_main == 4): return 1
        if np.any(diag_main == -4): return -1

        return 0


# --- FRONT-END ---

    def draw_grid(self,screen):

        pygame.draw.rect(screen,BLUE,(0,SQUARESIZE,SQUARESIZE*COLUMNS,SQUARESIZE*ROWS))

        for r in range(ROWS):
            for c in range(COLUMNS):

                center_x = int(c * SQUARESIZE + SQUARESIZE / 2)
                center_y = int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)
                    
                    # Check what number is sitting in our NumPy array
                piece = self.board[r, c]
                
                if piece == 0:
                    pygame.draw.circle(screen, BLACK, (center_x, center_y), RADIUS)
                elif piece == 1:
                    pygame.draw.circle(screen, RED, (center_x, center_y), RADIUS)
                elif piece == -1:
                    pygame.draw.circle(screen, YELLOW, (center_x, center_y), RADIUS)

        # Push the drawing to the monitor
        pygame.display.update()


        # --- Main function ---


def main(screen,player1,player2):


    my_game = Connect4()
    my_game.draw_grid(screen)
    win_font = pygame.font.SysFont("monospace", 75)

    clock = pygame.time.Clock()

    while not my_game.game_over:

        clock.tick()

        # --- if quit ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            
            if event.type == pygame.MOUSEBUTTONDOWN:

                pygame.draw.rect(screen, BLACK, (0, 0, SQUARESIZE*COLUMNS, SQUARESIZE))

                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                row = my_game.get_available_row(col)

                if row is not None:
                    my_game.board[row,col] = my_game.player

                    win_status = my_game.check_win()
                    
                    if win_status == 1:
                        label = win_font.render("Player 1 Wins!", 1, RED)
                        screen.blit(label, (40, 10)) # Draw text at X=40, Y=10
                        my_game.game_over = True
                        
                    elif win_status == -1:
                        label = win_font.render("Player 2 Wins!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        my_game.game_over = True
                        
                    elif my_game.is_full():
                        label = win_font.render("It's a Tie!", 1, BLUE)
                        screen.blit(label, (40, 10))
                        my_game.game_over = True

                    

                    my_game.switch_turns()
                else:
                    label = win_font.render("Select some other column.",1,BLUE)
                    screen.blit(label,(40,10))
                
                my_game.draw_grid(screen)

    if my_game.game_over:
        pygame.time.wait(5000)



if __name__ == "__main__":
    main()