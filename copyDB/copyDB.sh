#!/bin/sh

cd `dirname $0`

scp createDataYaml.py createOtherYaml.py yaml_utils.py mars:~/

# プロジェクトルートの fixture ディレクトリを使用するように修正
mkdir -p ../fixture

# 1Passwordからデータベース認証情報を一括で読み込む（1回のみ）
# テンプレートを使用して1回のop injectで全ての情報を取得し、
# IFS= read -r を用いて各変数に安全に代入する。
{
  cat <<EOT | op inject
{{op://Personal/Mariadb_MoneyBook/hostname}}
{{op://Personal/Mariadb_MoneyBook/port}}
{{op://Personal/Mariadb_MoneyBook/username}}
{{op://Personal/Mariadb_MoneyBook/password}}
{{op://Personal/Mariadb_MoneyBook/database}}
EOT
} | {
  IFS= read -r DB_HOSTNAME
  IFS= read -r DB_PORT
  IFS= read -r DB_USER
  IFS= read -r DB_PASSWORD
  IFS= read -r DB_DATABASE

  # 変数に代入された後、それらを使用して後続の処理を行う必要があるため、
  # 中括弧ブロック内でコマンドを実行する。

  # コマンドライン引数ではなく標準入力経由でデータベース認証情報を渡す
  db_creds=$(printf "%s\n" "$DB_HOSTNAME" "$DB_PORT" "$DB_USER" "$DB_PASSWORD" "$DB_DATABASE")
  echo "$db_creds" | ssh mars python3 /home/tmorriss/createDataYaml.py > ../fixture/data_all.yaml

  echo "$db_creds" | ssh mars python3 /home/tmorriss/createOtherYaml.py > ../fixture/initial_data.yaml
}

# プロジェクトルートの manage.py を実行
python3 ../manage.py loaddata ../fixture/initial_data.yaml
python3 ../manage.py loaddata ../fixture/data_all.yaml
