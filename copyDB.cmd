@echo off

cd %~dp0

scp createDataYaml.py createOtherYaml.py yaml_utils.py mars:~/

mkdir fixture

for /f "delims=" %%i in ('op read "op://Personal/Mariadb_MoneyBook/hostname"') do set DB_HOSTNAME=%%i
for /f "delims=" %%i in ('op read "op://Personal/Mariadb_MoneyBook/port"') do set DB_PORT=%%i
for /f "delims=" %%i in ('op read "op://Personal/Mariadb_MoneyBook/username"') do set DB_USER=%%i
for /f "delims=" %%i in ('op read "op://Personal/Mariadb_MoneyBook/password"') do set DB_PASSWORD=%%i
for /f "delims=" %%i in ('op read "op://Personal/Mariadb_MoneyBook/database"') do set DB_DATABASE=%%i

ssh mars python3 /home/tmorriss/createDataYaml.py "%DB_HOSTNAME%" "%DB_PORT%" "%DB_USER%" "%DB_PASSWORD%" "%DB_DATABASE%" > fixture\data_all.yaml
ssh mars python3 /home/tmorriss/createOtherYaml.py "%DB_HOSTNAME%" "%DB_PORT%" "%DB_USER%" "%DB_PASSWORD%" "%DB_DATABASE%" > fixture\initial_data.yaml

python manage.py loaddata fixture\initial_data.yaml
python manage.py loaddata fixture\data_all.yaml
