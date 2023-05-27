cd ~
git clone --branch production https://github.com/lautisilber/NewMovereFleet.git

sudo apt install python3-pip -y
sudo apt install python3-venv -y
cd NewMovereFleet
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# don't forget to create /etc/config.json file. example below
# {
#     "SECRET_KEY": "<secret>",
#     "ALLOWED_HOSTS": ["<allowed hosts>"]
# }
