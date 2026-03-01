@echo off

cd %~dp0

scp createDataYaml.py createOtherYaml.py yaml_utils.py mars:~/

if not exist "..\fixture" mkdir "..\fixture"

REM 1Passwordからデータベース認証情報を読み込む（1回のみ）
for /f "delims=" %%i in ('op read "op://Personal/Mariadb_MoneyBook/hostname"') do set DB_HOSTNAME=%%i
for /f "delims=" %%i in ('op read "op://Personal/Mariadb_MoneyBook/port"') do set DB_PORT=%%i
for /f "delims=" %%i in ('op read "op://Personal/Mariadb_MoneyBook/username"') do set DB_USER=%%i
for /f "delims=" %%i in ('op read "op://Personal/Mariadb_MoneyBook/password"') do set DB_PASSWORD=%%i
for /f "delims=" %%i in ('op read "op://Personal/Mariadb_MoneyBook/database"') do set DB_DATABASE=%%i

REM コマンドライン引数ではなく標準入力経由でデータベース認証情報を渡す
(
  echo %DB_HOSTNAME%
  echo %DB_PORT%
  echo %DB_USER%
  echo %DB_PASSWORD%
  echo %DB_DATABASE%
) | ssh mars python3 /home/tmorriss/createDataYaml.py > ..\fixture\data_all.yaml

(
  echo %DB_HOSTNAME%
  echo %DB_PORT%
  echo %DB_USER%
  echo %DB_PASSWORD%
  echo %DB_DATABASE%
) | ssh mars python3 /home/tmorriss/createOtherYaml.py > ..\fixture\initial_data.yaml

python ..\manage.py loaddata ..\fixture\initial_data.yaml
python ..\manage.py loaddata ..\fixture\data_all.yaml
