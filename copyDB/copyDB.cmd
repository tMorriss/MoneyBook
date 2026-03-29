@echo off

cd %~dp0

scp createDataYaml.py createOtherYaml.py yaml_utils.py mars:~/

if not exist "..\fixture" mkdir "..\fixture"

REM 1Passwordからデータベース認証情報を一括で読み込む（1回のみ）
REM 複数のechoコマンドを&で繋ぎ、op injectに渡す。
REM 変数名=値の形式で出力させ、for /fループでsetコマンドを実行する。
REM (echo VAR=VALUE& echo VAR2=VALUE2)のように、&の前にスペースを置かないことで、
REM 値に余分なスペースが含まれるのを防ぐ。
for /f "delims=" %%i in ('(echo DB_HOSTNAME^={{op://Personal/Mariadb_MoneyBook/hostname}}^&echo DB_PORT^={{op://Personal/Mariadb_MoneyBook/port}}^&echo DB_USER^={{op://Personal/Mariadb_MoneyBook/username}}^&echo DB_PASSWORD^={{op://Personal/Mariadb_MoneyBook/password}}^&echo DB_DATABASE^={{op://Personal/Mariadb_MoneyBook/database}}) ^| op inject') do set "%%i"

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
