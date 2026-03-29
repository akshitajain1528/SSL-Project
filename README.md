# SSL-Project
**SSL Project on Mini-game hub (Topic-2) created  by Akshita Jain (25B0999) and Maulik Jain (25B1002).**

## Overview
We plan to develop a secure, multi-user game hub that combines Bash scripting for user authentication with Python (Pygame) for gameplay. In our system, two verified players will log in, choose a game from a menu, and interact through a graphical interface. We will also implement a persistent leaderboard to store and track player's results over time.
<br>

## Key Features
### System Architecture & Authentication
The application flow is strictly controlled starting from a single Bash entry point.
1. **Authentication (`main.sh`):** Prompts for two distinct usernames and passwords. Passwords are never stored in plaintext; they are hashed using SHA-256 (`sha256sum`) and verified against `users.tsv`.
2. **Registration:** If a user does not exist, the system securely registers them into the database.
3. **Execution:** Upon successful dual-login, the Bash script passes the authenticated usernames as command-line arguments to the Python engine.
<br>


### Games
 Each game inherits from the base class and strictly utilizes NumPy array operations (e.g., slicing) to evaluate game states without manual iteration loops
1. **Tic-Tac-Toe:**
*  Played on a 10×10 board; players need 5 marks in a row to win
*  The winning line can be horizontal, vertical, or diagonal
*  Players alternate placing X or O in any empty cell

2. **Othello:**
* Played on an 8×8 board, starting with two Black and two White discs in the centre
* A move is valid only if it traps one or more opponent discs in a straight line between the newly placed disc and an existing own disc
* All trapped discs are flipped to the current player’s colour; multiple lines can be flipped in one move
* If a player has no valid moves, their turn is skipped
* The player with more discs of their colour when no valid moves remain wins

3. **Connect Four:**
* Played on a vertical 7×7 grid; coins fall to the lowest empty row in a column
* Players take turns dropping one coin into any column
* A player wins by getting 4 of their coins in a row (horizontal, vertical, or diagonal)
* The game ends in a draw if the board fills with no winner
<br>

### Analytics & Leaderboard
Post-match data is heavily tracked for player insights:
* **Logging:** `game.py` appends every match result (Winner, Loser, Date, Game) to `history.csv`.
* **Leaderboard (`leaderboard.sh`):** A Bash script parses the CSV to display a formatted terminal table showing wins, losses, and W/L ratios, sortable by user preference.
* **Visualizations:** The system utilizes Matplotlib to generate graphical insights, such as bar charts for top players and pie charts for game popularity.
<br>

## System Design
* **Layer 1: Security (Bash)**
    Acts as the entry point (`main.sh`) to authenticate two players. It uses **SHA-256** to hash and verify passwords against `users.tsv` before launching the Python engine via command-line arguments.

* **Layer 2: Core Engine (Python/Pygame)**
   The central `game.py` file manages the GUI menu and a **Base Class** for turn-based gameplay. It initializes the game board as a **NumPy array** and handles player turns.

* **Layer 3: Game Modules (NumPy Logic)**
   Individual games (Tic-Tac-Toe, Othello, Connect Four) inherit from the base class in the `games/` directory. Win conditions and move validations must be checked strictly using **NumPy array slicing** rather than manual loops.

* **Layer 4: Persistence & Analytics**
  After each match, `game.py` logs results to `history.csv`. It then calls `leaderboard.sh` to display sorted terminal stats and uses **Matplotlib** to render visual charts of player performance.
<br>

## Implementation Plan
* **Phase 1: Bash Infrastructure & Security**
Our immediate priority is to build the main.sh entry point. We will implement the user registration and login flow using SHA-256 hashing (via sha256sum) to secure users.tsv. This phase concludes once we successfully pass authenticated usernames as command-line arguments to the Python engine.

* **Phase 2: Core Game Engine Architecture**
Once the Bash part is complete, we will develop the game.py base class. This class will manage the NumPy board state, player turns, and the Pygame-CE GUI.

* **Phase 3: Individual Game Logic (NumPy)**
With the engine running, we will implement Tic-Tac-Toe, Othello, and Connect Four. We will focus on using NumPy array slicing to evaluate win/draw conditions, strictly avoiding manual loops per the project constraints.

* **Phase 4: Analytics & Final Documentation**
The final phase involves logging match results to history.csv, creating the leaderboard.sh stats parser, and generating Matplotlib visualizations. We will conclude with the LaTeX report and Makefile.


