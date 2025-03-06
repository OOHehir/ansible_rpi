## Setup

### Install Ansible

```bash
sudo apt update
sudo apt-get install -y ansible git
```

### Enable Ansible service

```bash
sudo systemctl enable ansible
sudo systemctl start ansible
```

### Running
Ensure /home/octopus/ansible exists and is owned by octopus user.

```bash
