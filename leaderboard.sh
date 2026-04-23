#!/bin/bash

game="$1"

declare -A wins
declare -A losses
declare -A draws

# --- loading data from history.csv --- #
if [ -e history.csv ]; then
    while IFS=, read -r user g w l d; do
        key="$user,$g"
        wins["$key"]=$w
        losses["$key"]=$l
        draws["$key"]=$d
    done < history.csv
fi

# --- taking input from game --- #
IFS=, read -r a b c <<< "$(python3 "$game.py")"

# --- updating new data --- #
if [ "$a" = "draw" ]; then
    key1="$b,$game"
    key2="$c,$game"

    if [ -z "${wins["$key1"]}" ]; then wins["$key1"]=0; losses["$key1"]=0; draws["$key1"]=0; fi
    if [ -z "${wins["$key2"]}" ]; then wins["$key2"]=0; losses["$key2"]=0; draws["$key2"]=0; fi

    draws["$key1"]=$((draws["$key1"] + 1))
    draws["$key2"]=$((draws["$key2"] + 1))

else
    key1="$a,$game"
    key2="$b,$game"

    # -z checks if the variable is empty, if it is empty then we initialize diff variables the array values 
    if [ -z "${wins["$key1"]}" ]; then wins["$key1"]=0; losses["$key1"]=0; draws["$key1"]=0; fi
    if [ -z "${wins["$key2"]}" ]; then wins["$key2"]=0; losses["$key2"]=0; draws["$key2"]=0; fi

    wins["$key1"]=$((wins["$key1"] + 1))
    losses["$key2"]=$((losses["$key2"] + 1))
fi

# --- editing history.csv --- #
echo > history.csv

for key in "${!wins[@]}"; do
# !{!wins[@]} is an expression that refers to all keys in the wins array 
    IFS=',' read -r user g <<< "$key"
    # we can read from anything, here key is not a file, just indices of an array but we can read from it

    echo "$user,$g,${wins["$key"]},${losses["$key"]},${draws["$key"]}" >> history.csv
done

# --- creating diff leaderboards --- #
declare -A created

for key in "${!wins[@]}"; do
    IFS=',' read -r user g <<< "$key"

    file="leaderboard_$g.csv"

    if [ -z "${created["$g"]}" ]; then
        echo "username,wins,losses,draws,ratio" > "$file"
        created["$g"]=1
    fi

    w=${wins["$key"]}
    l=${losses["$key"]}
    d=${draws["$key"]}

    total=$((w + l + d))

    if [ "$total" -eq 0 ]; then
    # == for string comparison in bash while -eq for numeric comparison 
        ratio=0
    else
        ratio=$(echo "scale=2; $w/$total" | bc) #decimal places 
    fi

    echo "$user,$w,$l,$d,$ratio" >> "$file"
done

# --- sorting the leaderboard --- #
for g in "${!done[@]}"; do
    file="leaderboard_$g.csv"
    # first row with titles neglected and using tail +2 second row onwards sorted
    # sorting by ratio
    # (head -n 1 "$file" && (tail -n +2 "$file" | sort -t, -k5 -nr)) > temp.csv
    # sorting by wins
    # (head -n 1 "$file" && (tail -n +2 "$file" | sort -t, -k2 -nr)) > temp.csv
    # sorting by losses 
    # (head -n 1 "$file" && (tail -n +2 "$file" | sort -t, -k5 -nr)) > temp.csv
    mv temp.csv "$file"
done


