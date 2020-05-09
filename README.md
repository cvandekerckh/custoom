# Custoom
Flask script for website 

# A. Development preparation
##  Step 0 : download elastic search
instructions for MAC :
https://medium.com/@felixgondwe/elasticsearch-setup-using-homebrew-2017891f62bb
commands:
- `brew install elasticsearch`
- `brew services start elasticsearch`
- test : http://localhost:9200

##  Step 1 : setting up gmail for password reset
Create .env file and set environment the following ENV variable

export MAIL_SERVER=smtp.googlemail.com
export MAIL_PORT=587
export MAIL_USE_TLS=1
export MAIL_USERNAME=<your-gmail-email>
export MAIL_PASSWORD=<your-gmail-password>
export MS_TRANSLATOR_KEY=<your-azur-translator-key>
export ELASTICSEARCH_URL=http://localhost:9200

## Step 2 : allow you gmail account to send emails
click on https://myaccount.google.com/lesssecureapps and  unlock

##  Step 3: setting up virtual environment
- setting the right python version using pyenv
- running `pipenv install`

## Step 4 : running flask
- running `flask run`

# Production Details
##  Step 1 : ssh connect to instance and prepare environment
`ssh -i ~/.ssh/gc corentinvdk@104.155.161.68`
(protect your instance : https://blog.miguelgrinberg.com/)

## Step 2 : install environment
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl
sudo apt-get install git
curl https://pyenv.run | bash
(following instruction)
reload shell
pyenv install --list | grep " 3\.[678]"
pyenv install -v 3.7.2
sudo apt-get update
sudo apt-get -y install mysql-server postfix supervisor nginx git
Internet Configuration for postfix
pip install -U pipenv

# Step 3 : prepare .env
SECRET_KEY=(gen by python -c "import uuid; print(uuid.uuid4().hex)")
MAIL_SERVER=localhost
MAIL_PORT=25
DATABASE_URL=mysql+pymysql://custoom:<db-password>@localhost:3306/custoom
MS_TRANSLATOR_KEY=<your-translator-key-here>

## 3.1 Setting up emails
see https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-postfix-as-a-send-only-smtp-server-on-debian-9
- with gmail, bypass additional security (captcha) by checking https://accounts.google.com/b/0/DisplayUnlockCaptcha
- without gmail, good luck...

## 3.2 Setting up elastic search
looks too intense for a small server

## 3.3 Setting up distrib
- redis : apt-get install redis-server + gunicorn
- cp /etc/supervisor/conf.d/custoom.conf
/etc/supervisor/conf.d/rq.conf (and adapt content)
(ideally adapting to multiple processes)
- sudo supervisorctl reload

# Step 4 : prepare languages
flask translate compile

# Step 5 : set up db
setting up db
mysql -u root -p
mysql> create database custoom character set utf8 collate utf8_bin;
mysql> create user 'custoom'@'localhost' identified by 'sZQ9NdjghCGykLwaWjPyfQUu';
mysql> grant all privileges on custoom.(star) to 'custoom'@'localhost';
mysql> flush privileges;
mysql> quit;

if issues :
USE mysql;
CREATE USER 'debian'@'localhost' IDENTIFIED BY '';
GRANT ALL PRIVILEGES ON *.* TO 'debian'@'localhost';
UPDATE user SET plugin='unix_socket' WHERE User='debian';

# Step 6 : deploy
gunicorn file (/etc/supervisor/conf.d/custoom.conf):
[program:custoom]
command=/home/ubuntu/custoom/venv/bin/gunicorn -b localhost:8000 -w 4 custoom:app
directory=/home/ubuntu/custoom
user=ubuntu
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
where gunicorn is referenced from virtualenv

useful commands:
sudo supervisorctl status all
sudo supervisorctl reload
sudo vim /etc/nginx/sites-enabled/custoom
sudo nginx -c /etc/nginx/nginx.conf -t
sudo service nginx reload
service nginx status

# Step 7 : get certificate using certbot
see tutorial. If issues:
sudo apt-get install dirmngr
sudo certbot certonly --webroot -w /home/debian/custoom/app/static -d thementaldoctors.com

# Step 8 : update application
(venv) $ git pull                              # download the new version
(vend) $ (pipenv install) if modif made
(venv) $ sudo supervisorctl stop custoom     # stop the current server
(venv) $ flask db upgrade                      # upgrade the database
(venv) $ flask translate compile               # upgrade the translations
(venv) $ sudo supervisorctl start custoom    # start a new server

# Step 9 : misc

checking storage remaining:
df -H /dev/sda1
allow https on compute :)

# API Queries
- get token:
http --auth cvandekerckh:<password> POST https://thementaldoctors.com/api/tokens

- get user:
http GET https://thementaldoctors.com/api/users/1 \
    "Authorization:Bearer pC1Nu9wwyNt8VCj1trWilFdFI276AcbS"
