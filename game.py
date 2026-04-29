import numpy as np
import pygame
import sys
import os
import matplotlib.pyplot as plt
import csv


os.environ["SDL_AUDIODRIVER"] = "dummy" 


class Game:

    def players(self):
        self.p1 = sys.argv[1] if len(sys.argv)>1  else "Steve"
        self.p2 = sys.argv[2] if len(sys.argv)>2 else "Alex"
    
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


from Core.configuration import *
from Core.renderer import *
from Core.characters import *
from Core.league import *

ASSETS = 'Assets_MC'

# --- Load the BG ---
bg_path = os.path.join(ASSETS,'minecraft_bg.png')
bg_img = pygame.image.load(bg_path).convert()
GAME_BG = pygame.transform.scale(bg_img,(WIDTH,HEIGHT))
stat_bg_path = os.path.join(ASSETS,'leaderboard_bg.jpg')
stat_bg_img = pygame.image.load(stat_bg_path).convert()
stat_bg = pygame.transform.scale(stat_bg_img,(WIDTH,HEIGHT))
is_league = False
league_bg_path = os.path.join(ASSETS,'image.png')
league_bg = pygame.image.load(league_bg_path).convert()
league_bg = pygame.transform.scale(league_bg,(WIDTH,HEIGHT))

# --- SOUND EFFECTS ---
click_path = os.path.join(ASSETS,'click.mp3')
click_sound = pygame.mixer.Sound(click_path)

# popularity_pie = None
# overall_bar = None


def update_history(game_id, winner, loser, is_draw=False):
    history = {}
    
    # 1. Load existing data
    if os.path.exists("history.csv"):
        with open("history.csv", "r") as f:
            for line in f:
                if line.strip():
                    user, g, w, l = line.strip().split(',')
                    history[f"{user},{g}"] = {"w": int(w), "l": int(l)}
    
    # 2. Update the specific players
    if not is_draw:
        win_key = f"{winner},{game_id}"
        loss_key = f"{loser},{game_id}"
        
        if win_key not in history: history[win_key] = {"w": 0, "l": 0}
        if loss_key not in history: history[loss_key] = {"w": 0, "l": 0}
        
        history[win_key]["w"] += 1
        history[loss_key]["l"] += 1

    # 3. Write it all back cumulatively!
    with open("history.csv", "w") as f:
        for key, stats in history.items():
            user, g = key.split(',')
            f.write(f"{user},{g},{stats['w']},{stats['l']}\n")


# -------GRAPH PLOTS-------



# ==========================
#       PIE CHART  
# ==========================


    
ttt=0
othello=0
c4=0


with open("history.csv", "r") as f:
    player_stats = {}
    for line in f:
        if line.strip():
            user, g, w, l = line.strip().split(',') 
            if user not in player_stats:
                player_stats[user] = {"w": 0, "l": 0}
            player_stats[user]["w"] += int(w)
            player_stats[user]["l"] += int(l)
top_players = sorted(player_stats.items(), key=lambda x: x[1]["w"], reverse=True)[:3]
players = [p[0] for p in top_players]
wins = [p[1]["w"] for p in top_players]

with open("history.csv", "r") as f:
    for line in f:
        if line.strip():
            user, g, w, l = line.strip().split(',')
            if g == "tictactoe":
                ttt += int(w) + int(l)
            elif g == "othello":
                othello += int(w) + int(l)
            elif g == "connect4":
                c4 += int(w) + int(l)

games = ["Tic Tac Toe", "Othello", "Connect 4"]
plays = [ttt, othello, c4]


def refresh_plots():
    global popularity_pie, overall_bar
    global ttt, othello, c4
    global games, plays, players, wins 

    
    plt.pie(plays, labels=games, autopct='%1.1f%%', startangle=140)
    plt.title("Game Popularity")
    plt.savefig("game_popularity.png")

    plt.savefig("game_popularity.png")
    plt.close()



    games = ["Tic Tac Toe", "Othello", "Connect 4"]
    plays = [ttt, othello, c4]
    
    plt.bar(players, wins, color=['green', 'blue', 'red'])
    plt.title("Top Players by Total Wins")
    plt.xlabel("Players")
    plt.ylabel("Wins")
    plt.savefig("top_players_overall.png")

    plt.savefig("top_players.png")
    plt.close()

    popularity_pie = pygame.image.load("game_popularity.png").convert_alpha()
    overall_bar = pygame.image.load("top_players.png").convert_alpha()

    popularity_pie = pygame.transform.scale(popularity_pie, (500, 400))
    overall_bar = pygame.transform.scale(overall_bar, (500, 400))
    pygame.display.flip()

