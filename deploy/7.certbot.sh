sudo snap install core
sudo snap refresh core

sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
sudo certbot --nginx

# test
sudo certbot renew --dry-run

# add monthly renewal
sudo crontab -e
# write this line: 30 4 1 * * sudo certbot renew --quiet