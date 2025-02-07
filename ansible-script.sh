#!/usr/bin/env bash

ANSIBLE_PATH=/home/octopus/ansible
ANSIBLE_CONTROL_NODE_URL='https://github.com/OOHehir/ansible_rpi.git'

first_boot_setup () {
    apt update
    apt install ansible-core git -y

    # Clone the ansible repository
    cd $ANSIBLE_PATH
    git clone $ANSIBLE_CONTROL_NODE_URL

    # If successful, create a file to indicate that the first boot setup has been completed
    echo $(date) > $ANSIBLE_PATH/ansible-first-boot.log
}

update_and_run_ansible () {
    # Pull latest changes from the git repository
    cd $ANSIBLE_PATH/ansible_rpi
    # Probably need to change this to a curl from a server
    git pull

    # A little artificial but use eventually use this to update & run
    ansible-pull -U $ANSIBLE_PATH/ansible_rpi -C main playbook.yml

    # log the operation
    rm $ANSIBLE_PATH/ansible.log
    echo $(date) > $ANSIBLE_PATH/ansible.log
}

# Check if the script is running as root
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

# Check if this is the first boot
if [ -f $ANSIBLE_PATH/ansible-first-boot.log ]; then
  echo "This is not the first boot"
else
  echo "This is the first boot"
  first_boot_setup
fi

update_and_run_ansible