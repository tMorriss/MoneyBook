# MoneyBook

自分用家計簿 Web アプリケーション

## デプロイ

このアプリケーションはPodmanコンテナで実行されます。nginxとgunicornは同じPod内の別々のコンテナで実行されるサイドカーパターンを採用しています。

Podおよびコンテナの管理には **Podman Quadlet**（systemd 連携）を使用しています。`build/quadlet/` 配下のテンプレートを元に生成された Quadlet ユニットファイルがユーザーの `~/.config/containers/systemd/moneybook/` に配置され、systemd ユーザーサービス（`moneybook-pod.service`）として起動・管理されます。

ホスト再起動時や障害発生時も `loginctl enable-linger` および systemd / Quadlet の `Restart=always` 設定により自動的に再起動します。

### 環境変数の設定

デプロイ時（`build/jenkins.sh` 実行時）に以下の環境変数を指定します。データベース接続情報や Django シークレットキーなどの機密情報は **Podman Secrets** に安全に登録され、コンテナへ渡されます。

- `PODMAN_USER`: Podmanを実行するユーザー名（必須）
- `DB_NAME`: データベース名
- `DB_USER`: データベースユーザー
- `DB_PASS`: データベースパスワード
- `DB_HOST`: データベースホスト
- `HOST_NAME`: ホスト名（nginxのserver_nameとDjangoのALLOWED_HOSTSで使用）
- `SECRET_KEY`: Djangoのシークレットキー

### サービスの操作コマンド（ユーザー権限）

```bash
# サービスの状態確認
systemctl --user status moneybook-pod.service

# サービスの起動・再起動
systemctl --user restart moneybook-pod.service

# サービスの停止
systemctl --user stop moneybook-pod.service

# ログの確認
journalctl --user -u moneybook-pod.service
journalctl --user -u moneybook-gunicorn.service
journalctl --user -u moneybook-nginx.service
```

## lint 確認

```
$ tox -e lint
```

## 単体テスト

[![codecov](https://codecov.io/gh/tMorriss/MoneyBook/branch/master/graph/badge.svg?token=E522OPRLRM)](https://codecov.io/gh/tMorriss/MoneyBook)

```
$ tox -e unittest
```

## e2e テスト

e2e テストは PostgreSQL を使用します。テストを実行する前に、以下のコマンドで PostgreSQL コンテナを起動してください。

```
$ docker run --rm -d -p 5432:5432 -e POSTGRES_DB=moneybook_e2e -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres --name moneybook-postgres-e2e postgres:15
```

e2e テストはデフォルトでヘッドレスモードで実行されます。

```
# 全てのe2eテストを実行
$ tox -e e2e

## ブラウザを表示して実行
# mac
$ HEADLESS=0 tox -e e2e
# windows
$ $env:HEADLESS="0"; tox -e e2e

## 特定のテストモジュールを実行（例：indexモジュールのみ）
# mac
$ HEADLESS=0 TEST_MODULE=moneybook.e2e.index tox -e e2e

# windows
$ $env:HEADLESS="0"; $env:TEST_MODULE="moneybook.e2e.index"; tox -e e2e
```

### 他

```
## デバッグログ
# mac
$ EXTRA_OPTIONS="-v 2"

# windows
$env:EXTRA_OPTIONS="-v 2"
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

### git worktree

```
# 作成
git worktree add -b new-branch ../MoneyBook_new-branch master

# 既存ブランチの追加
git worktree add ../MoneyBook_new-branch new-branch


# 一覧表示
git worktree list

# 削除
git worktree remove ../MoneyBook_new-branch
```
