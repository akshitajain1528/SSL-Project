
import pygame
from Games import tictactoe
from Games import connect4
from Games import othello
import os

def start_league(screen, player1, player2, avatar_left, avatar_right):
    game_sequence = [
        (tictactoe, "tictactoe"),
        (connect4, "connect4"),
        (othello, "othello")
    ]
    
    results = []

    for game_module, game_id in game_sequence:
        # 2. Run the game
        res = game_module.main(screen, player1, player2, avatar_left, avatar_right, is_league=True)
        
        # Use the actual player name or "Tie"
        results.append(res) 

        # 4. Handle the Bash/Leaderboard logic
        winner_name = "draw" if res == "Tie" else res

        if winner_name == "draw":
            os.system(f'bash leaderboard.sh update {game_id} "{player1}" "{player2}" true')
        elif winner_name:
            loser = player2 if winner_name == player1 else player1
            os.system(f'bash leaderboard.sh update {game_id} "{winner_name}" "{loser}" false')

    return results
