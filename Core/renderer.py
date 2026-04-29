import pygame
import os
import math
from Core.configuration import *
import sys

# --- FONTS ---
font_modern = os.path.join(ASSETS,'font_modern.otf')
font_minecrafter = os.path.join(ASSETS,'minecrafter.ttf')
font_pixel_purl = os.path.join(ASSETS,'pixel_purl.ttf')

# --- FONT STYLES ---
title_font = pygame.font.Font(font_minecrafter,80)
button_font = pygame.font.Font(font_modern,36)
small_font = pygame.font.Font(font_modern,24)
medium_font = pygame.font.Font(font_modern,36)
title_modern_font = pygame.font.Font(font_modern,80)

# --- ASSET LOADING ---


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

pink_block = pygame.image.load(os.path.join(ASSETS,'spritepink.png')).convert_alpha()
PINK_BLOCK_SPRITE = pygame.transform.scale(pink_block,(120,70))

black_block = pygame.image.load(os.path.join(ASSETS,'spriteblack.png')).convert_alpha()
BLACK_BLOCK_SPRITE = pygame.transform.scale(black_block,(120,70))

# ========================
#     GHOST VERSIONS 
# ========================

# --- CONNECT 4 ---
P1_GHOST = P1_SPRITE.copy()
P1_GHOST.set_alpha(180)
P2_GHOST = P2_SPRITE.copy()
P2_GHOST.set_alpha(180)

# --- TIC TAC TOE / OTHELLO ---
SWORD_GHOST = SWORD_SPRTIE.copy()
SWORD_GHOST.set_alpha(160)
APPLE_GHOST = APPLE_SPRITE.copy()
APPLE_GHOST.set_alpha(160) 
PINK_BLOCK_SPRITE_GHOST = PINK_BLOCK_SPRITE.copy()
PINK_BLOCK_SPRITE_GHOST.set_alpha(160)
BLACK_BLOCK_SPRITE_GHOST = BLACK_BLOCK_SPRITE.copy()
BLACK_BLOCK_SPRITE_GHOST.set_alpha(160)


# ======================
#    UI ELEMENT FUXNS
# ======================

def text_with_shadow (screen,text,font,c_x,c_y,color,color_shaow=BLACK):
    """Gives shadow to a text of 4 pixel of desired color."""
    shadow = font.render(text, False, color_shaow)
    shadow_rect = shadow.get_rect(center=(c_x + 4, c_y + 4))
    screen.blit(shadow, shadow_rect)
    
    label = font.render(text, False, color)
    label_rect = label.get_rect(center=(c_x, c_y))
    screen.blit(label, label_rect)

def menu_button(screen, rect, text, is_hovering,fontstyle=button_font,):
    border_color = WHITE if is_hovering else BORDER_DARK
    text_color = YELLOW if is_hovering else WHITE
    
    overlay = pygame.Surface((rect.width, rect.height))
    overlay.set_alpha(200) 
    overlay.fill(UI_GREY)
    screen.blit(overlay, (rect.x, rect.y))
    
    pygame.draw.rect(screen, border_color, rect, width=4)

    label = fontstyle.render(text, False, text_color)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

def image_button(screen, rect, image, is_hovering):
    if is_hovering:
        border_color = WHITE
        pygame.draw.rect(screen, border_color, rect, width=4)


    # --- RESIZE IMAGE TO FIT BUTTON ---
    img = pygame.transform.scale(image, (rect.width - 10, rect.height - 10))
    img_rect = img.get_rect(center=rect.center)
    screen.blit(img, img_rect)

def wireframe_box(screen,rect,text=""):
    pygame.draw.rect(screen,WHITE,rect,width=3,border_radius=10)
    if text:
        label = small_font.render(text,False,WHITE)
        screen.blit(label, label.get_rect(center=rect.center))


