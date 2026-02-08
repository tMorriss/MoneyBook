# MoneyBook

自分用家計簿 Web アプリケーション

## デプロイ

このアプリケーションはPodmanコンテナで実行されます。nginxとgunicornは同じPod内の別々のコンテナで実行されるサイドカーパターンを採用しています。

Pod定義はKubernetes互換のYAML形式（`build/pod.yaml`）で管理されており、`podman play kube`コマンドで起動します。

### 環境変数の設定

以下の環境変数を設定する必要があります：
- `PODMAN_USER`: Podmanを実行するユーザー名（必須）
- `DB_NAME`: データベース名
- `DB_USER`: データベースユーザー
- `DB_PASS`: データベースパスワード
- `DB_HOST`: データベースホスト
- `HOST_NAME`: ホスト名（nginxのserver_nameとDjangoのALLOWED_HOSTSで使用）
- `SECRET_KEY`: Djangoのシークレットキー

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

E2E テストは並列実行に対応しており、テスト時間を大幅に短縮できます。

### 基本的な実行

```
# 並列実行（推奨）
$ python manage.py test moneybook.selenium --settings config.settings.test --parallel auto

# 並列数を指定（例：4並列）
$ python manage.py test moneybook.selenium --settings config.settings.test --parallel 4

# シングルプロセスで実行
$ python manage.py test moneybook.selenium --settings config.settings.test
```

### ヘッドレスモード

E2E テストはデフォルトでヘッドレスモードで実行されます。ブラウザを表示して実行する場合は、環境変数`HEADLESS=0`を設定してください。

```
# mac
$ HEADLESS=0 python manage.py test moneybook.selenium --settings config.settings.test --parallel auto
# winodows
$ $env:HEADLESS="0"; python manage.py test moneybook.selenium --settings config.settings.test --parallel auto
```

**注意**: 並列実行時にブラウザを表示すると、複数のブラウザウィンドウが同時に開きます。デバッグ目的の場合は、並列数を1に制限するか、`--parallel`オプションを外すことをお勧めします。

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
