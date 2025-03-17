#!/usr/bin/env bash

ANSIBLE_PATH=/home/octopus/ansible
ANSIBLE_CONTROL_NODE_URL='https://github.com/OOHehir/ansible_rpi.git'

first_boot_setup () {
    # Apt update and install git
    apt update
    apt install git python3-pip -y

    # Install pip and ansible
    python3 -m pip install --user ansible-core

    # Clone the ansible repository
    # cd $ANSIBLE_PATH
    # git clone $ANSIBLE_CONTROL_NODE_URL

    # If successful, create a file to indicate that the first boot setup has been completed
    mkdir -p $ANSIBLE_PATH
    echo $(date) > $ANSIBLE_PATH/ansible-first-boot.log
}

update_and_run_ansible () {
    # Pull latest changes from the git repository
    # cd $ANSIBLE_PATH/ansible_rpi
    # Probably need to change this to a curl from a server
    # git pull

    # A little artificial but use eventually use this to update & run
    #/usr/bin/ansible-pull -U https://github.com/OOHehir/ansible_rpi.git -d /home/octopus/ansible --diff playbook.yml
    /usr/bin/ansible-pull -U https://github.com/OOHehir/ansible_rpi.git -d /home/octopus/ansible --diff playbook.yml
    # ansible-pull -U $ANSIBLE_PATH/ansible_rpi -C main playbook.yml

    # log the operation, continue if file doesn't exist
    rm $ANSIBLE_PATH/ansible.log || true
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