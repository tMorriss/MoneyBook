@echo off

cd %~dp0

scp createDataYaml.py createOtherYaml.py mars:~/

mkdir fixture

ssh mars python3 /home/tmorriss/createDataYaml.py > fixture\data_all.yaml
ssh mars python3 /home/tmorriss/createOtherYaml.py > fixture\initial_data.yaml

python manage.py loaddata fixture\initial_data.yaml
python manage.py loaddata fixture\data_all.yaml
