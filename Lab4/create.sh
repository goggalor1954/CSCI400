#!/bin/bash

if [ $(whoami) != 'root' ]; then
    echo "Must be root to run $0"
    exit 1;
fi

# 4.1.1

echo "Starting 4.1.1..."

echo "Create the admins directory"
mkdir -pv /admins

echo "Create the groups emp and wheel (see man groupadd)"
groupadd -g 300 emp
groupadd -g 400 wheel

# Define our users.
users=("larry" "moe" "curly")
userGroup="emp"

# Define our admins.
admins=("ken" "dmr" "bwk")
adminGroup="wheel"
adminGroupMembers=("larry bwk dmr" "curly ken bwk" "moe dmr ken")

# Add all the users.
for user in "${users[@]}"; do
    echo "Creating user $user"

    # Add the user.
    useradd -m $user -p $user

    # Add the user to the group for the users.
    usermod -aG $userGroup $user

    echo "Setting permissions for /home/$user to 750 (drwxr-x---)"
    chmod 750 /home/$user
done

# Add all the admin users.
for admin in "${admins[@]}"; do
    echo "Creating user $admin"

    # Add the admin
    useradd $admin --home-dir /admins/$admin --base-dir /admins/$admin \
        -m -p $admin

    # Add the admin to the admin group.
    usermod -aG $adminGroup $admin
done

c=0

# Now add the users into the admin's groups.
for admin in "${admins[@]}"; do
    # Loop through all the users to go into the .
    for user in ${adminGroupMembers[$c]}; do
        echo "Adding $user to $admin's group"
        usermod -a -G $admin $user
    done

    ((c++))
done

perl -i.bak -pe 's/DIR_MODE=0755/DIR_MODE=0750/' /etc/adduser.conf
perl -i.bak -pe 's/UMASK(\s*)025/UMASK$1027/' /etc/login.defs

# Now, for 11 we set the /home directory off limits to user listing. We allow
# Them to execute (as in list their own directory), but not read or write, which
# ultimately prevents them from listing what's in /home.
setfacl -m u::rwx,g::rx,o::x /home/

# Then allow the admin users to be able to list /home without sudo.
setfacl -m g:wheel:rx /home/

# For the /admins directory we do the following.
chmod -R 775 /admins

for admin in "${admins[@]}"; do
    chmod -R g+rwxs /admins/$admin
done
