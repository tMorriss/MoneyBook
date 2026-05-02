#!/bin/sh

cd `dirname $0`

scp createDataYaml.py createOtherYaml.py yaml_utils.py mars:~/

# プロジェクトルートの fixture ディレクトリを使用するように修正
mkdir -p ../fixture

# 1Passwordからデータベース認証情報を一括で読み込む（1回のみ）
# op item get ... --format json と jq を使用して安全に変数へ代入する
# フィールドが存在しない場合は空文字列を返すように // "" を使用
eval "$(op item get "Mariadb_MoneyBook" --vault "Personal" --format json | jq -r '
  .fields | map({key: .label, value: .value}) | from_entries |
  "DB_HOSTNAME=\((.hostname // "") | @sh)\n" +
  "DB_PORT=\((.port // "") | @sh)\n" +
  "DB_USER=\((.username // "") | @sh)\n" +
  "DB_PASSWORD=\((.password // "") | @sh)\n" +
  "DB_DATABASE=\((.database // "") | @sh)"
')"

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
