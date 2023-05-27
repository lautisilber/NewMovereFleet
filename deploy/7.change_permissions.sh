# sudo chown lautisilber:www-data ~/NewMovereFleet/db.sqlite3
# sudo chmod 775 ~/NewMovereFleet/db.sqlite3

# sudo chown -R lautisilber:www-data /home/lautisilber/NewMovereFleet/static
# sudo chmod -R 775 /home/lautisilber/NewMovereFleet/static

# sudo chown lautisilber:www-data /home/lautisilber/NewMovereFleet
# sudo chmod 775 /home/lautisilber/NewMovereFleet

sudo cp -r /home/lautisilber/NewMovereFleet/static /var/www/static

# sudo chown :www-data /var
# sudo chmod 775 /var

# sudo chown :www-data /var/www
# sudo chmod 775 /var/www

sudo chown -R :www-data /var/www/static
sudo chmod -R 775 /var/www/static
