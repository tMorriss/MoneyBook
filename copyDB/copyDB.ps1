# カレントディレクトリの移動
Set-Location $PSScriptRoot

scp createDataYaml.py createOtherYaml.py yaml_utils.py mars:~/

# プロジェクトルートの fixture ディレクトリを使用するように修正
if (-not (Test-Path "..\fixture")) {
    New-Item -ItemType Directory -Path "..\fixture"
}

# 1Passwordからデータベース認証情報を一括で読み込む（1回のみ）
# op item get ... --format json と ConvertFrom-Json を使用してオブジェクトとして取得
# 日本語環境でも正しく取得できるよう、label ではなく id を使用してマッピングする
$opJson = op item get "Mariadb_MoneyBook" --vault "Personal" --format json | ConvertFrom-Json
$fields = $opJson.fields | ForEach-Object { $hash = @{} } { $hash[$_.id] = $_.value } { $hash }

$DB_HOSTNAME = $fields["hostname"]
$DB_PORT = $fields["port"]
$DB_USER = $fields["username"]
$DB_PASSWORD = $fields["password"]
$DB_DATABASE = $fields["database"]

# コマンドライン引数ではなく標準入力経由でデータベース認証情報を渡す
$dbInfo = @"
$DB_HOSTNAME
$DB_PORT
$DB_USER
$DB_PASSWORD
$DB_DATABASE
"@

$dbInfo | ssh mars python3 /home/tmorriss/createDataYaml.py > ..\fixture\data_all.yaml
$dbInfo | ssh mars python3 /home/tmorriss/createOtherYaml.py > ..\fixture\initial_data.yaml

python ..\manage.py loaddata ..\fixture\initial_data.yaml
python ..\manage.py loaddata ..\fixture\data_all.yaml
