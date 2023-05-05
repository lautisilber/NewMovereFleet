sudo ufw default allow outgoing 
sudo ufw default deny incoming
sudo ufw allow ssh
sudo ufw enable
sudo ufw status

# echo "Check that no errors occured and enter \"Y\": "
# read CONFIRM

# if [ $CONFIRM == "Y" ]; then
# fi