# ==========================
#      MAIN LOOP AAGE 
# ==========================

def main_hub(player1,player2):

    results = [] 
    league_winner = None
    final_score = ""
    winner_avatar = None
    global popularity_pie, overall_bar
    run = True

    lb_selected_game = "Tic Tac Toe"
    lb_selected_sort = "Wins"
    terminal_message = ""         
    terminal_message_timer = 0

    current_state = "START_SCREEN"
    

    # --- BUTTON RECTANGLES: START SCREEN ---
    btn_start_game_menu = pygame.Rect(WIDTH//2-200,300,400,60)
    btn_start_how_to = pygame.Rect(WIDTH//2-200,400,400,60)
    btn_start_leaderboard = pygame.Rect(WIDTH//2-200,500,400,60)
    btn_start_stats = pygame.Rect(WIDTH//2-200,600,400,60)
    btn_start_quit = pygame.Rect(WIDTH//2-200,700,400,60)

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
    btn_league = pygame.Rect(WIDTH//2 - 200, 585, 400, 90)
    btn_back = pygame.Rect(WIDTH//2 - 200, 700, 400, 60)
    
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

            h_stats = btn_start_stats.collidepoint((mx,my))
            menu_button(screen, btn_start_stats, "STATISTICS", h_stats)

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

                    elif h_stats:
                        refresh_plots()
                        current_state="STATISTICS"
                        print("STATISTICS")

                    elif h_quit:
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


                        # =======================================================
                        # =======================================================
                        #                   2ND PAGE: GAME MENU
                        # =======================================================
                        # =======================================================



        elif current_state=="GAME_MENU":
                # --- CHARACTER ---
            rect_left = pygame.Rect(50,150,200,50)
            rect_right = pygame.Rect(WIDTH-250,150,200,50)
            wireframe_box(screen, rect_left, "AVATAR")
            wireframe_box(screen, rect_right, "AVATAR")


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

            hover_league = btn_league.collidepoint((mx,my))
            menu_button(screen, btn_league, "START LEAGUE", hover_league)

            hover_back = btn_back.collidepoint((mx,my))
            menu_button(screen,btn_back, "Back",hover_back)

            
            # # --- EVENT LISTENER: GAME MENU ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False


                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    # --- TIC TAC TOE ---
                    if hover_ttt:
                        from Games import tictactoe
                        res = tictactoe.main(screen, player1, player2,avatar_left,avatar_right,is_league=False)
                        if res == "draw":
                            os.system(f'bash leaderboard.sh update tictactoe "{player1}" "{player2}" true')
                        elif res:
                            loser = player2 if res == player1 else player1
                            os.system(f'bash leaderboard.sh update tictactoe "{res}" "{loser}" false')
                            refresh_plots()

                    # --- OTHELLO ---
                    elif hover_o: 
                        from Games import othello
                        res = othello.main(screen, player1, player2,avatar_left,avatar_right,is_league=False)
                        if res == "draw":
                            os.system(f'bash leaderboard.sh update othello "{player1}" "{player2}" true')
                        elif res:
                            loser = player2 if res == player1 else player1
                            os.system(f'bash leaderboard.sh update othello "{res}" "{loser}" false')
                            refresh_plots()

                    # --- CONNECT 4 ---
                    elif hover_c4:
                        from Games import connect4
                        res = connect4.main(screen, player1, player2,avatar_left,avatar_right,is_league=False)
                        if res == "draw":
                            os.system(f'bash leaderboard.sh update connect4 "{player1}" "{player2}" true')
                        elif res:
                            loser = player2 if res == player1 else player1
                            os.system(f'bash leaderboard.sh update connect4 "{res}" "{loser}" false')
                            refresh_plots()

                    elif hover_league:
                        current_state = "LEAGUE"
                        is_league = True

                    elif hover_back:
                        current_state = "START_SCREEN"

    # ====================================
    #        2ND PAGE: STATISTICS
    # ====================================
        
        elif current_state=="STATISTICS":
            screen.blit(stat_bg,(0,0))

            text_with_shadow(screen,"STATISTICS",title_font,WIDTH//2,80,WHITE)

            btn_stat_back = pygame.Rect(WIDTH//2 - 200, 700, 400, 60)
            hover_stat_back = btn_stat_back.collidepoint((mx,my))
            menu_button(screen,btn_stat_back,"Back",hover_stat_back)

            screen.blit(popularity_pie, (WIDTH//2 - 500, 150))
            screen.blit(overall_bar, (WIDTH//2 , 150))
            # screen.blit(resized_ttt_bar, (WIDTH//2 - 250, 400))
            # screen.blit(resized_othello_bar, (WIDTH//2 + 250, 400))
            # screen.blit(resized_c4_bar, (WIDTH//2 + 250, 150)) 

            pygame.display.flip()  


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run=False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if hover_stat_back:
                        current_state="START_SCREEN"

    # ====================================
    #        2ND PAGE: LEADERBOARD
    # ====================================


        elif current_state=="LEADERBOARD":

            l_bg = os.path.join(ASSETS,'download (1).jpg')
            l_bg_image = pygame.image.load(l_bg).convert()
            leaderboard_bg = pygame.transform.scale(l_bg_image,(WIDTH,HEIGHT))
            screen.blit(leaderboard_bg,(0,0))

            text_with_shadow(screen,"LEADERBOARD",title_font,WIDTH//2,60,WHITE)

            # --- ROW 1: GAME SELECTION ---
            btn_lb_ttt = pygame.Rect(WIDTH//2 - 500, 150, 320, 60)
            btn_lb_o   = pygame.Rect(WIDTH//2 - 160, 150, 320, 60)
            btn_lb_c4  = pygame.Rect(WIDTH//2 + 180, 150, 320, 60)
            
            # --- ROW 2: SORTING METHOD ---
            btn_sort_wins  = pygame.Rect(WIDTH//2 - 500, 240, 320, 60)
            btn_sort_loss  = pygame.Rect(WIDTH//2 - 160, 240, 320, 60)
            btn_sort_ratio = pygame.Rect(WIDTH//2 + 180, 240, 320, 60)

            # --- ROW 3: DISPLAY BUTTON (Right below the 6 options) ---
            btn_lb_display = pygame.Rect(WIDTH//2 - 250, 350, 500, 60)

            # --- BACK BUTTON ---
            btn_lbback = pygame.Rect(WIDTH//2 - 200, 700, 400, 60)

            # --- HOVER STATES ---
            hover_lb_ttt = btn_lb_ttt.collidepoint((mx, my))
            hover_lb_o   = btn_lb_o.collidepoint((mx, my))
            hover_lb_c4  = btn_lb_c4.collidepoint((mx, my))
            
            hover_sort_wins  = btn_sort_wins.collidepoint((mx, my))
            hover_sort_loss  = btn_sort_loss.collidepoint((mx, my))
            hover_sort_ratio = btn_sort_ratio.collidepoint((mx, my))
            
            hover_lb_display = btn_lb_display.collidepoint((mx, my))
            hover_back = btn_lbback.collidepoint((mx,my))

            # --- DRAW BUTTONS ---
            menu_button(screen, btn_lb_ttt, "Tic Tac Toe", hover_lb_ttt or lb_selected_game == "Tic Tac Toe")
            menu_button(screen, btn_lb_o, "Othello", hover_lb_o or lb_selected_game == "Othello")
            menu_button(screen, btn_lb_c4, "Connect 4", hover_lb_c4 or lb_selected_game == "Connect 4")

            menu_button(screen, btn_sort_wins, "Total Wins", hover_sort_wins or lb_selected_sort == "Wins")
            menu_button(screen, btn_sort_loss, "Total Losses", hover_sort_loss or lb_selected_sort == "Losses")
            menu_button(screen, btn_sort_ratio, "W/L Ratio", hover_sort_ratio or lb_selected_sort == "W/L Ratio")
            menu_button(screen, btn_lb_display, "DISPLAY LEADERBOARD", hover_lb_display)
        

            menu_button(screen, btn_lbback, "Back", hover_back)
            # The LEADERBOARD Back button
            menu_button(screen, btn_lbback, "Back", hover_back)

            # --- DRAW TERMINAL SUCCESS MESSAGE ---
            if terminal_message:
                if pygame.time.get_ticks() - terminal_message_timer < 3000:
                    text_with_shadow(screen, terminal_message, small_font, WIDTH//2, 600, OBSIDIAN_BLACK)
                else:
                    terminal_message = ""

            # --- EVENT LISTENER: LEADERBOARD ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if hover_back:
                        current_state = "START_SCREEN"
                    
                    # Selection Logic
                    elif hover_lb_ttt:
                        lb_selected_game = "Tic Tac Toe"
                    elif hover_lb_o:
                        lb_selected_game = "Othello"
                    elif hover_lb_c4:
                        lb_selected_game = "Connect 4"
                        
                    elif hover_sort_wins:
                        lb_selected_sort = "Wins"
                    elif hover_sort_loss:
                        lb_selected_sort = "Losses"
                    elif hover_sort_ratio:
                        lb_selected_sort = "W/L Ratio"

                    # elif hover_lb_display:
                        # print(f"Loading {lb_selected_game} stats, sorted by {lb_selected_sort}!")

                    elif hover_lb_display:
                        game_map = {"Tic Tac Toe": "tictactoe", "Othello": "othello", "Connect 4": "connect4"}
                        # Wins = col 2, Losses = col 3, Ratio = col 5
                        sort_map = {"Wins": 2, "Losses": 3, "W/L Ratio": 5}
    
                        g_id = game_map[lb_selected_game]
                        col = sort_map[lb_selected_sort]
    
                        os.system(f'bash leaderboard.sh display {g_id} {col}')

                        # screen message
                        terminal_message = "Leaderboard displayed on terminal!"
                        terminal_message_timer = pygame.time.get_ticks()

        # ====================================
        #            LEAGUE PAGE
        # ====================================
        elif current_state == "LEAGUE":
            screen.blit(league_bg, (0, 0))
            text_with_shadow(screen, "LEAGUE", title_font, WIDTH//2, 80, WHITE)

            btn_start_league = pygame.Rect(WIDTH//2 - 200, 550, 400, 110)
            hover_start_league = btn_start_league.collidepoint((mx, my))
            menu_button(screen, btn_start_league, "START", hover_start_league)

            btn_stat_back = pygame.Rect(WIDTH//2 - 200, 700, 400, 60)
            hover_stat_back = btn_stat_back.collidepoint((mx, my))
            menu_button(screen, btn_stat_back, "Back", hover_stat_back)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if hover_stat_back:
                        current_state = "START_SCREEN"
                    elif hover_start_league:
                        from Core import league
                        # Store result in 'league_results'
                        league_results = league.start_league(screen, player1, player2, avatar_left, avatar_right)

                        # --- CALCULATE LEAGUE WINNER ---
                        p1_wins = league_results.count(player1)
                        p2_wins = league_results.count(player2)
                        
                        if p1_wins > p2_wins:
                            league_winner = player1
                        elif p2_wins > p1_wins:
                            league_winner = player2
                        else:
                            league_winner = "Draw"
                            
                        final_score = f"{p1_wins} - {p2_wins}"
                        
                        # Update plots in background
                        refresh_plots()
                        
                        current_state = "LEAGUE_CHAMPION_SCREEN"

        # ====================================
        #       LEAGUE CHAMPION SCREEN
        # ====================================
        elif current_state == "LEAGUE_CHAMPION_SCREEN":
            screen.blit(stat_bg, (0, 0)) 
            
            text_with_shadow(screen, "LEAGUE RESULTS", title_font, WIDTH//2, 80, WHITE)
            text_with_shadow(screen, f"FINAL SCORE: {final_score}", button_font, WIDTH//2, 180, YELLOW)

            if league_winner == "Draw":
                text_with_shadow(screen, "IT'S A TIE!", title_font, WIDTH//2, HEIGHT//2, WHITE)
            else:
                text_with_shadow(screen, f"{league_winner} IS THE", title_font, WIDTH//2, 300, BLACK)
                text_with_shadow(screen, "LEAGUE CHAMPION!", title_font, WIDTH//2, 400, BLACK)

            btn_finish = pygame.Rect(WIDTH//2 - 150, 700, 300, 60)
            h_finish = btn_finish.collidepoint(pygame.mouse.get_pos())
            menu_button(screen, btn_finish, "BACK TO HUB", h_finish)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN and h_finish:
                    current_state = "START_SCREEN"

    
        pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.players()
    p1, p2 = game.p1, game.p2
    main_hub(p1,p2)