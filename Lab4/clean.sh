#!/bin/bash

if [ $(whoami) != 'root' ]; then
    echo "Must be root to run $0"
    exit 1;
fi

users=("larry" "moe" "curly")
admins=("ken" "dmr" "bwk")

# Delete the users.
for user in "${users[@]}"; do
    echo "Removing user $user"

    # Remove the user.
    userdel $user && rm -rf /home/$user
done

# Delete the admins.
for admin in "${admins[@]}"; do
    echo "Removing admin $admin"

    # Remove the admin.
    userdel $admin && rm -rf /admins/$admin
done

echo "Cleaning the groups"

# Remove the groups.
groupdel emp
groupdel wheel

echo "Removing directories"

# Delete the admins directory.
rm -rf /admins
