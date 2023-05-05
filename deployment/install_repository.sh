cd ~
git clone git@github.com:lautisilber/NewMovereFleet.git
cd ./NewMovereFleet
python3.11 -m venv venv
pip3.11 install -r requirements.txt
pip3.11 install gunicorn