import numpy as np
import pygame
import sys
import os
import math

from configuration import *
from renderer import *
from game import Game


# --- PREDEFINED VARIABLES ---

# ROWS_C4 = 6
# COLUMNS_C4 = 7
# SQUARESIZE_C4 = 100
# RADIUS_C4 = SQUARESIZE_C4//2 - 10
# # WIDTH = 1200
# # HEIGHT = 800
# BOARD_WIDTH_C4 = COLUMNS_C4*SQUARESIZE_C4
# BOARD_HEIGHT_C4 = ROWS_C4*SQUARESIZE_C4
# X_OFFSET_C4 = (WIDTH - BOARD_WIDTH_C4)//2
# Y_OFFSET_C4 = 160

# ASSETS = 'Assets_MC'

# BLUE = (85,255,255)
# RED = (255,85,85)
# YELLOW = (255,255,85)
# BLACK = (0,0,0)
# WHITE = (255,255,255)

# # --- FONTS ---
# font_modern = os.path.join(ASSETS,'font_modern.otf')
# font_minecrafter = os.path.join(ASSETS,'minecrafter.ttf')
# font_pixel_purl = os.path.join(ASSETS,'pixel_purl.ttf')
# medium_font = pygame.font.Font(font_modern,36)

# --- BACKGROUND ---
c4_bg_path = os.path.join(ASSETS,'connect4_bg.jpeg')
c4_bg_img = pygame.image.load(c4_bg_path).convert()
c4_GAME_BG = pygame.transform.scale(c4_bg_img,(WIDTH,HEIGHT))


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

# def text_with_shadow(screen,text,font,c_x,c_y,color,color_shadow="BLACK"):
#     # --- Shadow (offset of 4 pixels) ---
#     shadow = font.render(text, False, color_shadow)
#     shadow_rect = shadow.get_rect(center=(c_x + 4, c_y + 4))
#     screen.blit(shadow, shadow_rect)
    
#     # --- Main Text ---
#     label = font.render(text, False, color)
#     label_rect = label.get_rect(center=(c_x, c_y))
#     screen.blit(label, label_rect)



# def game_window(game,screen,player1,player2,winner,win_color):

#     screen.blit(c4_GAME_BG,(0,0))

#     # --- ADDING A TRANSLUCENT SURFACE TO THE BOARD ---
#     overlay = pygame.Surface((BOARD_WIDTH_C4+40,BOARD_HEIGHT_C4+40),pygame.SRCALPHA)
#     overlay.set_alpha(80)
#     overlay.fill(BLACK)
#     screen.blit(overlay,(X_OFFSET_C4-20,Y_OFFSET_C4-20))

#     # --- DRAW THE UI TEXT ---
#     text_with_shadow(screen, "CONNECT 4",pygame.font.Font(font_minecrafter,44),WIDTH//2,50,WHITE)

#     if not game.game_over:
#         if game.player == 1:
#             text_with_shadow(screen,f"{player1}'s Turn",pygame.font.Font(font_pixel_purl,44),WIDTH//2,110,RED_RGBA,BLACK)
#         else:
#             text_with_shadow(screen,f"{player2}'s Turn",pygame.font.Font(font_pixel_purl,44),WIDTH//2,110,BLUE_RGBA,BLACK)


#     grid_layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

#     for r in range(ROWS_C4):
#         for c in range(COLUMNS_C4):


#             # --- COORDINATES OF TOP-LEFT CORNER
#             x = X_OFFSET_C4 + c*SQUARESIZE_C4
#             y = Y_OFFSET_C4 + r*SQUARESIZE_C4

#             # --- STONE BLOCK AND ITS BORDER
#             # pygame.draw.rect(overlay,(125,125,125,70),(x,y,SQUARESIZE,SQUARESIZE))
#             pygame.draw.rect(grid_layer,(0,0,0,150),(x,y,SQUARESIZE_C4,SQUARESIZE_C4),3)

#             center_x = x + SQUARESIZE_C4//2
#             center_y = y + SQUARESIZE_C4//2
                
#             # Check what number is sitting in our NumPy array
#             piece = game.board[r, c]
            
#             if piece == 0:
#                 pygame.draw.circle(grid_layer,(0,0,0,20), (center_x, center_y), RADIUS_C4)
#                 pass
#             elif piece == 1:
#                 pygame.draw.circle(grid_layer, RED_RGBA, (center_x, center_y), RADIUS_C4)
#             elif piece == -1:
#                 pygame.draw.circle(grid_layer, YELLOW, (center_x, center_y), RADIUS_C4)

#     screen.blit(grid_layer,(0,0))


#     if game.game_over:
#         banner = pygame.Surface((WIDTH, 150))
#         banner.set_alpha(220)
#         banner.fill(BLACK)
#         screen.blit(banner, (0, HEIGHT//2 - 75))
    
#         text_with_shadow(screen, f"{winner} WINS!", medium_font, WIDTH//2, HEIGHT//2 - 20, win_color)
#         text_with_shadow(screen, "Press ESC to return to Hub", medium_font, WIDTH//2, HEIGHT//2 + 40, WHITE)

#     # Push the drawing to the monitor
#     pygame.display.update()




# --- MAIN FUNCTION ---
def main(screen,player1,player2):


    my_game = Connect4()
    win_font = pygame.font.SysFont("monospace", 75)
    winner = None
    win_color = None

    clock = pygame.time.Clock()

    # --- ANIMATION & WIN VARIABLES ---
    is_anim,anim_col,anim_target_row,anim_y,anim_player = False,0,0,0,0
    DROP_SPEED = 40
    win_data = (None,None)
    


    while not my_game.game_over:

        clock.tick(60)

        # game_window(my_game,screen,player1,player2,winner,win_color)
        anim_state = (is_anim,anim_col,anim_y,anim_player)
        connect4_frame(screen,my_game,player1,player2,c4_GAME_BG,anim_state,win_data)


        # --- EVENTS : CONNECT4 ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            
            if event.type == pygame.MOUSEBUTTONDOWN and not is_anim:
                posx = event.pos[0]

                if posx>=X_OFFSET_C4 and posx<=X_OFFSET_C4+BOARD_WIDTH_C4:
                    col = int(math.floor((posx-X_OFFSET_C4)/SQUARESIZE_C4))
                    row = my_game.get_available_row(col)

                if row is not None:
                    is_anim = True
                    anim_col,anim_target_row,anim_player = col,row,my_game.player
                    anim_y = Y_OFFSET_C4 - SQUARESIZE_C4
                    # my_game.drop_piece(row,col)

                    # win_status = my_game.check_win()
                    
                    # if win_status == 1:
                    #     winner = player1
                    #     my_game.game_over = True
                        
                    # elif win_status == -1:
                    #     winner = player2
                    #     my_game.game_over = True
                        
                    # elif my_game.is_full():
                    #     my_game.game_over = True


                    # my_game.switch_turns()

                else:
                    label = win_font.render("Select some other column.",1,BLUE_RGBA)
                    screen.blit(label,(40,10))

        if is_anim:
            target_y = Y_OFFSET_C4 + (anim_target_row*SQUARESIZE_C4)
            anim_y +=DROP_SPEED

            if anim_y>=target_y:
                anim_y = target_y
                is_anim = False
                
                my_game.drop_piece(anim_target_row,anim_col)


                if my_game.check_win() == 1:
                    my_game.game_over = True
                    win_data = (player1,RED_RGBA)

                elif my_game.check_win() == -1:
                    my_game.game_over = True
                    win_data(player2,BLUE_RGBA)

                my_game.switch_turns()

                

if __name__ == "__main__":
    main()