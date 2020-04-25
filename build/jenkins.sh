cd /home/programs/MoneyBook
git pull origin master

# pull docker images
sudo podman pull docker.io/library/python:3
sudo podman pull docker.io/library/nginx:latest

# build docker image
sudo podman build -t moneybook_gunicorn ./build/

# stop container
count=`sudo podman ps |grep moneybook_gunicorn |wc -l`
if [ $count -gt 0 ]; then
  sudo podman stop moneybook_gunicorn
fi
# remove container
count=`sudo podman ps -a |grep moneybook_gunicorn |wc -l`
if [ $count -gt 0 ]; then
  sudo podman rm moneybook_gunicorn
fi

# DB migration
python3 manage.py makemigrations --settings config.settings.prod
python3 manage.py migrate --settings config.settings.prod

# deploy container
sudo podman run -d --restart=always -p 8080:80 -v /home/programs/MoneyBook/:/MoneyBook/ --name moneybook_gunicorn -h moneybook_gunicorn moneybook_gunicorn

# delete old images
sudo podman image prune