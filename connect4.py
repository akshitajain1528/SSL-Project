import numpy as np
import pygame
import sys
import os
import math

from configuration import *
from renderer import *
from game import Game


# --- BACKGROUND ---
c4_bg_path = os.path.join(ASSETS,'connect4_bg.jpeg')
c4_bg_img = pygame.image.load(c4_bg_path).convert()
C4_GAME_BG = pygame.transform.scale(c4_bg_img,(WIDTH,HEIGHT))

c4_pause_bg = os.path.join(ASSETS,'pause_c4.PNG')
c4_pause_bg = pygame.image.load(c4_pause_bg).convert()
C4_PAUSE_BG = pygame.transform.scale(c4_pause_bg,(WIDTH,HEIGHT))


class Connect4(Game):
    

    def __init__(self):
        self.board_shape = (ROWS_C4,COLUMNS_C4)

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
        # --- HORIZONTAL ---
        horizontal = self.board[:,:-3] + self.board[:,1:-2] + self.board[:,2:-1] + self.board[:,3:]
        if np.any(horizontal == 4): return 1
        if np.any(horizontal == -4): return -1


        #--- VERTICAL ---
        vertical = self.board[:-3,:] + self.board[1:-2,:] + self.board[2:-1,:] + self.board[3:,:]
        if np.any(vertical == 4): return 1
        if np.any(vertical == -4): return -1

        # ---  OFF-DIAGONAL ---
        diag_off = self.board[:-3,:-3] + self.board[1:-2,1:-2] + self.board[2:-1,2:-1] + self.board[3:,3:]
        if np.any(diag_off == 4): return 1
        if np.any(diag_off == -4): return -1

        # --- MAIN-DIAGONAL
        diag_main = self.board[:-3,3:] + self.board[2:-1,1:-2] + self.board[1:-2,2:-1] + self.board[3:,:-3]
        if np.any(diag_main == 4): return 1
        if np.any(diag_main == -4): return -1

        # --- TIE ---
        elif self.is_full():
            return 0

        return None



# --- MAIN FUNCTION ---
def main(screen,player1,player2,avatar_left,avatar_right):


    my_game = Connect4()
    clock = pygame.time.Clock()

    # --- ANIMATION & WIN VARIABLES ---
    is_anim,anim_col,anim_target_row,anim_y,anim_player = False,0,0,0,0
    DROP_SPEED = 30
    win_data = (None,None,None)
    running = True

    # ---  BACK AND MENU BUTTONS ---
    back_button = pygame.Rect(50,50,150,60)
    gm_menu_button = pygame.Rect(WIDTH//2 - 150, HEIGHT//2, 300, 50)
    resume_button = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 70, 300, 50)

    is_paused = False
    # back_hovering = back_button.collidepoint((mx,my))


    while running:

        clock.tick(60)
        mx,my = pygame.mouse.get_pos()

        anim_state = (is_anim,anim_col,anim_y,anim_player)
        connect4_frame(screen,my_game,player1,player2,avatar_left,avatar_right,C4_GAME_BG,anim_state,win_data)

        h_back = back_button.collidepoint((mx, my))
        menu_button(screen, back_button, "BACK", h_back, small_font)

        if is_paused:
            darken = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            darken.fill((0, 0, 0, 150))
            screen.blit(darken, (0, 0))

            screen.blit(C4_PAUSE_BG,(0,0))
            # pygame.draw.rect(screen, WHITE, pm_rect, 4, border_radius=10)

            text_with_shadow(screen, "TOO EARLY??", title_font, WIDTH//2, HEIGHT//2 - 100, RED_RGBA)
            
            h_pm_menu = gm_menu_button.collidepoint((mx, my))
            menu_button(screen, gm_menu_button, "GAME MENU", h_pm_menu, small_font)
            
            h_pm_resume = resume_button.collidepoint((mx, my))
            menu_button(screen, resume_button, "BACK TO GAME", h_pm_resume, small_font)

        # ONE SINGLE UPDATE CALL AT THE VERY END
        pygame.display.update()

        # --- EVENTS : CONNECT4 ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return win_data[0]
            
            if is_paused:
                if gm_menu_button.collidepoint((mx,my)):
                    return
                elif resume_button.collidepoint((mx,my)):
                    is_paused = False
            
            else:
                if back_button.collidepoint((mx,my)):
                    is_paused = True
                
                elif event.type == pygame.MOUSEBUTTONDOWN and not is_anim and not my_game.game_over:

                    hover_row = int((my-Y_OFFSET_C4)//SQUARESIZE_C4)
                    sprite_y = Y_OFFSET_C4 + (hover_row*SQUARESIZE_C4) + 10


                    if mx>=X_OFFSET_C4 and mx<=X_OFFSET_C4+BOARD_WIDTH_C4:
                        col = int(math.floor((mx-X_OFFSET_C4)/SQUARESIZE_C4))
                        row = my_game.get_available_row(col)

                        if row is not None:
                            is_anim = True
                            anim_col,anim_target_row,anim_player = col,row,my_game.player
                            anim_y = sprite_y



        if is_anim:
            target_y = Y_OFFSET_C4 + (anim_target_row*SQUARESIZE_C4)
            anim_y +=DROP_SPEED

            if anim_y>=target_y:
                anim_y = target_y
                is_anim = False
                
                my_game.drop_piece(anim_target_row,anim_col)


                if my_game.check_win() == 1:
                    my_game.game_over = True
                    win_data = (player1,BLUE_RGBA,avatar_left)

                elif my_game.check_win() == -1:
                    my_game.game_over = True
                    win_data = (player2,RED_RGBA,avatar_right)

                elif my_game.check_win() == 0:
                    my_game.game_over = True
                    win_data = ("Tie",YELLOW,None)

                my_game.switch_turns()

        pygame.display.update()

                

if __name__ == "__main__":
    main()