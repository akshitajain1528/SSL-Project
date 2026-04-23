import pygame
import os
import math
from configuration import *



# --- FONTS ---
font_modern = os.path.join(ASSETS,'font_modern.otf')
font_minecrafter = os.path.join(ASSETS,'minecrafter.ttf')
font_pixel_purl = os.path.join(ASSETS,'pixel_purl.ttf')


# --- FONT STYLES ---
title_font = pygame.font.Font(font_minecrafter,80)
button_font = pygame.font.Font(font_modern,36)
small_font = pygame.font.Font(font_modern,24)
medium_font = pygame.font.Font(font_modern,36)


# --- BACKGROUND ---
# c4_bg_path = os.path.join(ASSETS,'connect4_bg.jpeg')
# c4_bg_img = pygame.image.load(c4_bg_path).convert()
# c4_GAME_BG = pygame.transform.scale(c4_bg_img,(WIDTH,HEIGHT))


# --- ASSET LOADING ---
zombie_img = pygame.image.load(os.path.join(ASSETS, "zombie.png")).convert_alpha()
pig_img = pygame.image.load(os.path.join(ASSETS, "pig.png")).convert_alpha()
dog_img = pygame.image.load(os.path.join(ASSETS, "dog.png")).convert_alpha()
steve_img = pygame.image.load(os.path.join(ASSETS, "steve.png")).convert_alpha()


p1_img = pygame.image.load(os.path.join(ASSETS,'diamond.png')).convert_alpha()
P1_SPRITE = pygame.transform.scale(p1_img,(90,90))

p2_img = pygame.image.load(os.path.join(ASSETS,'emerald.png')).convert_alpha()
P2_SPRITE = pygame.transform.scale(p2_img,(90,90))

sword = pygame.image.load(os.path.join(ASSETS,'diamond_sword.png')).convert_alpha()
SWORD_SPRTIE = pygame.transform.scale(sword,(50,50))

apple = pygame.image.load(os.path.join(ASSETS,'golden_apple.png')).convert_alpha()
APPLE_SPRITE = pygame.transform.scale(apple,(50,50))

redstone = pygame.image.load(os.path.join(ASSETS,'redstone.png')).convert_alpha()
REDSTONE_SPRITE = pygame.transform.scale(redstone,(20,20))

# ========================
#     GHOST VERSIONS 
# ========================

# --- CONNECT 4 ---
P1_GHOST = P1_SPRITE.copy()
P1_GHOST.set_alpha(180)
P2_GHOST = P2_SPRITE.copy()
P2_GHOST.set_alpha(180)

# --- TIC TAC TOE ---
SWORD_GHOST = SWORD_SPRTIE.copy()
SWORD_GHOST.set_alpha(160)
APPLE_GHOST = APPLE_SPRITE.copy()
APPLE_GHOST.set_alpha(160) 



# ======================
#    UI ELEMENT FUXNS
# ======================


def text_with_shadow (screen,text,font,c_x,c_y,color,color_shaow=BLACK):
    """Gives shadow to a text of 4 pixel of desired color."""

    # --- Shadow (Black, offset 4 pixels) ---
    shadow = font.render(text, False, color_shaow)
    shadow_rect = shadow.get_rect(center=(c_x + 4, c_y + 4))
    screen.blit(shadow, shadow_rect)
    
    # --- Main Text ---
    label = font.render(text, False, color)
    label_rect = label.get_rect(center=(c_x, c_y))
    screen.blit(label, label_rect)


def menu_button(screen, rect, text, is_hovering,fontstyle=button_font,):
    """Draws a multi-layered Minecraft menu button over the background artwork."""
    
    # --- Dynamic Hover Colors (Dark border standard, White border hover) ---
    border_color = WHITE if is_hovering else BORDER_DARK
    text_color = YELLOW if is_hovering else WHITE
    
    # --- Draw base UI grey block (slightly transparent for cool overlay effect) ---
    overlay = pygame.Surface((rect.width, rect.height))
    overlay.set_alpha(200) # (0-255 opacity) let the background bleed through slightly
    overlay.fill(UI_GREY)
    screen.blit(overlay, (rect.x, rect.y))
    
    # --- Draw accurate Minecraft 3D Border ---
    pygame.draw.rect(screen, border_color, rect, width=4)

    # --- Render Text ---
    label = fontstyle.render(text, False, text_color)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)


