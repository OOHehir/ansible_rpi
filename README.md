# Ansible Playbook for Raspberry Pi

## Purpose
This Ansible playbook is designed to setup a Raspberry Pi with the following:
- Docker
- Docker Compose
- Git
- Python3
- Pip3
- Ansible
- GivTCP

## Required files on fresh system
ansible.cfg
ansible-script.sh
requirements.yml

All other files are pulled in by script & Ansible.

## How to copy files to remote system
```bash
scp -r ansible.cfg ansible-script.sh requirements.yml octopus@octopuspi.local:/home/octopus/
```

## How to run
```bash
./ansible-script.sh
```

## GivTC
Should be available on address: http://octopuspi.local:8099/config.html
