# MoneyBook

自分用家計簿 Web アプリケーション

## デプロイ

このアプリケーションはPodmanコンテナで実行されます。nginxとgunicornは同じPod内の別々のコンテナで実行されるサイドカーパターンを採用しています。

### 環境変数の設定

以下の環境変数を設定する必要があります：
- `DB_NAME`: データベース名
- `DB_USER`: データベースユーザー
- `DB_PASS`: データベースパスワード
- `DB_HOST`: データベースホスト
- `ALLOWED_HOSTS`: 許可するホスト名
- `SECRET_KEY`: Djangoのシークレットキー

### デプロイ方法

```bash
cd /path/to/MoneyBook
./build/jenkins.sh
```

このスクリプトは以下を実行します：
- ベースイメージのpull
- コンテナイメージのビルド
- Podの作成
- データベースマイグレーション
- コンテナの起動（自動再起動設定付き）

### 手動でのコンテナ操作

```bash
# Podとコンテナの起動（初回）
sudo podman pod create --name moneybook-pod -p 8080:80
sudo podman run -d --name moneybook_gunicorn --pod moneybook-pod --restart=always -e DB_NAME=$DB_NAME -e DB_USER=$DB_USER -e DB_PASS=$DB_PASS -e DB_HOST=$DB_HOST -e ALLOWED_HOSTS=$ALLOWED_HOSTS -e SECRET_KEY=$SECRET_KEY moneybook_gunicorn:latest
sudo podman run -d --name moneybook_nginx --pod moneybook-pod --restart=always moneybook_nginx:latest

# Podの停止
sudo podman pod stop moneybook-pod

# Podの起動
sudo podman pod start moneybook-pod

# ログの確認
sudo podman logs -f moneybook_gunicorn
sudo podman logs -f moneybook_nginx

# Pod/コンテナの状態確認
sudo podman pod ps
sudo podman ps --filter pod=moneybook-pod
```

## lint 確認

```
$ flake8 . --count --ignore=E722,W503 --max-line-length=140 --exclude moneybook/migrations,__init__.py --show-source --statistics --import-order-style smarkets
```

## 単体テスト

[![codecov](https://codecov.io/gh/tMorriss/MoneyBook/branch/master/graph/badge.svg?token=E522OPRLRM)](https://codecov.io/gh/tMorriss/MoneyBook)

```
$ coverage run --source='moneybook.models,moneybook.views,moneybook.utils,moneybook.middleware,moneybook.forms' manage.py test moneybook.tests --settings config.settings.test
# レポートを表示
$ coverage report -m

# VSCodeでハイライト
$ coverage xml
# vscodeのコマンド
>code coverage: Toggle coverage display
```

## E2E テスト

```
$ python manage.py test moneybook.selenium --settings config.settings.test
```

### ヘッドレスモード

E2E テストはデフォルトでヘッドレスモードで実行されます。ブラウザを表示して実行する場合は、環境変数`HEADLESS=0`を設定してください。

```
# mac
$ HEADLESS=0 python manage.py test moneybook.selenium --settings config.settings.test
# winodows
$ $env:HEADLESS="0"; python manage.py test moneybook.selenium --settings config.settings.test
```

## メモ

### venv

```
## windows
# 作成
python -m venv .venv

# activate
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\.venv\Scripts\activate

# deactivate
deactivate

```
