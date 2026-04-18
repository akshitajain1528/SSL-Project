import numpy as np
import pygame
import sys
import os

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
    



# --- MINECRAFT COLORS ---
DIRT_BROWN = (134, 96, 67)
GRASS_GREEN = (89, 166, 34)
STONE_GREY = (125, 125, 125)
OBSIDIAN_BLACK = (20, 18, 32)
WHITE = (255, 255, 255)
MC_YELLOW = (255, 255, 85)
UI_GREY = (168, 168, 168)
BORDER_DARK = (85, 85, 85)



# --- Initialising pygame ---
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Minecraft Game Hub")


ASSETS = 'Assets_MC'

# --- Load the BG ---
bg_path = os.path.join(ASSETS,'minecraft_bg.png')
bg_img = pygame.image.load(bg_path).convert()
GAME_BG = pygame.transform.scale(bg_img,(WIDTH,HEIGHT))



# --- FONT ---
font_path = os.path.join(ASSETS,'font.otf')
title_font = pygame.font.Font(font_path,80)
button_font = pygame.font.Font(font_path,36)
small_font = pygame.font.Font(font_path,24)



# --- SOUND EFFECTS ---
click_path = os.path.join(ASSETS,'click.mp3')
click_sound = pygame.mixer.Sound(click_path)


# ======================
#    UI ELEMENT FUXNS
# ======================

def text_with_shadow (screen,text,font,c_x,c_y,color):

    # --- Shadow (Black, offset 4 pixels) ---
    shadow = font.render(text, False, (0, 0, 0))
    shadow_rect = shadow.get_rect(center=(c_x + 4, c_y + 4))
    screen.blit(shadow, shadow_rect)
    
    # --- Main Text ---
    label = font.render(text, False, color)
    label_rect = label.get_rect(center=(c_x, c_y))
    screen.blit(label, label_rect)


def menu_button(screen, rect, text, is_hovering):
    """Draws a multi-layered Minecraft menu button over the background artwork."""
    
    # --- Dynamic Hover Colors (Dark border standard, White border hover) ---
    border_color = WHITE if is_hovering else BORDER_DARK
    text_color = MC_YELLOW if is_hovering else WHITE
    
    # --- Draw base UI grey block (slightly transparent for cool overlay effect) ---
    overlay = pygame.Surface((rect.width, rect.height))
    overlay.set_alpha(200) # (0-255 opacity) let the background bleed through slightly
    overlay.fill(UI_GREY)
    screen.blit(overlay, (rect.x, rect.y))
    
    # --- Draw accurate Minecraft 3D Border ---
    # (Optional highlight line at top/left, shadow line at bottom/right)
    pygame.draw.rect(screen, border_color, rect, width=4)

    # --- Render Text ---
    label = button_font.render(text, False, text_color)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)


def wireframe_box(screen,rect,text=""):
    pygame.draw.rect(screen,WHITE,rect,width=3,border_radius=10)

    if text:
        label = small_font.render(text,False,WHITE)
        screen.blit(label, label.get_rect(center=rect.center))



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


    # --- WIREBOXES AROUND IT ---
    box_character_left = pygame.Rect(50,150,200,50)
    box_character_right = pygame.Rect(WIDTH-250,150,200,50)
    box_left_panel = pygame.Rect(50,250,200,400)
    box_right_panel = pygame.Rect(WIDTH-250,250,200,400)


    # --- BUTTON RECTANGLES: GAME MENU ---
    btn_tictactoe = pygame.Rect(WIDTH//2 - 200, 300, 400, 60)
    btn_othello = pygame.Rect(WIDTH//2 - 200, 400, 400, 60)
    btn_connect4 = pygame.Rect(WIDTH//2 - 200, 500, 400, 60)
    btn_back = pygame.Rect(WIDTH//2 - 200, 650, 400, 60)

    while run:
        screen.blit(GAME_BG,(0,0))

        mx,my = pygame.mouse.get_pos()

        # ===================================
        #      FRIST PAGE: START SCREEN
        # ===================================

        if current_state=="START_SCREEN":

            # --- WELCOME TO GAMECRAFT ---
            text_with_shadow(screen,'WELCOME TO',title_font,WIDTH//2,80,WHITE)
            text_with_shadow(screen,"GAMECRAFT",title_font,WIDTH//2,200,WHITE)
            text_with_shadow(screen,f"{player1}",button_font,WIDTH//2-450,80,MC_YELLOW)
            text_with_shadow(screen,f"{player2}",button_font,WIDTH//2+450,80,MC_YELLOW)

            # --- HOVERABLE BUTTONS ---
            h_menu = btn_start_game_menu.collidepoint((mx,my))
            menu_button(screen,btn_start_game_menu,"GAME MENU",h_menu)

            h_play = btn_start_how_to.collidepoint((mx,my))
            menu_button(screen,btn_start_how_to,"HOW TO PLAY",h_play)

            h_leaderboard = btn_start_leaderboard.collidepoint((mx,my))
            menu_button(screen,btn_start_leaderboard,"LEADERBOARD", h_leaderboard)

            h_quit = btn_start_quit.collidepoint((mx,my))
            menu_button(screen,btn_start_quit,"QUIT",h_quit)




            # --- SKETCH BOXES ---
            wireframe_box(screen,box_character_left,"CHARACTER")
            wireframe_box(screen,box_character_right,"CHARACTER")
            wireframe_box(screen,box_left_panel)
            wireframe_box(screen,box_right_panel)


            # --- EVENT LISTENERS: START PAGE ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run=False
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if h_menu:
                        current_state="GAME_MENU"

                    elif h_play:
                        print("HOW TO PLAY")
                        current_state="HOWTOPLAY"

                    elif h_leaderboard:
                        current_state="LEADERBOARD"
                        print('LEADERBOARD')

                    elif h_quit:
                        pygame.quit()
                        sys.exit()


        # ====================================
        #        2ND PAGE: GAME MENU
        # ====================================

        elif current_state=="GAME_MENU":

            # --- ADD TEXT ---
            text_with_shadow(screen,"GAMECRAFT",title_font,WIDTH//2,80,WHITE)
            text_with_shadow(screen,f"{player1} VS {player2}",button_font,WIDTH//2,180,MC_YELLOW)


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
                        connect4.main(screen,player1,player2)

                    elif hover_ttt:
                        # click_sound.play()
                        print("Launching Tic-Tac-Toe...")

                    elif hover_o: 
                        print("Launching Othello")
                    elif hover_back:
                        # click_sound.play()
                        current_state="START_SCREEN"

        pygame.display.update()


if __name__ == '__main__':
   p1 = sys.argv[1] if len(sys.argv)>1  else "Steve"
   p2 = sys.argv[2] if len(sys.argv)>2 else "Alex"
   main_hub(p1,p2)