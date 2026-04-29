import numpy as np
import pygame
import sys
import os

os.environ["SDL_AUDIODRIVER"] = "dummy" 

# ============
# Game Class
# ============

class Game:
    
    def __init__(self):
        pass 

    def draw_grid(self):
        pass

    def switch_turns(self):
        self.player *= -1

    def reset(self):
        self.board = np.zeros(self.board_shape)
        self.player = 1
        self.game_over = False

    def check_win(self):
        pass

    def is_empty(self, row, col):
        return self.board[row, col] == 0

    def is_full(self):
        return np.all(self.board != 0)
    


# --- INITIALIZING PYGAME ---
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Minecraft Game Hub")


from configuration import *
from renderer import *
from characters import *

ASSETS = 'Assets_MC'

# --- Load the BG ---
bg_path = os.path.join(ASSETS,'minecraft_bg.png')
bg_img = pygame.image.load(bg_path).convert()
GAME_BG = pygame.transform.scale(bg_img,(WIDTH,HEIGHT))


# --- SOUND EFFECTS ---
click_path = os.path.join(ASSETS,'click.mp3')
click_sound = pygame.mixer.Sound(click_path)


# ==========================
#     MAIN LOOP AAGE 
# ==========================

def main_hub(player1,player2):
    run = True
    current_state = "START_SCREEN"
    

    # --- BUTTON RECTANGLES: START SCREEN ---
    btn_start_game_menu = pygame.Rect(WIDTH//2-200,300,400,60)
    btn_start_how_to = pygame.Rect(WIDTH//2-200,400,400,60)
    btn_start_leaderboard = pygame.Rect(WIDTH//2-200,500,400,60)
    btn_start_quit = pygame.Rect(WIDTH//2-200,600,400,60)

    # --- BUTTON RECTANGLES: CHARACTERS ---
    btn_zombie_l = pygame.Rect(125,260,110,100)
    btn_pig_l = pygame.Rect(125,370,110,100)
    btn_dog_l = pygame.Rect(125,480,110,100)
    btn_steve_l = pygame.Rect(125,590,110,100)

    btn_zombie_r = pygame.Rect(975,260,110,100)
    btn_pig_r = pygame.Rect(975,370,110,100)
    btn_dog_r = pygame.Rect(975,480,110,100)
    btn_steve_r = pygame.Rect(975,590,110,100)

    # --- WIREBOXES AROUND IT ---
    box_left_panel = pygame.Rect(50,250,250,480)
    box_right_panel = pygame.Rect(WIDTH-300,250,250,480)


    # --- BUTTON RECTANGLES: GAME MENU ---
    btn_tictactoe = pygame.Rect(WIDTH//2 - 200, 300, 400, 60)
    btn_othello = pygame.Rect(WIDTH//2 - 200, 400, 400, 60)
    btn_connect4 = pygame.Rect(WIDTH//2 - 200, 500, 400, 60)
    btn_back = pygame.Rect(WIDTH//2 - 200, 650, 400, 60)
    
    # --- VARIBLES FOR CHARACTERS ---
    buttons_left,buttons_right = True,True  # TRUE WHEN LEFT/RIGHT DROP DOWN MENU IS OPEN
    avatar_left,avatar_right = None, None
    show_avatar_warning = False

    left_panel_data = {
    'panel': box_left_panel,
    'characters': {'zombie': btn_zombie_l, 'pig': btn_pig_l, 'dog': btn_dog_l, 'steve': btn_steve_l}
}
    right_panel_data = {
        'panel': box_right_panel,
        'characters': {'zombie': btn_zombie_r, 'pig': btn_pig_r, 'dog': btn_dog_r, 'steve': btn_steve_r}
    }

    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        screen.blit(GAME_BG,(0,0))

        mx,my = pygame.mouse.get_pos()



                                # ==============================================
                                # ==============================================
                                #             FRIST PAGE: START SCREEN
                                # ==============================================
                                # ==============================================

        if current_state=="START_SCREEN":

            draw_chr_panels(screen, mx, my, buttons_left, buttons_right, left_panel_data, right_panel_data)
            draw_selected_characters(screen, avatar_left, avatar_right, mx, my, small_font)

        # --- WARNING POPUP ---
            if show_avatar_warning:
                warning_box = pygame.Rect(WIDTH//2 - 450, HEIGHT - 100, 900, 50)
                pygame.draw.rect(screen, (200, 0, 0), warning_box, border_radius=2)
                pygame.draw.rect(screen, WHITE, warning_box, 3, border_radius=2)
                text_with_shadow(screen, "PLEASE SELECT BOTH AVATARS FIRST!", button_font, WIDTH//2, HEIGHT - 75, WHITE)


            # --- WELCOME TO GAMECRAFT ---
            text_with_shadow(screen,'WELCOME TO',title_font,WIDTH//2,80,WHITE)
            text_with_shadow(screen,"GAMECRAFT",title_font,WIDTH//2,200,WHITE)
            text_with_shadow(screen,f"{player1}",button_font,WIDTH//2-450,80,YELLOW)
            text_with_shadow(screen,f"{player2}",button_font,WIDTH//2+450,80,YELLOW)

            # --- HOVERABLE BUTTONS ---
            h_menu = btn_start_game_menu.collidepoint((mx,my))
            menu_button(screen,btn_start_game_menu,"GAME MENU",h_menu)

            h_play = btn_start_how_to.collidepoint((mx,my))
            menu_button(screen,btn_start_how_to,"HOW TO PLAY",h_play)

            h_leaderboard = btn_start_leaderboard.collidepoint((mx,my))
            menu_button(screen,btn_start_leaderboard,"LEADERBOARD", h_leaderboard)

            h_quit = btn_start_quit.collidepoint((mx,my))
            menu_button(screen,btn_start_quit,"QUIT",h_quit)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:

                    # --- GAME MENU BUTTON CLICK
                    if h_menu:
                        if avatar_left and avatar_right:
                            current_state = "GAME_MENU"
                            show_avatar_warning = False
                        else:
                            show_avatar_warning = True

                    if h_play:
                        current_state="HOWTOPLAY"
                        print("HOW TO PLAY")

                    
                    if h_leaderboard:
                        current_state="LEADERBOARD"
                        print("Leaderboard")

                    if h_quit:
                        pygame.quit()
                        sys.exit()



                    if avatar_left and current_state=="START_SCREEN":
                        reselect_btn_l = pygame.Rect(50, 220, 270, 45)
                        if reselect_btn_l.collidepoint((mx, my)):
                            avatar_left = None
                            buttons_left = True

                    # --- CLICKING A CHARACTER INSIDE THE LEFT MENU ---
                    if buttons_left:
                        for name, rect in left_panel_data['characters'].items():
                            if rect.collidepoint((mx, my)):  
                                avatar_left = name              
                                buttons_left = False        
                                show_avatar_warning = False

                        


                    if avatar_right and current_state=="START_SCREEN":
                        reselect_btn_l = pygame.Rect(WIDTH-320, 220, 270, 40)
                        if reselect_btn_l.collidepoint((mx, my)):
                            avatar_right = None
                            buttons_right = True

                    # --- CLICKING A CHARACTER INSIDE THE LEFT MENU ---
                    if buttons_right: 
                        for name, rect in right_panel_data['characters'].items():
                            if rect.collidepoint((mx, my)):   
                                avatar_right = name              
                                buttons_right = False     
                                show_avatar_warning = False

                

    # ====================================
    #             HOW TO PLAY
    # ====================================

        elif current_state=="HOWTOPLAY":
        
            bg = os.path.join(ASSETS,'howtoplay.jpeg')
            bg_image = pygame.image.load(bg).convert()
            howtoplay_bg = pygame.transform.scale(bg_image,(WIDTH,HEIGHT))

            screen.blit(howtoplay_bg,(0,0))

            def htp_box(screen,rect,text=""):
                pygame.draw.rect(screen,STONE_GREY,rect,width=3,border_radius=10)

                if text:
                    label = small_font.render(text,False,OBSIDIAN_BLACK)
                    screen.blit(label, label.get_rect(center=rect.center))

            # text_with_shadow(screen,f"HOW TO PLAY?",button_font,750,120,STONE_GREY)
            box_character = pygame.Rect(590,100,300,50)
            htp_box(screen,box_character,"HOW TO PLAY?")

            btn_htpback = pygame.Rect(WIDTH//2 - 480, 680, 250, 60)

            hover_back = btn_htpback.collidepoint((mx,my))
            menu_button(screen,btn_htpback, "Back",hover_back)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if hover_back:
                        current_state="START_SCREEN"

    # ====================================
    #             LEADERBOARD
    # ====================================

        elif current_state=="LEADERBOARD":

            l_bg = os.path.join(ASSETS,'download (1).jpg')
            l_bg_image = pygame.image.load(l_bg).convert()
            leaderboard_bg = pygame.transform.scale(l_bg_image,(WIDTH,HEIGHT))
            screen.blit(leaderboard_bg,(0,0))

            text_with_shadow(screen,"LEADERBOARD",title_font,WIDTH//2,80,OBSIDIAN_BLACK)

                # --- BACK BUTTON ---
            btn_lbback = pygame.Rect(WIDTH//2-125, 700, 250, 60)  
            hover_back = btn_lbback.collidepoint((mx,my))
            menu_button(screen,btn_lbback, "Back",hover_back)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if hover_back:
                        current_state="START_SCREEN"




                        # =======================================================
                        # =======================================================
                        #                   2ND PAGE: GAME MENU
                        # =======================================================
                        # =======================================================



        elif current_state=="GAME_MENU":
                # --- CHARACTER ---
            rect_left = pygame.Rect(50,150,200,50)
            rect_right = pygame.Rect(WIDTH-250,150,200,50)
            wireframe_box(screen, rect_left, "CHARACTER")
            wireframe_box(screen, rect_right, "CHARACTER")


            avatar = pygame.transform.scale(CHAR_IMAGES_L[avatar_left], (250, 250)) 
            screen.blit(avatar, (50,300))

            avatar = pygame.transform.scale(CHAR_IMAGES_R[avatar_right], (250, 250)) 
            screen.blit(avatar, (WIDTH-300,300))

            # --- ADD TEXT ---
            text_with_shadow(screen,"GAMECRAFT",title_font,WIDTH//2,80,WHITE)
            text_with_shadow(screen,f"{player1} VS {player2}",button_font,WIDTH//2,180,YELLOW)


            # --- HOVERABLE BUTTONS ---
            hover_ttt = btn_tictactoe.collidepoint((mx,my))
            menu_button(screen,btn_tictactoe, "Tic Tac Toe",hover_ttt)

            hover_o = btn_othello.collidepoint((mx,my))
            menu_button(screen,btn_othello, "Othello",hover_o)

            hover_c4 = btn_connect4.collidepoint((mx,my))
            menu_button(screen,btn_connect4, "Connect 4",hover_c4)

            hover_back = btn_back.collidepoint((mx,my))
            menu_button(screen,btn_back, "Back",hover_back)

            
            # --- EVENT LISTENER: GAME MENU ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if hover_c4:
                        # click_sound.play()
                        print("Launching Connect 4...")
                        import connect4
                        connect4.main(screen,player1,player2,avatar_left,avatar_right)

                    elif hover_ttt:
                        # click_sound.play()
                        print("Launching Tic-Tac-Toe...")
                        import tictactoe
                        tictactoe.main(screen,player1,player2,avatar_left,avatar_right)

                    elif hover_o: 
                        print("Launching Othello")
                        import othello
                        othello.main(screen,player1,player2)

                    elif hover_back:
                        # click_sound.play()
                        current_state="START_SCREEN"

        pygame.display.update()


if __name__ == '__main__':
   p1 = sys.argv[1] if len(sys.argv)>1  else "Steve"
   p2 = sys.argv[2] if len(sys.argv)>2 else "Alex"
   main_hub(p1,p2)