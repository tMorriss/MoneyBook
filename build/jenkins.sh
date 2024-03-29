# pull docker images
sudo podman pull quay.io/centos/centos:stream8

# build docker image
sudo podman build -t tmorriss/moneybook -f ./build/Dockerfile ./

# stop container
count=`sudo podman ps |grep moneybook |wc -l`
if [ $count -gt 0 ]; then
  sudo podman stop moneybook
fi
# remove container
count=`sudo podman ps -a |grep moneybook |wc -l`
if [ $count -gt 0 ]; then
  sudo podman rm moneybook
fi

# DB migration
sudo podman run \
-e DB_NAME=$DB_NAME \
-e DB_USER=$DB_USER \
-e DB_PASS=$DB_PASS \
-e DB_HOST=$DB_HOST \
-e SECRET_KEY=$SECRET_KEY \
-h moneybook_migration \
--name moneybook_migration \
--rm \
tmorriss/moneybook \
/bin/bash -c \
"/usr/bin/python3 /MoneyBook/manage.py migrate --settings config.settings.prod"

# deploy container
sudo podman run \
-d \
--restart=always \
-p 8080:80 \
-e DB_NAME=$DB_NAME \
-e DB_USER=$DB_USER \
-e DB_PASS=$DB_PASS \
-e DB_HOST=$DB_HOST \
-e ALLOWED_HOSTS=$ALLOWED_HOSTS \
-e SECRET_KEY=$SECRET_KEY \
-h moneybook \
--name moneybook \
tmorriss/moneybook

# delete old images
sudo podman image prune -f
