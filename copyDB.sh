#!/bin/sh

cd `dirname $0`

# rm moneybook/db.sqlite3
# python3 manage.py makemigrations
# python3 manage.py migrate

scp createDataYaml.py createOtherYaml.py mars:~/

mkdir -p fixture

# Pass database credentials via stdin instead of command-line arguments
# This prevents credentials from being visible in process listings
{
  op read "op://Personal/Mariadb_MoneyBook/hostname"
  op read "op://Personal/Mariadb_MoneyBook/port"
  op read "op://Personal/Mariadb_MoneyBook/username"
  op read "op://Personal/Mariadb_MoneyBook/password"
  op read "op://Personal/Mariadb_MoneyBook/database"
} | ssh mars python3 /home/tmorriss/createDataYaml.py > fixture/data_all.yaml

{
  op read "op://Personal/Mariadb_MoneyBook/hostname"
  op read "op://Personal/Mariadb_MoneyBook/port"
  op read "op://Personal/Mariadb_MoneyBook/username"
  op read "op://Personal/Mariadb_MoneyBook/password"
  op read "op://Personal/Mariadb_MoneyBook/database"
} | ssh mars python3 /home/tmorriss/createOtherYaml.py > fixture/initial_data.yaml

python3 manage.py loaddata fixture/initial_data.yaml
python3 manage.py loaddata fixture/data_all.yaml
