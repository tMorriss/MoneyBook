# MoneyBook

自分用家計簿 Web アプリケーション

## デプロイ

このアプリケーションはDockerコンテナで実行されます。nginxとgunicornは別々のコンテナで実行されるサイドカーパターンを採用しています。

### 環境変数の設定

`.env.example`をコピーして`.env`ファイルを作成し、必要な環境変数を設定してください。

```bash
cp .env.example .env
# .envファイルを編集して適切な値を設定
```

### デプロイ方法

```bash
cd /path/to/MoneyBook
./build/jenkins.sh
```

このスクリプトは以下を実行します：
- ベースイメージのpull
- Dockerイメージのビルド
- データベースマイグレーション
- コンテナの起動（自動再起動設定付き）

### 手動でのコンテナ操作

```bash
# コンテナの起動
sudo docker-compose up -d

# コンテナの停止
sudo docker-compose down

# ログの確認
sudo docker-compose logs -f

# コンテナの状態確認
sudo docker-compose ps
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