def image_button(screen, rect, image, is_hovering):
    """Draws an image-based button inside a UI rectangle."""

    # --- Dynamic Hover Border ---
    if is_hovering:
        border_color = WHITE
        pygame.draw.rect(screen, border_color, rect, width=4)

    # --- Draw base UI grey block ---
    # overlay = pygame.Surface((rect.width, rect.height))
    # overlay.set_alpha(200)
    # overlay.fill(UI_GREY)
    # screen.blit(overlay, (rect.x, rect.y))
    

    # --- Resize image to fit button ---
    img = pygame.transform.scale(image, (rect.width - 10, rect.height - 10))

    # --- Center image inside rect ---
    img_rect = img.get_rect(center=rect.center)
    screen.blit(img, img_rect)
   


def wireframe_box(screen,rect,text=""):
    pygame.draw.rect(screen,WHITE,rect,width=3,border_radius=10)

    if text:
        label = small_font.render(text,False,WHITE)
        screen.blit(label, label.get_rect(center=rect.center))


def connect4_frame(screen,game,player1,player2,bg_img,anim_state,win_data):
    is_anim,anim_col,anim_y,anim_player = anim_state
    winner,win_color = win_data

    mx,my = pygame.mouse.get_pos()


    # --- BG AND THE DIMMING BOX ---
    screen.blit(bg_img,(0,0))
    overlay = pygame.Surface((BOARD_WIDTH_C4+40,BOARD_HEIGHT_C4+40),pygame.SRCALPHA)
    overlay.fill((0,0,0))
    overlay.set_alpha(70)
    screen.blit(overlay,(X_OFFSET_C4-20,Y_OFFSET_C4-20))


    # --- TEXT ---
    text_with_shadow(screen,'CONNECT 4',title_font,WIDTH//2,50,WHITE)

    if not game.game_over:
        if game.player == 1:
            text_with_shadow(screen,f"{player1}'s Turn",pygame.font.Font(font_pixel_purl,44),WIDTH//2,110,BLUE_RGBA,BLACK)
        else:
            text_with_shadow(screen,f"{player2}'s Turn",pygame.font.Font(font_pixel_purl,44),WIDTH//2,110,RED_RGBA,BLACK)

    # --- DYNAMIC RENDERING ---
    if not is_anim and not game.game_over and (X_OFFSET_C4 <= mx <= X_OFFSET_C4 + BOARD_WIDTH_C4) and (Y_OFFSET_C4 <= my <= Y_OFFSET_C4 + BOARD_HEIGHT_C4):
        hover_col = int((mx-X_OFFSET_C4)//SQUARESIZE_C4)
        hover_row = int((my-Y_OFFSET_C4)//SQUARESIZE_C4)
        sprite_x = X_OFFSET_C4 + (hover_col*SQUARESIZE_C4) + 5
        sprite_y = Y_OFFSET_C4 + (hover_row*SQUARESIZE_C4) + 5
        ghost = P1_GHOST if game.player ==1 else P2_GHOST
        screen.blit(ghost,(sprite_x, sprite_y))

    if is_anim: 
        sprite_x = X_OFFSET_C4 + (anim_col*SQUARESIZE_C4) + 5
        active_sprite = P1_SPRITE if anim_player == 1 else P2_SPRITE
        screen.blit(active_sprite, (sprite_x,anim_y+5))

    # --- MAKING THE GRID ---
    grid_layer = pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)

    for r in range(ROWS_C4):
        for c in range(COLUMNS_C4):
            x = X_OFFSET_C4 + (c * SQUARESIZE_C4)
            y = Y_OFFSET_C4 + (r * SQUARESIZE_C4)
            
            # Static pieces
            piece = game.board[r, c]
            if piece == 1:
                screen.blit(P1_SPRITE, (x + 5, y +5))
            elif piece == -1:
                screen.blit(P2_SPRITE, (x + 5, y + 5))

            pygame.draw.rect(grid_layer,(0,0,0,150),(x,y,SQUARESIZE_C4,SQUARESIZE_C4),3)
            # pygame.draw.circle(grid_layer,BORDER_RGBA,(x+50,y+50),40)

    screen.blit(grid_layer,(0,0))

    if game.game_over:
        banner = pygame.Surface((WIDTH, 150))
        banner.set_alpha(220)
        banner.fill(BLACK)
        screen.blit(banner, (0, HEIGHT//2 - 75))
    
        text_with_shadow(screen, f"{winner} WINS!", medium_font, WIDTH//2, HEIGHT//2 - 20, win_color)
        text_with_shadow(screen, "Press ESC to return to Hub", medium_font, WIDTH//2, HEIGHT//2 + 40, WHITE)

    pygame.display.update()


def ttt_frame(screen,game,background,player1,player2,winner,win_color):

    # --- BACKGROUND ---
    screen.blit(background,(0,0))
    board = pygame.Surface((SQUARESIZE_TTT*COLS_TTT+50,SQUARESIZE_TTT*ROWS_TTT+50),pygame.SRCALPHA)
    board.fill(C_YELLOW)
    board.set_alpha(50)
    screen.blit(board,(X_OFFSET_TTT-25,Y_OFFSET_TTT+30))

    # --- TEXT ---
    text_with_shadow(screen,"TIC TAC TOE",title_font,WIDTH//2,50,WHITE)

    if not game.game_over:
        if game.player == 1:
            text_with_shadow(screen,f"{player1}'s Turn",pygame.font.Font(font_pixel_purl,44),WIDTH//2,105,BLUE_RGBA,BLACK)
        else:
            text_with_shadow(screen,f"{player2}'s Turn",pygame.font.Font(font_pixel_purl,44),WIDTH//2,105,YELLOW,BLACK)

    mx,my = pygame.mouse.get_pos()
    if not game.game_over and (X_OFFSET_TTT <= mx <= WIDTH - X_OFFSET_TTT) and (Y_OFFSET_TTT + 55 <= my <= HEIGHT - 20):
        hover_col = int((mx-X_OFFSET_TTT)//SQUARESIZE_TTT)
        hover_row = int((my-Y_OFFSET_TTT-55)//SQUARESIZE_TTT)
        sprite_x = X_OFFSET_TTT + (hover_col*SQUARESIZE_TTT) + 5
        sprite_y = Y_OFFSET_TTT + (hover_row*SQUARESIZE_TTT) + 60
        ghost = SWORD_GHOST if game.player == 1 else APPLE_GHOST
        if not game.board[hover_row,hover_col]:
            screen.blit(ghost,(sprite_x, sprite_y))


    # --- MAKING THE GRID ---
    grid_layer = pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)

    for r in range(ROWS_TTT):
        for c in range(COLS_TTT):
            x = X_OFFSET_TTT + (c * SQUARESIZE_TTT)
            y = Y_OFFSET_TTT + (r * SQUARESIZE_TTT) + 55

            piece = game.board[r,c]
            if piece == 1:
                screen.blit(SWORD_SPRTIE,(x+5,y+5))
            elif piece == -1:
                screen.blit(APPLE_SPRITE,(x+5,y+5))

            pygame.draw.rect(grid_layer,C_YELLOW,(x,y,SQUARESIZE_TTT,SQUARESIZE_TTT),1)
    
    screen.blit(grid_layer,(0,0))

    if game.game_over:
        banner = pygame.Surface((WIDTH, 150))
        banner.set_alpha(220)
        banner.fill(BLACK)
        screen.blit(banner, (0, HEIGHT//2 - 75))
    
        text_with_shadow(screen, f"{winner} WINS!", medium_font, WIDTH//2, HEIGHT//2 - 20, win_color)
        text_with_shadow(screen, "Press ESC to return to Hub", medium_font, WIDTH//2, HEIGHT//2 + 40, WHITE)


        if game.winning_line:
            start_pos, end_pos = game.winning_line
            
            distance = math.hypot(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
            
            # Determine how many blocky particles to draw based on current animation progress
            total_particles = int(distance / 15) # One block every 15 pixels
            current_particles = int(total_particles * game.win_anim_progress)
            
            for i in range(current_particles):
                t = i / max(1, total_particles)
                px = start_pos[0] + (end_pos[0] - start_pos[0]) * t
                py = start_pos[1] + (end_pos[1] - start_pos[1]) * t
                
                # Draw a blocky Redstone Square
                # rect = pygame.Rect(0, 0, 14, 14)
                center = (px, py)
                # pygame.draw.rect(screen, (255, 85, 85), rect) # Glowing Red center
                # pygame.draw.rect(screen, (170, 0, 0), rect, 3) # Dark Red border
                screen.blit(REDSTONE_SPRITE,center)

    pygame.display.update()
