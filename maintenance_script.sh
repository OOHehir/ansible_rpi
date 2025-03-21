#!/usr/bin/env bash
OCTOPUS_HOME=/home/octopus
ANSIBLE_BIN_PATH=/home/octopus/.venv/bin
ANSIBLE_CONTROL_NODE_URL='https://github.com/OOHehir/ansible_rpi.git'
PATH=$PATH:/home/octopus/.local/bin

check_result () {
    if [ $? -eq 0 ]; then
        echo "Success"
    else
        echo "Failed"
        exit 1
    fi
}

first_boot_setup () {
    echo "Updating"
    apt update
    check_result

    echo "Installing git, python3-pip"
    apt install git python3-full python3-pip -y
    check_result

    echo "Checking for venv for octopus user"
    # check if .venv directory exists, if not create it
    if [ ! -d "$OCTOPUS_HOME/.venv" ]; then
        echo "Creating venv for octopus user"
        python3 -m venv $OCTOPUS_HOME/.venv
        check_result
    fi

    # Activate venv and install Ansible
    echo "Activating venv and installing Ansible"
    source $OCTOPUS_HOME/.venv/bin/activate
    check_result
    echo "Installing Ansible"
    pip install ansible
    check_result

    # Setup Ansible requirements
    echo "Installing Ansible requirements"
    sudo -H -u octopus $ANSIBLE_BIN_PATH/ansible-galaxy collection install -r $OCTOPUS_HOME/requirements.yml
    check_result

    # If successful, create a file to indicate that the first boot setup has been completed
    mkdir -p $OCTOPUS_HOME
    echo $(date) > $OCTOPUS_HOME/ansible-first-boot.log
}

update_and_run_ansible () {
    $ANSIBLE_BIN_PATH/ansible-pull -U https://github.com/OOHehir/ansible_rpi.git -d $OCTOPUS_HOME/ansible --diff playbook.yml
    # ansible-pull -U $OCTOPUS_HOME/ansible_rpi -C main playbook.yml
    check_result

    # log the operation, continue if file doesn't exist
    rm $OCTOPUS_HOME/ansible.log || true
    echo $(date) > $OCTOPUS_HOME/ansible.log
}

# Check if this is running already (i.e called via service)
if pidof -x "$0" -o $$ >/dev/null; then
    echo "Already running, exiting"
    exit 1
fi

# Check if the script is running as root
if [ "$EUID" -ne 0 ]
    then echo "Please run as root"
    exit
fi

# Check if this is the first boot
if [ -f $OCTOPUS_HOME/ansible-first-boot.log ]; then
  echo "This is not the first boot"
else
  echo "This is the first boot"
  first_boot_setup
fi

update_and_run_ansible