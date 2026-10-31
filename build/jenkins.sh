#!/usr/bin/env bash
set -euo pipefail

# 最新コミットメッセージに[skip ci]が含まれているかチェック
# GitHub push トリガー（新規コミット）の場合のみ適用し、手動実行時などはデプロイを継続する
COMMIT_MESSAGE=$(git log -1 --pretty=%B)
if grep -qiE "\\[(skip ci|ci skip)\\]" <<< "$COMMIT_MESSAGE"; then
  if [ "${GIT_COMMIT:-}" != "${GIT_PREVIOUS_COMMIT:-}" ]; then
    echo "[INFO] Commit message contains [skip ci] and it's a new commit. Skipping deployment."
    exit 0
  fi
  echo "[INFO] Commit message contains [skip ci] but it's not a new commit. Proceeding with deployment."
fi

# 必須環境変数のチェック
for VAR in DB_NAME DB_USER DB_PASS DB_HOST HOST_NAME SECRET_KEY; do
  if [ -z "${!VAR:-}" ]; then
    echo "[ERROR] Required environment variables are not set."
    echo "Please set: DB_NAME, DB_USER, DB_PASS, DB_HOST, HOST_NAME, SECRET_KEY"
    exit 1
  fi
done

# ビルドタグの生成（ランダム値）
BUILD_TAG=$(date +%Y%m%d%H%M%S)-$(head -c 8 /dev/urandom | base64 | tr -dc 'a-z0-9' | head -c 8)
export STATIC_VERSION=$BUILD_TAG
echo "[INFO] Build tag: $BUILD_TAG"
echo "[INFO] Static version: $STATIC_VERSION"

# ベースイメージのpull
echo "[INFO] Pulling base images..."
podman pull python:3.12-slim
podman pull nginx:alpine

# イメージのビルド
echo "[INFO] Building images..."
podman build \
  --build-arg STATIC_VERSION=$STATIC_VERSION \
  -t moneybook_gunicorn:$BUILD_TAG \
  -f build/Dockerfile.gunicorn .
podman build \
  --build-arg STATIC_VERSION=$STATIC_VERSION \
  --build-arg GUNICORN_IMAGE=moneybook_gunicorn:$BUILD_TAG \
  -t moneybook_nginx:$BUILD_TAG \
  -f build/Dockerfile.nginx .

# Podman Secrets の更新関数
create_or_update_secret() {
  local name="$1"
  local value="$2"
  echo "[INFO] Updating Podman secret: $name"
  if podman secret exists "$name"; then
    podman secret rm "$name"
  fi
  echo -n "$value" | podman secret create "$name" -
}

# 秘匿情報を Podman Secrets に登録
create_or_update_secret "moneybook_db_name" "$DB_NAME"
create_or_update_secret "moneybook_db_user" "$DB_USER"
create_or_update_secret "moneybook_db_pass" "$DB_PASS"
create_or_update_secret "moneybook_db_host" "$DB_HOST"
create_or_update_secret "moneybook_host_name" "$HOST_NAME"
create_or_update_secret "moneybook_secret_key" "$SECRET_KEY"

# DBマイグレーション実行
echo "[INFO] Running DB migration..."
podman run \
  --rm \
  --name moneybook_migration \
  --secret moneybook_db_name,type=env,target=DB_NAME \
  --secret moneybook_db_user,type=env,target=DB_USER \
  --secret moneybook_db_pass,type=env,target=DB_PASS \
  --secret moneybook_db_host,type=env,target=DB_HOST \
  --secret moneybook_host_name,type=env,target=HOST_NAME \
  --secret moneybook_secret_key,type=env,target=SECRET_KEY \
  -e STATIC_VERSION=$STATIC_VERSION \
  moneybook_gunicorn:$BUILD_TAG \
  python /MoneyBook/manage.py migrate --settings config.settings.prod

# Lingerの設定（ホスト再起動時の自動起動を許可）
SCRIPT_USER=$(id -un)
echo "[INFO] Enabling linger for $SCRIPT_USER..."
loginctl enable-linger "$SCRIPT_USER" || true

# Quadlet ユニットファイルの配置（プロジェクト用サブディレクトリに配置）
QUADLET_DIR="$HOME/.config/containers/systemd/moneybook"
echo "[INFO] Deploying Quadlet unit files to $QUADLET_DIR..."
mkdir -p "$QUADLET_DIR"

# 配置先サブディレクトリ内の既存ユニットファイルをクリーンアップ（旧ファイルの残留防止）
rm -rf "${QUADLET_DIR:?}"/*

export BUILD_TAG=$BUILD_TAG
envsubst '$BUILD_TAG $STATIC_VERSION' < build/quadlet/moneybook.pod.template > "$QUADLET_DIR/moneybook.pod"
envsubst '$BUILD_TAG $STATIC_VERSION' < build/quadlet/moneybook-gunicorn.container.template > "$QUADLET_DIR/moneybook-gunicorn.container"
envsubst '$BUILD_TAG $STATIC_VERSION' < build/quadlet/moneybook-nginx.container.template > "$QUADLET_DIR/moneybook-nginx.container"

# systemd ユーザーデーモンのリロードと Quadlet サービスの再起動
SCRIPT_UID=$(id -u)
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$SCRIPT_UID}"
echo "[INFO] Reloading systemd user daemon and restarting Quadlet services..."
systemctl --user daemon-reload
systemctl --user restart moneybook-pod.service

# サービスの起動を待機
echo "[INFO] Waiting for services to be ready..."
sleep 5

# Podとコンテナのステータスを表示
echo "[INFO] Pod status:"
podman pod ps

echo "[INFO] Container status:"
podman ps --filter pod=moneybook-pod

# 古いイメージの削除（moneybook関係のみ）
echo "[INFO] Cleaning up old moneybook images..."
podman images --filter "reference=localhost/moneybook_gunicorn" --format "{{.Tag}}" | \
  grep -v "^$BUILD_TAG$" | \
  xargs -r -I {} podman rmi localhost/moneybook_gunicorn:{} || true
podman images --filter "reference=localhost/moneybook_nginx" --format "{{.Tag}}" | \
  grep -v "^$BUILD_TAG$" | \
  xargs -r -I {} podman rmi localhost/moneybook_nginx:{} || true

# 未使用イメージの削除
echo "[INFO] Pruning unused images..."
podman image prune -f || true

echo "[INFO] done."
