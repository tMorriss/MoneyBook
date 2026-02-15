# テスト手順書

このドキュメントは、Docker/Kubernetes構成の変更を検証するための手順を説明します。

## 前提条件

以下がインストールされていること：
- Podman または Docker
- 必要な環境変数が設定されていること

## テスト環境の準備

```bash
# 環境変数の設定（例）
export PODMAN_USER=$(whoami)
export DB_NAME=moneybook_test
export DB_USER=testuser
export DB_PASS=testpass
export DB_HOST=localhost
export HOST_NAME=localhost
export SECRET_KEY=test-secret-key-for-testing-only
```

## テスト項目

### 1. YAML構文の検証

```bash
# ConfigMap YAMLの検証
python3 -c "import yaml; yaml.safe_load(open('build/configmap-nginx.yaml'))"
echo "✓ configmap-nginx.yaml is valid"

# Pod YAMLの検証
python3 -c "import yaml; yaml.safe_load(open('build/pod.yaml'))"
echo "✓ pod.yaml is valid"
```

**期待結果**: エラーなく完了すること

### 2. シェルスクリプト構文の検証

```bash
# jenkins.shの構文チェック
bash -n build/jenkins.sh
echo "✓ jenkins.sh has no syntax errors"

# shellcheckによる詳細チェック（利用可能な場合）
shellcheck build/jenkins.sh
echo "✓ No shellcheck issues"
```

**期待結果**: 構文エラーや警告がないこと

### 3. Dockerイメージのビルドテスト

```bash
# アプリケーションイメージのビルド
podman build -t moneybook_gunicorn:test -f build/Dockerfile.gunicorn .
```

**期待結果**: 
- ビルドが成功すること
- エラーメッセージが出ないこと
- `/start.sh`スクリプトがイメージに含まれていること

**確認方法**:
```bash
podman run --rm moneybook_gunicorn:test cat /start.sh
# start.shの内容が表示されればOK
```

### 4. ConfigMapの作成テスト

```bash
# ConfigMapの作成（Podman）
podman play kube build/configmap-nginx.yaml

# ConfigMapの確認
podman volume ls | grep moneybook-nginx-config
```

**期待結果**: ConfigMapが作成されること

### 5. nginx公式イメージのpullテスト

```bash
# nginx公式イメージのpull
podman pull docker.io/nginx:alpine
```

**期待結果**: イメージが正常にダウンロードされること

### 6. Pod定義の検証

```bash
# Pod YAMLの環境変数置換
envsubst < build/pod.yaml > /tmp/pod-generated.yaml

# 生成されたYAMLの確認
cat /tmp/pod-generated.yaml

# YAMLの検証
python3 -c "import yaml; yaml.safe_load(open('/tmp/pod-generated.yaml'))"
```

**期待結果**: 
- 環境変数が正しく置換されること
- 生成されたYAMLが有効であること
- 以下の要素が含まれていること：
  - volumes: nginx-config (configMap), static-files (emptyDir)
  - gunicornコンテナのvolumeMount: /shared-static
  - nginxコンテナのvolumeMount: /etc/nginx/conf.d, /usr/share/nginx/html/static

### 7. 統合テスト（オプション）

完全なデプロイテストを実行する場合：

```bash
# jenkins.shの実行（実際の環境がある場合のみ）
# 注意: これは実際のデータベースとPodmanが必要です
./build/jenkins.sh
```

**期待結果**:
1. イメージビルドが成功
2. ConfigMapが作成される
3. 既存Podが停止される
4. DBマイグレーションが実行される
5. 新しいPodが起動する
6. gunicornコンテナで「Copying static files to shared volume...」が表示される
7. nginxコンテナが正常に起動する

**確認方法**:
```bash
# Podのステータス確認
podman pod ps

# コンテナのステータス確認
podman ps --filter pod=moneybook-pod

# gunicornログの確認（静的ファイルコピーメッセージ）
podman logs moneybook-pod-gunicorn | grep "Copying static files"

# nginxログの確認
podman logs moneybook-pod-nginx

# nginx設定の確認
podman exec -it moneybook-pod-nginx cat /etc/nginx/conf.d/moneybook.conf

# 静的ファイルの確認
podman exec -it moneybook-pod-nginx ls -la /usr/share/nginx/html/static
```

### 8. 動作確認（統合テスト実行時）

```bash
# アプリケーションへのアクセステスト
curl -I http://localhost:8081/

# 静的ファイルへのアクセステスト
curl -I http://localhost:8081/static/style.css
```

**期待結果**:
- HTTP 200 または 302が返ること
- 静的ファイルが正常に配信されること

## トラブルシューティング

### 静的ファイルが見つからない

```bash
# gunicornコンテナ内の静的ファイル確認
podman exec -it moneybook-pod-gunicorn ls -la /MoneyBook/moneybook/static

# 共有ボリューム内の静的ファイル確認
podman exec -it moneybook-pod-gunicorn ls -la /shared-static

# nginxコンテナ内の静的ファイル確認
podman exec -it moneybook-pod-nginx ls -la /usr/share/nginx/html/static
```

### ConfigMapがマウントされない

```bash
# nginxコンテナ内の設定ファイル確認
podman exec -it moneybook-pod-nginx ls -la /etc/nginx/conf.d

# 設定ファイルの内容確認
podman exec -it moneybook-pod-nginx cat /etc/nginx/conf.d/moneybook.conf
```

### Podが起動しない

```bash
# Pod全体のログ確認
podman pod logs moneybook-pod

# 個別コンテナのログ確認
podman logs moneybook-pod-gunicorn
podman logs moneybook-pod-nginx
```

## クリーンアップ

テスト後の後片付け：

```bash
# Podの停止・削除
podman play kube --down build/pod.yaml

# テストイメージの削除
podman rmi moneybook_gunicorn:test

# 未使用イメージの削除
podman image prune -f
```

## テスト結果チェックリスト

- [ ] YAML構文検証: 合格
- [ ] シェルスクリプト構文検証: 合格
- [ ] Dockerイメージビルド: 成功
- [ ] ConfigMap作成: 成功
- [ ] nginx公式イメージpull: 成功
- [ ] Pod定義検証: 合格
- [ ] （オプション）統合テスト: 成功
- [ ] （オプション）動作確認: 成功

すべてのチェック項目が合格であれば、変更は正常に動作します。
