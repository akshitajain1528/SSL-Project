import pygame
from renderer import wireframe_box,image_button,menu_button
from configuration import *



def draw_chr_panels(screen,mx,my,buttons_left,buttons_right,left_panel_data,right_panel_data):

    """buttons_left and buttons_right are boolean variables, which are true when to display."""
    """Whereas, left_panel_data and right_panel_data are dictionaries containing info of the panel(bada rectangle) and other smaller rectangles for character images. See in game.py"""

    if buttons_left:
        wireframe_box(screen,left_panel_data['panel'])
        for name,rect in left_panel_data['characters'].items():
            is_hovering = rect.collidepoint((mx,my))
            image_button(screen,rect,CHAR_IMAGES_L[name],is_hovering)
    
    if buttons_right:
        wireframe_box(screen,right_panel_data['panel'])
        for name,rect in right_panel_data['characters'].items():
            is_hovering = rect.collidepoint((mx,my))
            image_button(screen,rect,CHAR_IMAGES_R[name],is_hovering)


def draw_selected_characters(screen, avatar_left, avatar_right, mx, my, small_font):
    """avatar_left and avatar_right are the selected characters when we clicked on them."""

    rect_left = pygame.Rect(50,150,200,50)
    rect_right = pygame.Rect(WIDTH-250,150,200,50)

    wireframe_box(screen, rect_left, "AVATAR")
    wireframe_box(screen, rect_right, "AVATAR")
    
    # --- LEFT PLAYER ---
    if avatar_left: 

        img = CHAR_IMAGES_L[avatar_left]
        big_img = pygame.transform.scale(img, (250, 250)) 
        screen.blit(big_img, (50,300))


        reselect_button_l = pygame.Rect(rect_left.x, rect_left.bottom + 20, rect_left.width+70, 45)
        h_res_l = reselect_button_l.collidepoint((mx, my))
        menu_button(screen, reselect_button_l, "SELECT ANOTHER", h_res_l, small_font)



    # --- RIGHT PLAYER ---
    if avatar_right:
        img = CHAR_IMAGES_R[avatar_right]
        big_img = pygame.transform.scale(img, (250, 250))
        screen.blit(big_img, (WIDTH-300,300))


        reselect_btn_r = pygame.Rect(rect_right.x-70, rect_right.bottom + 20, rect_right.width+70, 45)
        h_res_r = reselect_btn_r.collidepoint((mx, my))
        menu_button(screen, reselect_btn_r, "SELECT ANOTHER", h_res_r, small_font)