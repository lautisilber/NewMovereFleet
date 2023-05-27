cd /home/lautisilber/NewMovereFleet

source venv/bin/activate
python manage.py check
python manage.py collectstatic
python manage.py makemigrations
python manage.py migrate