def connect4_frame(screen,game,player1,player2,avatar_left,avatar_right,bg_img,anim_state,win_data,is_league=False):
    is_anim,anim_col,anim_y,anim_player = anim_state
    winner,win_color,win_avatar = win_data

    mx,my = pygame.mouse.get_pos()

    screen.blit(bg_img,(0,0))
    overlay = pygame.Surface((BOARD_WIDTH_C4+40,BOARD_HEIGHT_C4+40),pygame.SRCALPHA)
    overlay.fill((0,0,0))
    overlay.set_alpha(70)
    screen.blit(overlay,(X_OFFSET_C4-20,Y_OFFSET_C4-20))

    # --- CHARACTERS ---
    rect_left = pygame.Rect(50,150,200,50)
    rect_right = pygame.Rect(WIDTH-250,150,200,50)
    wireframe_box(screen, rect_left, "AVATAR")
    wireframe_box(screen, rect_right, "AVATAR")
    
    avatar = pygame.transform.scale(CHAR_IMAGES_L[avatar_left], (200, 200)) 
    screen.blit(avatar, (50,300))
    avatar = pygame.transform.scale(CHAR_IMAGES_R[avatar_right], (200, 200)) 
    screen.blit(avatar, (WIDTH-250,300))

    # --- BACK BUTTON ---

    # menu_button(screen, back_button, "BACK",back_hovering ,fontstyle=button_font,)
    

    # --- TEXT ---
    text_with_shadow(screen,'CONNECT 4',title_font,WIDTH//2,50,WHITE)

    if not game.game_over:
        if game.player == 1:
            text_with_shadow(screen,f"{player1}'s Turn",pygame.font.Font(font_pixel_purl,44),WIDTH//2,110,BLUE_RGBA,BLACK)
        else:
            text_with_shadow(screen,f"{player2}'s Turn",pygame.font.Font(font_pixel_purl,44),WIDTH//2,110,RED_RGBA,BLACK)

    if not is_anim and not game.game_over and (X_OFFSET_C4 <= mx <= X_OFFSET_C4 + BOARD_WIDTH_C4) and (Y_OFFSET_C4 <= my <= Y_OFFSET_C4 + BOARD_HEIGHT_C4):
        hover_col = int((mx-X_OFFSET_C4)//SQUARESIZE_C4)
        hover_row = int((my-Y_OFFSET_C4)//SQUARESIZE_C4)
        sprite_x = X_OFFSET_C4 + (hover_col*SQUARESIZE_C4) + 3
        sprite_y = Y_OFFSET_C4 + (hover_row*SQUARESIZE_C4)
        ghost = P1_GHOST if game.player ==1 else P2_GHOST
        screen.blit(ghost,(sprite_x, sprite_y))

    if is_anim: 
        sprite_x = X_OFFSET_C4 + (anim_col*SQUARESIZE_C4) + 5
        active_sprite = P1_SPRITE if anim_player == 1 else P2_SPRITE
        screen.blit(active_sprite, (sprite_x,anim_y+5))

    grid_layer = pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
    for r in range(ROWS_C4):
        for c in range(COLUMNS_C4):
            x = X_OFFSET_C4 + (c * SQUARESIZE_C4)
            y = Y_OFFSET_C4 + (r * SQUARESIZE_C4)
            
            piece = game.board[r, c]
            if piece == 1:
                screen.blit(P1_SPRITE, (x + 3, y))
            elif piece == -1:
                screen.blit(P2_SPRITE, (x+3, y))

            pygame.draw.rect(grid_layer,(0,0,0,150),(x,y,SQUARESIZE_C4,SQUARESIZE_C4),2)

    screen.blit(grid_layer,(0,0))
    
    if game.game_over:
        if is_league:
            banner = pygame.Surface((WIDTH, 150))
            banner.set_alpha(220)
            banner.fill(BLACK)
            screen.blit(banner, (0, HEIGHT//2 - 75))

            if winner == player1:
                text_with_shadow(screen, f"{winner} WINS!", medium_font, WIDTH//2+200, HEIGHT//2 - 20, win_color)
                avatar = pygame.transform.scale(CHAR_IMAGES_L[win_avatar], (450,450)) 
                screen.blit(avatar, (50,200))

            elif winner == player2:
                text_with_shadow(screen, f"{winner} WINS!", medium_font, WIDTH//2-200, HEIGHT//2 - 20, win_color)
                # text_with_shadow(screen, "Press ESC to return to Hub", medium_font, WIDTH//2-200, HEIGHT//2 + 40, WHITE)
                avatar = pygame.transform.scale(CHAR_IMAGES_R[win_avatar], (450,450)) 
                screen.blit(avatar, (WIDTH-490,200))
            
            elif winner == "Tie":
                text_with_shadow(screen, f"It's a Tie", medium_font, WIDTH//2, HEIGHT//2 - 20, win_color)
                # text_with_shadow(screen, "Press ESC to return to Hub", medium_font, WIDTH//2, HEIGHT//2 + 40, WHITE)

           
            btn_text = "SHOW RESULTS" if "othello" in sys.modules[__name__].__file__ else "NEXT GAME"
            btn_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT - 100, 300, 50)
            hover = btn_rect.collidepoint((mx, my))
            menu_button(screen, btn_rect, btn_text, hover, small_font)
            
        else:
            banner = pygame.Surface((WIDTH, 150))
            banner.set_alpha(220)
            banner.fill(BLACK)
            screen.blit(banner, (0, HEIGHT//2 - 75))
        
            if winner == player1:
                text_with_shadow(screen, f"{winner} WINS!", medium_font, WIDTH//2+200, HEIGHT//2 - 20, win_color)
                text_with_shadow(screen, "Press ESC to return to Hub", medium_font, WIDTH//2+210, HEIGHT//2 + 40, WHITE)
                avatar = pygame.transform.scale(CHAR_IMAGES_L[win_avatar], (450,450)) 
                screen.blit(avatar, (50,200))

            elif winner == player2:
                text_with_shadow(screen, f"{winner} WINS!", medium_font, WIDTH//2-200, HEIGHT//2 - 20, win_color)
                text_with_shadow(screen, "Press ESC to return to Hub", medium_font, WIDTH//2-200, HEIGHT//2 + 40, WHITE)
                avatar = pygame.transform.scale(CHAR_IMAGES_R[win_avatar], (450,450)) 
                screen.blit(avatar, (WIDTH-490,200))
            
            elif winner == "Tie":
                text_with_shadow(screen, f"It's a Tie", medium_font, WIDTH//2, HEIGHT//2 - 20, win_color)
                text_with_shadow(screen, "Press ESC to return to Hub", medium_font, WIDTH//2, HEIGHT//2 + 40, WHITE)


def ttt_frame(screen,game,background,player1,player2,avatar_left,avatar_right,winner,win_color,win_avatar,is_league=False):

    # --- BACKGROUND ---
    screen.blit(background,(0,0))
    board = pygame.Surface((SQUARESIZE_TTT*COLS_TTT+50,SQUARESIZE_TTT*ROWS_TTT+50),pygame.SRCALPHA)
    board.fill(C_YELLOW)
    board.set_alpha(140)
    screen.blit(board,(X_OFFSET_TTT-25,Y_OFFSET_TTT+30))

    # --- CHARACTERS ---
    rect_left = pygame.Rect(50,150,200,50)
    rect_right = pygame.Rect(WIDTH-250,150,200,50)
    wireframe_box(screen, rect_left, "AVATAR")
    wireframe_box(screen, rect_right, "AVATAR")
    
    avatar = pygame.transform.scale(CHAR_IMAGES_L[avatar_left], (200, 200)) 
    screen.blit(avatar, (50,300))
    avatar = pygame.transform.scale(CHAR_IMAGES_R[avatar_right], (200, 200)) 
    screen.blit(avatar, (WIDTH-250,300))


    # --- TEXT ---
    text_with_shadow(screen,"TIC TAC TOE",title_font,WIDTH//2,50,WHITE)

    if not game.game_over:
        if game.player == 1:
            text_with_shadow(screen,f"{player1}'s Turn",pygame.font.Font(font_pixel_purl,44),WIDTH//2,105,BLUE_RGBA,BLACK)
        else:
            text_with_shadow(screen,f"{player2}'s Turn",pygame.font.Font(font_pixel_purl,44),WIDTH//2,105,YELLOW,BLACK)

    mx,my = pygame.mouse.get_pos()
    hover_col = int((mx-X_OFFSET_TTT)//SQUARESIZE_TTT)
    hover_row = int((my-Y_OFFSET_TTT-55)//SQUARESIZE_TTT)
    if not game.game_over and (0<=hover_row<=9) and (0<=hover_col<=9):

        sprite_x = X_OFFSET_TTT + (hover_col*SQUARESIZE_TTT) + 5
        sprite_y = Y_OFFSET_TTT + (hover_row*SQUARESIZE_TTT) + 60
        ghost = SWORD_GHOST if game.player == 1 else APPLE_GHOST
        if not game.board[hover_row,hover_col]:
            screen.blit(ghost,(sprite_x, sprite_y))

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

            pygame.draw.rect(grid_layer,(166, 41, 0),(x,y,SQUARESIZE_TTT,SQUARESIZE_TTT),2)
    
    screen.blit(grid_layer,(0,0))

    if game.game_over and game.win_anim_progress==1:
        if is_league:
            banner = pygame.Surface((WIDTH, 150))
            banner.set_alpha(220)
            banner.fill(BLACK)
            screen.blit(banner, (0, HEIGHT//2 - 75))

            if winner == player1:
                text_with_shadow(screen, f"{winner} WINS!", medium_font, WIDTH//2+200, HEIGHT//2 - 20, win_color)
                avatar = pygame.transform.scale(CHAR_IMAGES_L[win_avatar], (450,450)) 
                screen.blit(avatar, (50,200))

            elif winner == player2:
                text_with_shadow(screen, f"{winner} WINS!", medium_font, WIDTH//2-200, HEIGHT//2 - 20, win_color)
                # text_with_shadow(screen, "Press ESC to return to Hub", medium_font, WIDTH//2-200, HEIGHT//2 + 40, WHITE)
                avatar = pygame.transform.scale(CHAR_IMAGES_R[win_avatar], (450,450)) 
                screen.blit(avatar, (WIDTH-490,200))
            
            elif winner == "Tie":
                text_with_shadow(screen, f"It's a Tie", medium_font, WIDTH//2, HEIGHT//2 - 20, win_color)
                # text_with_shadow(screen, "Press ESC to return to Hub", medium_font, WIDTH//2, HEIGHT//2 + 40, WHITE)

           
            btn_text = "SHOW RESULTS" if "othello" in sys.modules[__name__].__file__ else "NEXT GAME"
            btn_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT - 100, 300, 50)
            hover = btn_rect.collidepoint((mx, my))
            menu_button(screen, btn_rect, btn_text, hover, small_font)

        else:
            banner = pygame.Surface((WIDTH, 150))
            banner.set_alpha(220)
            banner.fill(BLACK)
            screen.blit(banner, (0, HEIGHT//2 - 75))
        
            if winner == player1:
                text_with_shadow(screen, f"{winner} WINS!", medium_font, WIDTH//2+200, HEIGHT//2 - 20, win_color)
                text_with_shadow(screen, "Press ESC to return to Hub", medium_font, WIDTH//2+210, HEIGHT//2 + 40, WHITE)
                avatar = pygame.transform.scale(CHAR_IMAGES_L[win_avatar], (450,450)) 
                screen.blit(avatar, (50,200))

            elif winner == player2:
                text_with_shadow(screen, f"{winner} WINS!", medium_font, WIDTH//2-200, HEIGHT//2 - 20, win_color)
                text_with_shadow(screen, "Press ESC to return to Hub", medium_font, WIDTH//2-200, HEIGHT//2 + 40, WHITE)
                avatar = pygame.transform.scale(CHAR_IMAGES_R[win_avatar], (450,450)) 
                screen.blit(avatar, (WIDTH-490,200))
            
            elif winner == "Tie":
                text_with_shadow(screen, f"It's a Tie", medium_font, WIDTH//2, HEIGHT//2 - 20, win_color)
                text_with_shadow(screen, "Press ESC to return to Hub", medium_font, WIDTH//2, HEIGHT//2 + 40, WHITE)


    if game.game_over and game.winning_line and not game.win_anim_progress == 1:
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

def othello_frame(screen,game,background,player1,player2,avatar_left,avatar_right,winner,win_color,win_avatar,is_league):
    screen.blit(background,(0,0))
    board = pygame.Surface((SQUARESIZE_OTHELLO*COLS_OTHELLO+50,SQUARESIZE_OTHELLO*ROWS_OTHELLO+50),pygame.SRCALPHA)
    board.fill(DARK_PINK)
    board.set_alpha(50)
    screen.blit(board,(X_OFFSET_OTHELLO-25,Y_OFFSET_OTHELLO+30))


    # --- CHARACTERS ---
    rect_left = pygame.Rect(50,150,200,50)
    rect_right = pygame.Rect(WIDTH-250,150,200,50)
    wireframe_box(screen, rect_left, "AVATAR")
    wireframe_box(screen, rect_right, "AVATAR")
    
    avatar = pygame.transform.scale(CHAR_IMAGES_L[avatar_left], (200, 200)) 
    screen.blit(avatar, (50,300))
    avatar = pygame.transform.scale(CHAR_IMAGES_R[avatar_right], (200, 200)) 
    screen.blit(avatar, (WIDTH-250,300))


    # --- TEXT ---
    text_with_shadow(screen,"OTHELLO",title_font,WIDTH//2,50,WHITE)

    if not game.game_over:
        if game.player == 1:
            text_with_shadow(screen,f"{player1}'s Turn",pygame.font.Font(font_pixel_purl,44),WIDTH//2,105,(153, 153, 153))
        else:
            text_with_shadow(screen,f"{player2}'s Turn",pygame.font.Font(font_pixel_purl,44),WIDTH//2,105,(183, 49, 204))

    mx,my = pygame.mouse.get_pos()

    # --- OTHELLO HOVER OVER ONLY VALID MOVES ---
    if not game.game_over and (X_OFFSET_OTHELLO <= mx <= WIDTH - X_OFFSET_OTHELLO) and (Y_OFFSET_OTHELLO + 55 <= my <= HEIGHT - 20):
        hover_col = int((mx-X_OFFSET_OTHELLO)//SQUARESIZE_OTHELLO)
        hover_row = int((my-Y_OFFSET_OTHELLO-55)//SQUARESIZE_OTHELLO)
        
        if 0 <= hover_row < ROWS_OTHELLO and 0 <= hover_col < COLS_OTHELLO:
            
            if game.board[hover_row, hover_col] == 0:
                is_valid = False
                
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        if game.switch_possible(hover_row, hover_col, dr, dc, game.player):
                            is_valid = True
                            break 
                    if is_valid:
                        break 
                
                # ONLY DRAW THE GHOST IF THE MOVE IS LEGAL
                if is_valid:
    
                    x = X_OFFSET_OTHELLO + (hover_col * SQUARESIZE_OTHELLO)
                    y = Y_OFFSET_OTHELLO + (hover_row * SQUARESIZE_OTHELLO) + 55
                    
                    ghost = PINK_BLOCK_SPRITE_GHOST if game.player == 1 else BLACK_BLOCK_SPRITE_GHOST
                    screen.blit(ghost, (x - 25, y))
    
    # --- BOARD ---

    grid_layer = pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
    for r in range(ROWS_OTHELLO):
        for c in range(COLS_OTHELLO):
            x = X_OFFSET_OTHELLO + (c * SQUARESIZE_OTHELLO)
            y = Y_OFFSET_OTHELLO + (r * SQUARESIZE_OTHELLO) + 55

            piece = game.board[r,c]
            if piece == 1:
                screen.blit(PINK_BLOCK_SPRITE,(x-25,y))
            elif piece == -1:
                screen.blit(BLACK_BLOCK_SPRITE,(x-25,y))

            pygame.draw.rect(grid_layer,DARK_PINK,(x,y,SQUARESIZE_OTHELLO,SQUARESIZE_OTHELLO),2)
    
    screen.blit(grid_layer,(0,0))

    if game.game_over:
        if is_league:
            banner = pygame.Surface((WIDTH, 150))
            banner.set_alpha(220)
            banner.fill(BLACK)
            screen.blit(banner, (0, HEIGHT//2 - 75))

            if winner == player1:
                text_with_shadow(screen, f"{winner} WINS!", medium_font, WIDTH//2+200, HEIGHT//2 - 20, win_color)
                # avatar = pygame.transform.scale(CHAR_IMAGES_L[win_avatar], (450,450)) 
                # screen.blit(avatar, (50,200))

            elif winner == player2:
                text_with_shadow(screen, f"{winner} WINS!", medium_font, WIDTH//2-200, HEIGHT//2 - 20, win_color)
                # text_with_shadow(screen, "Press ESC to return to Hub", medium_font, WIDTH//2-200, HEIGHT//2 + 40, WHITE)
                # avatar = pygame.transform.scale(CHAR_IMAGES_R[win_avatar], (450,450)) 
                # screen.blit(avatar, (WIDTH-490,200))
            
            elif winner == "Tie":
                text_with_shadow(screen, f"It's a Tie", medium_font, WIDTH//2, HEIGHT//2 - 20, win_color)
                # text_with_shadow(screen, "Press ESC to return to Hub", medium_font, WIDTH//2, HEIGHT//2 + 40, WHITE)

           
            btn_text = "SHOW RESULTS"
            btn_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT - 100, 300, 50)
            hover = btn_rect.collidepoint((mx, my))
            menu_button(screen, btn_rect, btn_text, hover, small_font)
            
        else:
            banner = pygame.Surface((WIDTH, 150))
            banner.set_alpha(220)
            banner.fill(BLACK)
            screen.blit(banner, (0, HEIGHT//2 - 75))
        
            if winner == player1:
                text_with_shadow(screen, f"{winner} WINS!", medium_font, WIDTH//2+200, HEIGHT//2 - 20, win_color)
                text_with_shadow(screen, "Press ESC to return to Hub", medium_font, WIDTH//2+210, HEIGHT//2 + 40, WHITE)
                avatar = pygame.transform.scale(CHAR_IMAGES_L[win_avatar], (450,450)) 
                screen.blit(avatar, (50,200))

            elif winner == player2:
                text_with_shadow(screen, f"{winner} WINS!", medium_font, WIDTH//2-200, HEIGHT//2 - 20, win_color)
                text_with_shadow(screen, "Press ESC to return to Hub", medium_font, WIDTH//2-200, HEIGHT//2 + 40, WHITE)
                avatar = pygame.transform.scale(CHAR_IMAGES_R[win_avatar], (450,450)) 
                screen.blit(avatar, (WIDTH-490,200))
            
            elif winner == "Tie":
                text_with_shadow(screen, f"It's a Tie", medium_font, WIDTH//2, HEIGHT//2 - 20, win_color)
                text_with_shadow(screen, "Press ESC to return to Hub", medium_font, WIDTH//2, HEIGHT//2 + 40, WHITE)
