#!/usr/bin/env bash

ANSIBLE_BIN_PATH=/home/octopus/.local/bin
ANSIBLE_CONTROL_NODE_URL='https://github.com/OOHehir/ansible_rpi.git'
PATH=$PATH:/home/octopus/.local/bin

first_boot_setup () {
    # Apt update and install git
    apt update
    echo "Installing git, python3-pip"
    apt install git python3-pip -y

    # Install ansible for user octopus
    echo "Installing ansible"
    sudo -H -u octopus python3 -m pip install --user ansible

    # Setup Ansible requirements
    echo "Installing Ansible requirements"
    sudo -H -u octopus $ANSIBLE_BIN_PATH/ansible-galaxy collection install -r $HOME/ansible_rpi/requirements.yml

    # If successful, create a file to indicate that the first boot setup has been completed
    mkdir -p $HOME
    echo $(date) > $HOME/ansible-first-boot.log
}

update_and_run_ansible () {
    #/usr/bin/ansible-pull -U https://github.com/OOHehir/ansible_rpi.git -d /home/octopus/ansible --diff playbook.yml
    $ANSIBLE_BIN_PATH/ansible-pull -U https://github.com/OOHehir/ansible_rpi.git -d $HOME/ansible --diff playbook.yml
    # ansible-pull -U $HOME/ansible_rpi -C main playbook.yml

    # log the operation, continue if file doesn't exist
    rm $HOME/ansible.log || true
    echo $(date) > $HOME/ansible.log
}

# Check if the script is running as root
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

# Check if this is the first boot
if [ -f $HOME_PATH/ansible-first-boot.log ]; then
  echo "This is not the first boot"
else
  echo "This is the first boot"
  first_boot_setup
fi

update_and_run_ansible