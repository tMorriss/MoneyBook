#!/bin/sh

cd `dirname $0`

scp createDataYaml.py createOtherYaml.py yaml_utils.py mars:~/

# プロジェクトルートの fixture ディレクトリを使用するように修正
mkdir -p ../fixture

# 1Passwordからデータベース認証情報を読み込む（1回のみ）
DB_HOSTNAME=$(op read "op://Personal/Mariadb_MoneyBook/hostname")
DB_PORT=$(op read "op://Personal/Mariadb_MoneyBook/port")
DB_USER=$(op read "op://Personal/Mariadb_MoneyBook/username")
DB_PASSWORD=$(op read "op://Personal/Mariadb_MoneyBook/password")
DB_DATABASE=$(op read "op://Personal/Mariadb_MoneyBook/database")

# コマンドライン引数ではなく標準入力経由でデータベース認証情報を渡す
{
  echo "$DB_HOSTNAME"
  echo "$DB_PORT"
  echo "$DB_USER"
  echo "$DB_PASSWORD"
  echo "$DB_DATABASE"
} | ssh mars python3 /home/tmorriss/createDataYaml.py > ../fixture/data_all.yaml

{
  echo "$DB_HOSTNAME"
  echo "$DB_PORT"
  echo "$DB_USER"
  echo "$DB_PASSWORD"
  echo "$DB_DATABASE"
} | ssh mars python3 /home/tmorriss/createOtherYaml.py > ../fixture/initial_data.yaml

# プロジェクトルートの manage.py を実行
python3 ../manage.py loaddata ../fixture/initial_data.yaml
python3 ../manage.py loaddata ../fixture/data_all.yaml
