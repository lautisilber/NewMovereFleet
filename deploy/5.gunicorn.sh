sudo apt install supervisor -y

cd /home/lautisilber/NewMovereFleet
source venv/bin/activate
pip install gunicorn

# gunicorn -w=3 --env DJANGO_SETTINGS_MODULE=MovereFleet.settings MovereFleet.wsgi:application --chdir /home/lautisilber/NewMovereFleet

sudo cp deploy/server.supervisor /etc/supervisor/conf.d/moverefleet.conf
sudo mkdir -p /var/log/moverefleet/

sudo supervisorctl update
sudo supervisorctl reload
