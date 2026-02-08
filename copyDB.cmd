@echo off

cd %~dp0

scp createDataYaml.py createOtherYaml.py mars:~/

mkdir fixture

REM 1Passwordからデータベース認証情報を読み込む
REM プロセスリストに認証情報が表示されることを防ぐ

REM コマンドライン引数ではなく標準入力経由でデータベース認証情報を渡す
(
  op read "op://Personal/Mariadb_MoneyBook/hostname"
  op read "op://Personal/Mariadb_MoneyBook/port"
  op read "op://Personal/Mariadb_MoneyBook/username"
  op read "op://Personal/Mariadb_MoneyBook/password"
  op read "op://Personal/Mariadb_MoneyBook/database"
) | ssh mars python3 /home/tmorriss/createDataYaml.py > fixture\data_all.yaml

(
  op read "op://Personal/Mariadb_MoneyBook/hostname"
  op read "op://Personal/Mariadb_MoneyBook/port"
  op read "op://Personal/Mariadb_MoneyBook/username"
  op read "op://Personal/Mariadb_MoneyBook/password"
  op read "op://Personal/Mariadb_MoneyBook/database"
) | ssh mars python3 /home/tmorriss/createOtherYaml.py > fixture\initial_data.yaml

python manage.py loaddata fixture\initial_data.yaml
python manage.py loaddata fixture\data_all.yaml
