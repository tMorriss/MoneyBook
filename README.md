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
$ tox -e lint
```

## 単体テスト

[![codecov](https://codecov.io/gh/tMorriss/MoneyBook/branch/master/graph/badge.svg?token=E522OPRLRM)](https://codecov.io/gh/tMorriss/MoneyBook)

```
$ tox -e unittest
```

## e2e テスト

```
# 全てのe2eテストを実行
$ tox -e e2e

# 特定のテストモジュールを実行（例：indexモジュールのみ）
$ TEST_MODULE=moneybook.e2e.index tox -e e2e
```

### ヘッドレスモード

e2e テストはデフォルトでヘッドレスモードで実行されます。ブラウザを表示して実行する場合は、環境変数`HEADLESS=0`を設定してください。

```
# mac
$ HEADLESS=0 tox -e e2e
# windows
$ $env:HEADLESS="0"; tox -e e2e
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

# 一覧表示
git worktree list

# 削除
git worktree remove ../MoneyBook_new-branch
```