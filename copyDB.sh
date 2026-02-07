#!/bin/sh

cd `dirname $0`

# rm moneybook/db.sqlite3
# python3 manage.py makemigrations
# python3 manage.py migrate

scp createDataYaml.py createOtherYaml.py mars:~/

mkdir -p fixture

# 1Passwordからデータベース認証情報を読み込む関数
# プロセスリストに認証情報が表示されることを防ぐ
get_db_credentials() {
  op read "op://Personal/Mariadb_MoneyBook/hostname"
  op read "op://Personal/Mariadb_MoneyBook/port"
  op read "op://Personal/Mariadb_MoneyBook/username"
  op read "op://Personal/Mariadb_MoneyBook/password"
  op read "op://Personal/Mariadb_MoneyBook/database"
}

# コマンドライン引数ではなく標準入力経由でデータベース認証情報を渡す
get_db_credentials | ssh mars python3 /home/tmorriss/createDataYaml.py > fixture/data_all.yaml
get_db_credentials | ssh mars python3 /home/tmorriss/createOtherYaml.py > fixture/initial_data.yaml

python3 manage.py loaddata fixture/initial_data.yaml
python3 manage.py loaddata fixture/data_all.yaml
