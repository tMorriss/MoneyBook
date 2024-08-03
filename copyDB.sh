#!/bin/sh

cd `dirname $0`

# rm moneybook/db.sqlite3
# python3 manage.py makemigrations
# python3 manage.py migrate

scp createDataYaml.py createOtherYaml.py mars:~/

mkdir -p fixture

ssh mars python3 /home/tmorriss/createDataYaml.py > fixture/data_all.yaml
ssh mars python3 /home/tmorriss/createOtherYaml.py > fixture/initial_data.yaml

python3 manage.py loaddata fixture/initial_data.yaml
python3 manage.py loaddata fixture/data_all.yaml
