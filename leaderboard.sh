#!/bin/bash 
# doesnt work if there are spaces in the names of the users, NVM IT DOES I GUESS
declare -A arr
i=0

while IFS=$'\t' read -r a b; do
arr[$i]=$a 
((i++))
done < users.tsv

declare -A winner
declare -A points
p=0


for(( k=0; k<i; k++ )); do
    points[$k]=0
done

if [ "$1" == "tictactoe" ]; then
    winner[$p]="$(python3 tictactoe.py)"
    # tajes care of spaces now
    for(( j=0; j<i; j++ )); do
        if [ "${arr[$j]}" == "${winner[$p]}" ]; then
            points[$j]=$((points[$j]+5))
        fi
    done
    ((p++))
fi

if [ "$1" == "connect4" ]; then
    winner[$p]="$(python3 connect4.py)"
    for(( j=0; j<i; j++ )); do
        if [ "${arr[$j]}" == "${winner[$p]}" ]; then
            points[$j]=$((points[$j]+5))
        fi
    done
    ((p++))
fi

if [ "$1" == "othello" ]; then
    winner[$p]="$(python3 othello.py)"
    for(( j=0; j<i; j++ )); do
        if [ "${arr[$j]}" == "${winner[$p]}" ]; then
            points[$j]=$((points[$j]+5))
        fi
    done
    ((p++))
fi

# echo > points.csv
# for(( k=0; k<i; k++ )); do
#     echo "${arr[$k]},${points[$k]}" >> points.csv
# done

declare -A array
l=0
while IFS=, read -r c d; do
array["$l,0"]=$c
array["$l,1"]=$d
((l++))
done < leaderboard.csv

for(( k=0; k<i; k++ )); do
    found=0
    for(( j=0; j<l; j++ )); do
        if [ "${arr[$k]}" == "${array["$j,0"]}" ]; then
            found=1
            array["$j,1"]=$((${array["$j,1"]}+${points[$k]}))
        fi
    done
    if [ $found -eq 0 ]; then
        array["$l,0"]="${arr[$k]}"
        array["$l,1"]="${points[$k]}"
        ((l++))
    fi
done


echo > leaderboard.csv
for(( k=0; k<l; k++ )); do
    echo "${array["$k,0"]},${array["$k,1"]}" >> leaderboard.csv
done

touch sorted_leaderboard.csv
sort -t, -k2 -nr leaderboard.csv > sorted_leaderboard.csv
mv sorted_leaderboard.csv leaderboard.csv

