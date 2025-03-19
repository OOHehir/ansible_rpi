# Ansible Playbook for Raspberry Pi
Sets up required packages for GivEnergy Inverter on Raspberry Pi

## Base image
```
Raspberry Pi OS (Legacy) Lite - NO DESKTOP
    Release date: October 22nd 2024
    System: 64-bit
    Kernel version: 6.1
    Debian version: 11 (bullseye)
```

Download [link](https://downloads.raspberrypi.com/raspios_oldstable_lite_arm64/images/raspios_oldstable_lite_arm64-2024-10-28/2024-10-22-raspios-bullseye-arm64-lite.img.xz)

hostname: octopuspi

username: octopus

## Script & playbook installs & starts the following:
- Docker
- Docker Compose
- Git
- Python3
- Pip3
- Ansible
- GivTCP
- Mosquitto

## Required files on fresh system
- ansible.cfg
- maintenance_script.sh
- requirements.yml

All other files are pulled in by script & Ansible.

## Access
```bash
ssh ssh octopus@octopuspi.local
```

## Copy files to remote system
```bash
scp -r ansible.cfg maintenance_script.sh requirements.yml octopus@octopuspi.local:/home/octopus/
```

## How to run
Must be sudo
```bash
sudo ./maintenance_script.sh
```

## GivTC
Interface available on: http://octopuspi.local:8099