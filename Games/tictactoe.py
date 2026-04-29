import pygame
import sys
import numpy as np
from game import Game

from Core.configuration import *
from Core.renderer import *



screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic tac toe")


# Background
background = pygame.image.load("Assets_MC/nether.jpeg").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

ttt_pause_bg = os.path.join(ASSETS,'pause_ttt.PNG')
ttt_pause_bg = pygame.image.load(ttt_pause_bg).convert()
TTT_PAUSE_BG = pygame.transform.scale(ttt_pause_bg,(WIDTH,HEIGHT))


class TicTacToe(Game):

    def __init__(self):
        self.board_shape = (ROWS_TTT,COLS_TTT)
        self.reset()
        self.winning_line = None
        self.win_anim_progress = 0.0


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

        elif self.is_full():
            return 0
        
        return None



def main(screen, player1, player2, avatar_left, avatar_right, is_league=False):
    my_game = TicTacToe()
    
    # global game_over, player
    clock = pygame.time.Clock()
    # game_over = False  
    winner,win_color,win_avatar = None,None,None

    # --- BACK AND MENU BUTTONS ---
    back_button = pygame.Rect(50,50,150,60)
    gm_menu_button = pygame.Rect(WIDTH//2 - 350,HEIGHT//2, 300, 50)
    resume_button = pygame.Rect(WIDTH//2 - 350, HEIGHT//2 + 70, 300, 50)

    is_paused = False
    hover = False

    while True:
        ttt_frame(screen, my_game, background, player1, player2, avatar_left, avatar_right, winner, win_color, win_avatar, is_league)
        clock.tick(60)
        mx,my = pygame.mouse.get_pos()

        # --- BACK BUTTON ---
        h_back = back_button.collidepoint((mx, my))
        if not my_game.game_over:
            menu_button(screen, back_button, "BACK", h_back, small_font)

        if is_paused:
            screen.blit(TTT_PAUSE_BG,(0,0))

            text_with_shadow(screen, "PLEASE DON'T LEAVE", title_modern_font, WIDTH//2, HEIGHT//2 - 100, WHITE)
            gm_menu = gm_menu_button.collidepoint((mx, my))
            menu_button(screen, gm_menu_button, "GAME MENU", gm_menu, small_font)
            
            resume = resume_button.collidepoint((mx, my))
            menu_button(screen, resume_button, "BACK TO GAME", resume, small_font)

        if my_game.winning_line and my_game.game_over:
            my_game.win_anim_progress = min(1.0, my_game.win_anim_progress + 0.03)
            
            if is_league:
                btn_text = "SHOW RESULTS" if "othello" in sys.modules[__name__].__file__ else "NEXT GAME"
                btn_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT - 100, 300, 50)
                hover = btn_rect.collidepoint(pygame.mouse.get_pos())
                menu_button(screen, btn_rect, btn_text, hover, small_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if my_game.game_over and is_league and hover:
                    return winner

            if event.type == pygame.KEYDOWN and not my_game.game_over:
                if event.key == pygame.K_ESCAPE:
                    is_paused = True
                    # return winner # EXITS THIS GAME AND GOES BACK
                
            if event.type == pygame.MOUSEBUTTONDOWN and is_paused:
                if gm_menu_button.collidepoint((mx,my)):
                    return
                elif resume_button.collidepoint((mx,my)):
                    is_paused = False
            else:
                if event.type == pygame.MOUSEBUTTONDOWN and h_back and not my_game.game_over:
                    is_paused = True   

                elif event.type == pygame.MOUSEBUTTONDOWN and not my_game.game_over:

                    if X_OFFSET_TTT <= mx <= WIDTH - X_OFFSET_TTT and Y_OFFSET_TTT + 30 < my <= HEIGHT - 20:
                        col = (mx - X_OFFSET_TTT) // SQUARESIZE_TTT
                        row = (my - 55 - Y_OFFSET_TTT) // SQUARESIZE_TTT

                        if X_OFFSET_TTT<=mx<=WIDTH-X_OFFSET_TTT and Y_OFFSET_TTT+30<my<=HEIGHT-20:
                            col = (mx - X_OFFSET_TTT)//SQUARESIZE_TTT
                            row = (my - 55 - Y_OFFSET_TTT) // SQUARESIZE_TTT

                            if my_game.available_square(row, col):
                                my_game.mark_square(row, col)

                                if my_game.check_win() == 1:
                                    my_game.game_over = True
                                    winner = player1
                                    win_color = BLUE_RGBA
                                    win_avatar = avatar_left
                                    
                                elif my_game.check_win() == -1:
                                    my_game.game_over = True
                                    winner = player2
                                    win_color = YELLOW
                                    win_avatar = avatar_right

                                elif my_game.check_win() == 0:
                                    my_game.game_over = True
                                    winner = "Tie"
                                    win_color = RED_RGBA

                            # if my_game.game_over:
                            #     return winner

                        my_game.switch_turns()

        pygame.display.update()
if __name__ == "__main__":
    main(screen, None, None)