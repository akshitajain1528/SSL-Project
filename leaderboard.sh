# #!/bin/bash 
# # doesnt work if there are spaces in the names of the users, NVM IT DOES I GUESS
# declare -A arr
# i=0

# while IFS=$'\t' read -r a b; do
# arr[$i]=$a 
# ((i++))
# done < users.tsv

# declare -A winner
# declare -A points
# p=0


# for(( k=0; k<i; k++ )); do
#     points[$k]=0
# done

# if [ "$1" == "tictactoe" ]; then
#     winner[$p]="$(python3 tictactoe.py)"
#     # takes care of spaces now
#     for(( j=0; j<i; j++ )); do
#         if [ "${arr[$j]}" == "${winner[$p]}" ]; then
#             points[$j]=$((points[$j]+5))
#         fi
#     done
#     ((p++))
# fi

# if [ "$1" == "connect4" ]; then
#     winner[$p]="$(python3 connect4.py)"
#     for(( j=0; j<i; j++ )); do
#         if [ "${arr[$j]}" == "${winner[$p]}" ]; then
#             points[$j]=$((points[$j]+5))
#         fi
#     done
#     ((p++))
# fi

# if [ "$1" == "othello" ]; then
#     winner[$p]="$(python3 othello.py)"
#     for(( j=0; j<i; j++ )); do
#         if [ "${arr[$j]}" == "${winner[$p]}" ]; then
#             points[$j]=$((points[$j]+5))
#         fi
#     done
#     ((p++))
# fi

# # echo > points.csv
# # for(( k=0; k<i; k++ )); do
# #     echo "${arr[$k]},${points[$k]}" >> points.csv
# # done

# declare -A array
# l=0
# while IFS=, read -r c d; do
# array["$l,0"]=$c
# array["$l,1"]=$d
# ((l++))
# done < leaderboard.csv

# for(( k=0; k<i; k++ )); do
#     found=0
#     for(( j=0; j<l; j++ )); do
#         if [ "${arr[$k]}" == "${array["$j,0"]}" ]; then
#             found=1
#             array["$j,1"]=$((${array["$j,1"]}+${points[$k]}))
#         fi
#     done
#     if [ $found -eq 0 ]; then
#         array["$l,0"]="${arr[$k]}"
#         array["$l,1"]="${points[$k]}"
#         ((l++))
#     fi
# done


# echo > leaderboard.csv
# for(( k=0; k<l; k++ )); do
#     echo "${array["$k,0"]},${array["$k,1"]}" >> leaderboard.csv
# done

# touch sorted_leaderboard.csv
# sort -t, -k2 -nr leaderboard.csv > sorted_leaderboard.csv
# mv sorted_leaderboard.csv leaderboard.csv



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


