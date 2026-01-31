#!/bin/sh

cd `dirname $0`

# rm moneybook/db.sqlite3
# python3 manage.py makemigrations
# python3 manage.py migrate

scp createDataYaml.py createOtherYaml.py mars:~/

mkdir -p fixture

DB_HOSTNAME=$(op read "op://Personal/Mariadb_MoneyBook/hostname")
DB_PORT=$(op read "op://Personal/Mariadb_MoneyBook/port")
DB_USER=$(op read "op://Personal/Mariadb_MoneyBook/username")
DB_PASSWORD=$(op read "op://Personal/Mariadb_MoneyBook/password")
DB_DATABASE=$(op read "op://Personal/Mariadb_MoneyBook/database")

ssh mars python3 /home/tmorriss/createDataYaml.py "$DB_HOSTNAME" "$DB_PORT" "$DB_USER" "$DB_PASSWORD" "$DB_DATABASE" > fixture/data_all.yaml
ssh mars python3 /home/tmorriss/createOtherYaml.py "$DB_HOSTNAME" "$DB_PORT" "$DB_USER" "$DB_PASSWORD" "$DB_DATABASE" > fixture/initial_data.yaml

python3 manage.py loaddata fixture/initial_data.yaml
python3 manage.py loaddata fixture/data_all.yaml
