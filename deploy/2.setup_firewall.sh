# firewall configuration
sudo apt install ufw -y
sudo ufw default allow outgoing
sudo ufw default deny incoming
sudo ufw allow ssh
sudo ufw allow http/tcp
sudo ufw allow https
sudo ufw enable
sudo ufw status