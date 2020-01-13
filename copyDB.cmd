@echo off

cd %~dp0

scp createDataYaml.py createOtherYaml.py tmorriss:~/

ssh tmorriss python3 /home/tmorriss/createDataYaml.py > fixture\data_all.yaml
ssh tmorriss python3 /home/tmorriss/createOtherYaml.py > fixture\initial_data.yaml

python manage.py loaddata fixture\initial_data.yaml
python manage.py loaddata fixture\data_all.yaml