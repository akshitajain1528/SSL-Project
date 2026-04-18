import numpy as np
import pygame
import sys
import os

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


# --- Load the BG ---
ASSETS = 'Assets_MC'

bg_path = os.path.join(ASSETS,'minecraft_bg.png')
bg_img = pygame.image.load(bg_path).convert()
GAME_BG = pygame.transform.scale(bg_img,(WIDTH,HEIGHT))

# --- FONT ---
font_path = os.path.join(ASSETS,'font.otf')
title_font = pygame.font.Font(font_path,80)
button_font = pygame.font.Font(font_path,36)

# --- SOUND EFFECTS ---
click_path = os.path.join(ASSETS,'click.mp3')
click_sound = pygame.mixer.Sound(click_path)


# --- UI ELEMENT FUXNS ---

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


# --- Main loop aage ---

def main_menu(player1="Steve",player2="Alex"):
    run = True

    # --- Game and Quit buttons ---
    btn_tictactoe = pygame.Rect(WIDTH//2 - 200, 300, 400, 60)
    btn_othello = pygame.Rect(WIDTH//2 - 200, 400, 400, 60)
    btn_connect4 = pygame.Rect(WIDTH//2 - 200, 500, 400, 60)
    # Re-using the Emergency Meeting idea for standard Quit
    btn_quit = pygame.Rect(WIDTH//2 - 200, 650, 400, 60)

    while run:
        screen.blit(GAME_BG,(0,0))

        # --- Add text ---
        text_with_shadow(screen,"GAMECRAFT",title_font,WIDTH//2,80,WHITE)
        text_with_shadow(screen,f"{player1} VS {player2}",button_font,WIDTH//2,180,MC_YELLOW)

        # --- Tracking mouse for animations
        mx,my = pygame.mouse.get_pos()
        hover_ttt = btn_tictactoe.collidepoint((mx,my))
        hover_o = btn_othello.collidepoint((mx,my))
        hover_c4 = btn_connect4.collidepoint((mx,my))
        hover_quit = btn_quit.collidepoint((mx,my))

        # --- Interaction when hovered over ---
        menu_button(screen,btn_tictactoe, "Tic Tac Toe",hover_ttt)
        menu_button(screen,btn_othello, "Othello",hover_o)
        menu_button(screen,btn_connect4, "Connect 4",hover_c4)
        menu_button(screen,btn_quit, "Quit",hover_quit)

        # --- EVENT LISTENER ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if hover_c4:
                    # click_sound.play()
                    print("Launching Connect 4...")
                elif hover_ttt:
                    # click_sound.play()
                    print("Launching Tic-Tac-Toe...")
                elif hover_quit:
                    # click_sound.play()
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


if __name__ == '__main__':
    p1 = sys.argv[1]
    p2 = sys.argv[2]
    main_menu(p1,p2)