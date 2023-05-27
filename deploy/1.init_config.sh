sudo apt update
sudo apt upgrade -y

hostnamectl set-hostname movere-server # edit /etc/hosts file
adduser lautisilber
adduser lautisilber sudo

# logging in as lautisilber
mkdir -p ~/.ssh/
# on local machine
scp ~/.ssh/id_ed25519.pub movere-server:~/.ssh/authorized_keys

# on server
sudo chmod 700 ~/.ssh/
sudo chmod 600 ~/.ssh/*
# edit /etc/ssh/sshd_config file
sudo systemctl restart sshd