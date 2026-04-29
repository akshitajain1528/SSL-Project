import pygame
import sys
import numpy as np
from main_hub import Game

from Core.configuration import *
from Core.renderer import *

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Background
background = os.path.join(ASSETS,'othellobackdrop.jpeg')
background = pygame.image.load(background).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

o_pause_bg = os.path.join(ASSETS,'pause_o.PNG')
o_pause_bg = pygame.image.load(o_pause_bg).convert()
O_PAUSE_BG = pygame.transform.scale(o_pause_bg,(WIDTH,HEIGHT))


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
                return 0  
        return None  


def main(screen, player1, player2,avatar_left,avatar_right,is_league=False):

    my_game = Othello()
    clock = pygame.time.Clock()
    winner, win_color,win_avatar = None, None, None

    # --- BACK AND MENU BUTTONS ---
    back_button = pygame.Rect(50,50,150,60)
    gm_menu_button = pygame.Rect(WIDTH//2 + 250,HEIGHT//2, 300, 50)
    resume_button = pygame.Rect(WIDTH//2 + 250, HEIGHT//2 + 70, 300, 50)

    # --- PLAY AGAIN & LEADERBOARDS BUTTON ---
    btn_start_again = pygame.Rect(WIDTH//2 - 150, HEIGHT - 280, 300, 50)
    btn_leaderboard = pygame.Rect(WIDTH//2 - 150, HEIGHT - 210, 300, 50)

    is_paused = False
    display_message = ""
    message_timer = 0
    hover = False

    while True:
        othello_frame(screen, my_game, background, player1, player2,avatar_left,avatar_right, winner, win_color,win_avatar,is_league)

        clock.tick(60)
        mx,my = pygame.mouse.get_pos()

        # --- BACK BUTTON ---
        h_back = back_button.collidepoint((mx, my))
        if not my_game.game_over:
            menu_button(screen, back_button, "BACK", h_back, small_font)

        if is_paused:
            screen.blit(O_PAUSE_BG,(0,0))

            text_with_shadow(screen, "PLEASE DON'T LEAVE", title_modern_font, WIDTH//2, HEIGHT//2 - 200, WHITE)
            gm_menu = gm_menu_button.collidepoint((mx, my))
            menu_button(screen, gm_menu_button, "GAME MENU", gm_menu, small_font)
            
            resume = resume_button.collidepoint((mx, my))
            menu_button(screen, resume_button, "BACK TO GAME", resume, small_font)


        # --- PLAY AGAIN & LEADERBOARDS BUTTON ---
        h_start_button = btn_start_again.collidepoint((mx,my))
        h_game_leaderboard = btn_leaderboard.collidepoint((mx,my))

        if my_game.game_over:
            menu_button(screen,btn_start_again,"START AGAIN",h_start_button,small_font)
            menu_button(screen,btn_leaderboard,"LEADERBOARD",h_game_leaderboard,small_font)


        # 2. League Button Logic 
        if my_game.game_over and is_league:
            btn_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT - 100, 300, 50)
            hover = btn_rect.collidepoint(pygame.mouse.get_pos())
            menu_button(screen, btn_rect, "SHOW RESULTS", hover, small_font)

        # 3. Message Banner Logic
        if display_message:
            current_time = pygame.time.get_ticks()
            if current_time - message_timer < 3000:
                banner = pygame.Surface((WIDTH, 150))
                banner.set_alpha(220)
                banner.fill(BLACK)
                screen.blit(banner, (0, HEIGHT//2 - 75))
                text_with_shadow(screen, display_message, medium_font, WIDTH//2, HEIGHT//2 - 20, WHITE)
            else:
                display_message = ""

        # 4. Event Handling
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

            if event.type == pygame.KEYDOWN and my_game.game_over:
                if event.key == pygame.K_ESCAPE:
                    return winner
                
            if event.type == pygame.MOUSEBUTTONDOWN and is_paused:
                if gm_menu_button.collidepoint((mx,my)):
                    return "GAME_MENU"
                elif resume_button.collidepoint((mx,my)):
                    is_paused = False
            else:
                if event.type == pygame.MOUSEBUTTONDOWN and h_back and not my_game.game_over:
                    is_paused = True 
                
                if event.type == pygame.MOUSEBUTTONDOWN and my_game.game_over:
                    if h_game_leaderboard:
                        return "GO_TO_LEADERBOARD"
                    if h_start_button:
                        return "STARTAGAIN"

         
                elif event.type == pygame.MOUSEBUTTONDOWN and not my_game.game_over:

                    if X_OFFSET_OTHELLO <= mx <= WIDTH - X_OFFSET_OTHELLO and Y_OFFSET_OTHELLO + 30 < my <= HEIGHT - 20:
                        col = (mx - X_OFFSET_OTHELLO) // SQUARESIZE_OTHELLO
                        row = (my - 55 - Y_OFFSET_OTHELLO) // SQUARESIZE_OTHELLO

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
                win_color = (153,153,153) 
                win_avatar =  avatar_left 
                
            elif winner_code == -1:
                winner = player2            
                win_color = (183, 49, 204)
                win_avatar = avatar_right    
                
            else:
                winner = "draw"            
                win_color = (255, 255, 255) 
                win_avatar = None
        
        # if display_message:
        #     current_time = pygame.time.get_ticks()
        #     if current_time - message_timer < 3000: 
                

        #             banner = pygame.Surface((WIDTH, 150))
        #             banner.set_alpha(220)
        #             banner.fill(BLACK)
        #             screen.blit(banner, (0, HEIGHT//2 - 75))
    
        #             text_with_shadow(screen,display_message, medium_font, WIDTH//2, HEIGHT//2 - 20, WHITE)
                
        #     else:
        #         display_message = ""

        pygame.display.update()


if __name__ == "__main__":
    main(screen, None, None)