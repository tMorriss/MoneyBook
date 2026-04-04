@echo off

cd %~dp0

scp createDataYaml.py createOtherYaml.py yaml_utils.py mars:~/

if not exist "..\fixture" mkdir "..\fixture"

REM 1Passwordからデータベース認証情報を一括で読み込む（1回のみ）
REM op item get ... --format json と jq を使用して、変数名=値の形式で出力させ、
REM for /fループでsetコマンドを介して一括設定する。
for /f "delims=" %%i in ('op item get "Mariadb_MoneyBook" --vault "Personal" --format json ^| jq -r ".fields | map({key: .label, value: .value}) | from_entries | \"DB_HOSTNAME=\(.hostname)\", \"DB_PORT=\(.port)\", \"DB_USER=\(.username)\", \"DB_PASSWORD=\(.password)\", \"DB_DATABASE=\(.database)\""') do set "%%i"

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
