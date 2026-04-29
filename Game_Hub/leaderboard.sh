#!/bin/bash         


# game="$1"

# declare -A wins
# declare -A losses

# # --- loading data from history.csv --- #
# if [ -e history.csv ]; then
#     while IFS=, read -r user g w l; do
#         key="$user,$g"
#         wins["$key"]=$w
#         losses["$key"]=$l
#     done < history.csv
# fi

# # --- taking input from game --- #
# IFS=, read -r a b c <<< "$(python3 "$game.py")"

# # --- updating new data --- #
# if [ "$a" != "draw" ]; then
#     key1="$a,$game"
#     key2="$b,$game"

#     # Initialize if empty
#     if [ -z "${wins["$key1"]}" ]; then wins["$key1"]=0; losses["$key1"]=0; fi
#     if [ -z "${wins["$key2"]}" ]; then wins["$key2"]=0; losses["$key2"]=0; fi

#     wins["$key1"]=$((wins["$key1"] + 1))
#     losses["$key2"]=$((losses["$key2"] + 1))
# fi

# # --- editing history.csv --- #
# echo > history.csv

# for key in "${!wins[@]}"; do
#     IFS=',' read -r user g <<< "$key"
#     echo "$user,$g,${wins["$key"]},${losses["$key"]}" >> history.csv
# done

# # --- creating diff leaderboards --- #
# declare -A created

# for key in "${!wins[@]}"; do
#     IFS=',' read -r user g <<< "$key"

#     file="leaderboard_$g.csv"

#     if [ -z "${created["$g"]}" ]; then
#         echo "username,wins,losses,ratio" > "$file"
#         created["$g"]=1
#     fi

#     w=${wins["$key"]}
#     l=${losses["$key"]}

#     # Win/Loss Ratio logic
#     if [ "$l" -eq 0 ]; then
#         ratio="undefeatable"
#     else
#         ratio=$(echo "scale=2; $w/$l" | bc)
#     fi

#     echo "$user,$w,$l,$ratio" >> "$file"
# done

# # --- sorting the leaderboard --- #
# for g in "${!created[@]}"; do
#     file="leaderboard_$g.csv"
    
#     # Sort by Ratio (Column 4)
#     # (head -n 1 "$file" && tail -n +2 "$file" | sort -t, -k4 -nr) > temp.csv
    
#     # Sort by Wins (Column 2)
#     # (head -n 1 "$file" && tail -n +2 "$file" | sort -t, -k2 -nr) > temp.csv
    
#     # mv temp.csv "$file"
# done


#!/bin/bash

# $1 = Mode (update/display), $2 = Game, $3 = winner/sort_col, $4 = loser, $5 = is_draw
mode="$1"
game="$2"

declare -A wins
declare -A losses

# --- loading data from history.csv --- #
if [ -e history.csv ]; then
    while IFS=, read -r user g w l; do
        key="$user,$g"
        wins["$key"]=$w
        losses["$key"]=$l
    done < history.csv
fi

# ==========================================
# MODE: UPDATE (Saves data after a game)
# ==========================================
if [ "$mode" == "update" ]; then
    winner="$3"
    loser="$4"
    is_draw="$5"

    if [ "$is_draw" != "true" ]; then
        key1="$winner,$game"
        key2="$loser,$game"

        if [ -z "${wins["$key1"]}" ]; then wins["$key1"]=0; losses["$key1"]=0; fi
        if [ -z "${wins["$key2"]}" ]; then wins["$key2"]=0; losses["$key2"]=0; fi

        wins["$key1"]=$((wins["$key1"] + 1))
        losses["$key2"]=$((losses["$key2"] + 1))
    fi

    # Rewriting history.csv
    echo -n > history.csv
    for key in "${!wins[@]}"; do
        IFS=',' read -r user g <<< "$key"
        echo "$user,$g,${wins["$key"]},${losses["$key"]}" >> history.csv
    done

# ==========================================
# MODE: DISPLAY (Prints to terminal)
# ==========================================
elif [ "$mode" == "display" ]; then
    sort_col="$3" # This will be 2 (Wins), 3 (Losses), or 5 (Ratio)
    
    file="leaderboard_$game.csv"
    echo "username,wins,losses,ratio" > "$file"

    for key in "${!wins[@]}"; do
        IFS=',' read -r user g <<< "$key"
        if [ "$g" == "$game" ]; then
            w=${wins["$key"]}
            l=${losses["$key"]}

            if [ "$l" -eq 0 ]; then
                ratio=99999999
            
            else
                ratio=$(echo "scale=2; $w/$l" | bc)
            fi
            echo "$user,$w,$l,$ratio" >> "$file"
        fi
    done

cat << "EOF"
 /$$                           /$$                     /$$                                           /$$
| $$                          | $$                    | $$                                          | $$
| $$  /$$$$$$   /$$$$$$   /$$$$$$$  /$$$$$$   /$$$$$$ | $$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$$
| $$ /$$__  $$ |____  $$ /$$__  $$ /$$__  $$ /$$__  $$| $$__  $$ /$$__  $$ |____  $$ /$$__  $$ /$$__  $$
| $$| $$$$$$$$  /$$$$$$$| $$  | $$| $$$$$$$$| $$  \__/| $$  \ $$| $$  \ $$  /$$$$$$$| $$  \__/| $$  | $$
| $$| $$_____/ /$$__  $$| $$  | $$| $$_____/| $$      | $$  | $$| $$  | $$ /$$__  $$| $$      | $$  | $$
| $$|  $$$$$$$|  $$$$$$$|  $$$$$$$|  $$$$$$$| $$      | $$$$$$$/|  $$$$$$/|  $$$$$$$| $$      |  $$$$$$$
|__/ \_______/ \_______/ \_______/ \_______/|__/      |_______/  \______/  \_______/|__/       \_______/

EOF

    (head -n 1 "$file" && tail -n +2 "$file" | sort -t, -k"$sort_col" -nr) | column -t -s,
    rm "$file" 
fi