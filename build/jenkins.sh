# pull docker images
sudo podman pull docker.io/library/python:3
sudo podman pull docker.io/library/nginx:latest

# build docker image
sudo podman build -t tmorriss/moneybook -f ./build/Dockerfile ./

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
sudo podman run \
-e DB_NAME=$DB_NAME \
-e DB_USER=$DB_USER \
-e DB_PASS=$DB_PASS \
-e DB_HOST=$DB_HOST \
-h moneybook_migration \
--name moneybook_migration \
--rm \
tmorriss/moneybook \
/bin/bash -c \
"/usr/bin/python3 /MoneyBook/manage.py makemigrations --settings config.settings.prod && \
/usr/bin/python3 /MoneyBook/manage.py migrate --settings config.settings.prod"

# deploy container
sudo podman run \
-d \
--restart=always \
-p 8080:80 \
-e DB_NAME=$DB_NAME \
-e DB_USER=$DB_USER \
-e DB_PASS=$DB_PASS \
-e DB_HOST=$DB_HOST \
-h moneybook \
--name moneybook \
tmorriss/moneybook

# delete old images
sudo podman image prune