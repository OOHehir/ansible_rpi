#!/usr/bin/env bash
ANSIBLE_BIN_PATH=/home/octopus/.local/bin

$ANSIBLE_BIN_PATH/ansible-galaxy collection install -r requirements.yml