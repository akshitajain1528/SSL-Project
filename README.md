# SSL-Project
SSL Project on Mini-game hub (Topic-2) created  by Akshita Jain (25B0999) and Maulik Jain (25B1002).
### Part 1: Systems, Security & Analytics 
*(Focus: Bash, Subprocessing, and Data Parsing)*

* **Phase 1: Infrastructure & Security (Bash)**
    * [cite_start]Initialize the repository with the required directory structure (`hub/`, `games/`)[cite: 13, 14, 18].
    * [cite_start]Develop `main.sh` to handle the terminal-based authentication loop[cite: 25].
    * [cite_start]Implement SHA-256 hashing using `sha256sum` to securely store and verify passwords in `users.tsv`[cite: 27, 28].
    * [cite_start]Engineer the secure handoff to execute `python3 game.py <username1> <username2>`[cite: 31, 32].
* **Phase 4: Data Logging & Visual Analytics**
    * [cite_start]Configure `game.py` to continuously append match outcomes (Winner, Loser, Date, Game) to `history.csv`[cite: 66].
    * [cite_start]Write `leaderboard.sh` to parse the CSV and output a formatted, sortable terminal table of player statistics[cite: 68].
    * [cite_start]Integrate Matplotlib to generate a Top 5 Players bar chart and a Most Played Games pie chart upon exiting the game menu[cite: 71, 72, 73].