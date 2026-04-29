#!/bin/bash

cat << "EOF"
   _____          __  __ ______ _____ _____            ______ _______ 
  / ____|   /\   |  \/  |  ____/ ____|  __ \     /\   |  ____|__   __|
 | |  __   /  \  | \  / | |__ | |    | |__) |   /  \  | |__     | |   
 | | |_ | / /\ \ | |\/| |  __|| |    |  _  /   / /\ \ |  __|    | |   
 | |__| |/ ____ \| |  | | |___| |____| | \ \  / ____ \| |       | |   
  \_____/_/    \_\_|  |_|______\_____|_|  \_\/_/    \_\_|       |_| 

 __          ________ _      _____ ____  __  __ ______  _____ 
 \ \        / /  ____| |    / ____/ __ \|  \/  |  ____|/ ____|
  \ \  /\  / /| |__  | |   | |   | |  | | \  / | |__  | (___  
   \ \/  \/ / |  __| | |   | |   | |  | | |\/| |  __|  \___ \ 
    \  /\  /  | |____| |___| |___| |__| | |  | | |____ ____) |
     \/  \/   |______|______\_____\____/|_|  |_|______|_____/ 
                                                              
                 __     ______  _    _ 
                 \ \   / / __ \| |  | |
                  \ \_/ / |  | | |  | |
                   \   /| |  | | |  | |
                    | | | |__| | |__| |
                    |_|  \____/ \____/               
                                                                      
EOF

FILE="users.tsv"

if [[ ! -f "$FILE" ]]; then
touch "$FILE"
fi 

# --Helper function--
hash_password() {
    echo -n "$1" | sha256sum | awk '{print $1}'
}

# --Authentication function--

authenticate_user() {
    echo -en "$1, "
while true; do
    read -p "Enter your username: " USER_NAME

    if grep -q -P "^${USER_NAME}\t" ${FILE}; then

            # --Comparing entered and stored hashes.--
        STORED_HASH=$(grep -P "^${USER_NAME}\t" "${FILE}"| awk '{print $2}')

        while true; do

        read -s -p "Enter your password: " PASSWORD
        ENTERED_HASH=$(hash_password ${PASSWORD})

        if [[ "${STORED_HASH}" == "${ENTERED_HASH}" ]];then
            echo -e "\n\e[32mLogin successful\e[0m"
            break 2
            else
            echo -e "\n\e[31mPassword did not match. Retry...\e[0m"
        fi
        done


            # --Username not found, register or not.
    else

        while true; do
        read -p "Username not found, do you want to register? (Y/N)" binary

        if [[ ${binary} == "Y" || ${binary}  == "y" ]]; then
        read -s -p "Create your password: " PASSWORD
        ENTERED_HASH=$(hash_password ${PASSWORD})
        echo -e "${USER_NAME}\t${ENTERED_HASH}" >> $FILE
        echo -e "\n\e[32mRegistration successful.\e[0m"

        break 2

        elif [[ ${binary} == "N" || ${binary} == "n" ]]; then
        echo -n "Returning back. "
        break
        else
        echo -e "\e[31mUnknown input. Please input Y for YES or N for NO.\e[0m"
        fi
        done

    fi
done
    CURR_AUTH_USER=${USER_NAME}

}

# --First authentication

authenticate_user "Player 1"
PLAYER1=${CURR_AUTH_USER}

# --Second authentication, also checking if player 1 and 2 are same.
while true; do
authenticate_user "Player 2"
PLAYER2=${CURR_AUTH_USER}
if [[ ${PLAYER1} == ${PLAYER2} ]]; then
    echo -e "\e[31mBoth players cannot be the same. Please use a different account.\e[0m"
else
    break
fi
done


# --- PYTHON ---
python3 main_hub.py ${PLAYER1} ${PLAYER2}