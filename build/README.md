# MoneyBook ビルド・デプロイ設定

このディレクトリには、MoneyBookアプリケーションのDocker/Kubernetes構成ファイルが含まれています。

## ファイル構成

### Dockerfiles

- **Dockerfile.gunicorn**: Djangoアプリケーション用のコンテナイメージ定義
  - ベースイメージ: `python:3.11-slim`
  - 起動時に静的ファイルを共有ボリュームにコピー
  - Gunicornでアプリケーションを実行

### Kubernetes/Podman設定

- **pod.yaml**: Podの定義ファイル
  - 2つのコンテナ: `gunicorn` (アプリ) と `nginx` (リバースプロキシ)
  - `nginx`は公式イメージ (`docker.io/nginx:alpine`) を使用
  - ConfigMapとemptyDirボリュームをマウント

- **configmap-nginx.yaml**: Nginx設定用ConfigMap
  - Nginx設定ファイル (`moneybook.conf`) を含む
  - `/static` パスへの静的ファイルの配信設定
  - Djangoアプリへのリバースプロキシ設定

### その他

- **nginx.conf**: Nginx設定ファイル（参考用）
  - configmap-nginx.yamlの内容と同じ
  - 直接マウントしないが、設定の参照用に保持

- **jenkins.sh**: CI/CDデプロイスクリプト
  - イメージのビルド
  - ConfigMapの作成
  - Podのデプロイ
  - データベースマイグレーション

## アーキテクチャ

```
┌─────────────────────────────────────────┐
│             Pod: moneybook-pod          │
│                                         │
│  ┌─────────────┐      ┌──────────────┐ │
│  │  gunicorn   │      │    nginx     │ │
│  │  container  │      │  container   │ │
│  │             │      │ (公式イメージ)│ │
│  │  :8081      │◄─────┤    :80       │ │
│  └──────┬──────┘      └──────┬───────┘ │
│         │                    │         │
│         │  ┌────────────┐    │         │
│         └─►│ emptyDir   │◄───┘         │
│            │ (static)   │              │
│            └────────────┘              │
│                                         │
│            ┌────────────┐              │
│            │ ConfigMap  │              │
│            │  (nginx    │──────────────┤
│            │   config)  │              │
│            └────────────┘              │
└─────────────────────────────────────────┘
```

### 静的ファイルの配信

1. `gunicorn`コンテナ起動時に`/MoneyBook/moneybook/static/*`を`/shared-static`にコピー
2. `nginx`コンテナは`/usr/share/nginx/html/static`に同じemptyDirボリュームをマウント
3. ブラウザからの`/static`リクエストはnginxが直接配信

### 設定ファイルの管理

- Nginx設定は`configmap-nginx.yaml`で管理
- ConfigMapを`/etc/nginx/conf.d`にマウント
- 設定変更時はConfigMapを更新して適用

## デプロイ手順

### 前提条件

以下の環境変数が設定されている必要があります:

```bash
PODMAN_USER    # Podmanを実行するユーザー
DB_NAME        # データベース名
DB_USER        # データベースユーザー
DB_PASS        # データベースパスワード
DB_HOST        # データベースホスト
HOST_NAME      # アプリケーションのホスト名
SECRET_KEY     # Django秘密鍵
```

### 手動デプロイ

```bash
# 1. イメージのビルド
podman build -t moneybook_gunicorn:latest -f build/Dockerfile.gunicorn .

# 2. ConfigMapの作成
podman play kube build/configmap-nginx.yaml

# 3. Podのデプロイ
envsubst < build/pod.yaml | podman play kube -

# 4. 確認
podman pod ps
podman ps --filter pod=moneybook-pod
```

### 自動デプロイ (Jenkins)

```bash
./build/jenkins.sh
```

## トラブルシューティング

### 静的ファイルが表示されない

```bash
# gunicornコンテナのログを確認
podman logs moneybook-pod-gunicorn

# "Copying static files to shared volume..." が表示されているか確認
```

### Nginx設定エラー

```bash
# nginxコンテナのログを確認
podman logs moneybook-pod-nginx

# ConfigMapが正しくマウントされているか確認
podman exec -it moneybook-pod-nginx cat /etc/nginx/conf.d/moneybook.conf
```

### Podが起動しない

```bash
# Pod全体の状態を確認
podman pod ps

# 詳細なログを確認
podman pod logs moneybook-pod
```

## 変更履歴

### 2026-02-15: Docker構成の整理

- **変更前**: カスタムnginx Dockerイメージを使用
- **変更後**: 公式nginx:alpineイメージを使用
- **理由**: 
  - イメージビルドの簡素化
  - メンテナンス負荷の軽減
  - ConfigMapによる設定の柔軟な管理

### 主な変更点

1. `Dockerfile.nginx`を削除
2. `configmap-nginx.yaml`を追加（Nginx設定用）
3. `pod.yaml`を更新（公式nginx、ConfigMap、emptyDirボリューム）
4. `Dockerfile.gunicorn`を更新（静的ファイルコピー機能追加）
5. `jenkins.sh`を更新（nginxビルド削除、ConfigMap作成追加）
