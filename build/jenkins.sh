#!/usr/bin/env bash
set -euo pipefail

# 最新コミットメッセージに[skip ci]が含まれているかチェック
COMMIT_MESSAGE=$(git log -1 --pretty=%B)
if echo "$COMMIT_MESSAGE" | grep -q "\[skip ci\]"; then
  echo "[INFO] Commit message contains [skip ci]. Skipping deployment."
  exit 0
fi

# 必須環境変数のチェック
for VAR in PODMAN_USER DB_NAME DB_USER DB_PASS DB_HOST HOST_NAME SECRET_KEY; do
  if [ -z "${!VAR:-}" ]; then
    echo "[ERROR] Required environment variables are not set."
    echo "Please set: PODMAN_USER, DB_NAME, DB_USER, DB_PASS, DB_HOST, HOST_NAME, SECRET_KEY"
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
sudo -u "$PODMAN_USER" podman pull python:3.11-slim
sudo -u "$PODMAN_USER" podman pull nginx:alpine

# sed -i 's/DEBUG = False/DEBUG = True/' config/settings/prod.py

# イメージのビルド
echo "[INFO] Building images..."
sudo -u "$PODMAN_USER" podman build \
  --build-arg STATIC_VERSION=$STATIC_VERSION \
  -t moneybook_gunicorn:$BUILD_TAG \
  -f build/Dockerfile.gunicorn .
sudo -u "$PODMAN_USER" podman build \
  --build-arg STATIC_VERSION=$STATIC_VERSION \
  --build-arg GUNICORN_IMAGE=moneybook_gunicorn:$BUILD_TAG \
  -t moneybook_nginx:$BUILD_TAG \
  -f build/Dockerfile.nginx .

# 既存のPodが存在する場合は停止・削除
echo "[INFO] Stopping existing pod..."
sudo -u "$PODMAN_USER" podman play kube --down build/pod.yaml || true

# DBマイグレーション実行
echo "[INFO] Running DB migration..."
sudo -u "$PODMAN_USER" podman run \
  --rm \
  --name moneybook_migration \
  -e DB_NAME=$DB_NAME \
  -e DB_USER=$DB_USER \
  -e DB_PASS=$DB_PASS \
  -e DB_HOST=$DB_HOST \
  -e SECRET_KEY=$SECRET_KEY \
  -e STATIC_VERSION=$STATIC_VERSION \
  moneybook_gunicorn:$BUILD_TAG \
  python /MoneyBook/manage.py migrate --settings config.settings.prod

# 環境変数を置換してPod定義YAMLを生成・起動
echo "[INFO] Generating pod configuration with environment variables..."
export BUILD_TAG=$BUILD_TAG
envsubst < build/pod.yaml | sudo -u "$PODMAN_USER" podman play kube -

# サービスの起動を待機
echo "[INFO] Waiting for services to be ready..."
sleep 5

# PodとコンテナのステータスをCLI表示
echo "[INFO] Pod status:"
sudo -u "$PODMAN_USER" podman pod ps

echo "[INFO] Container status:"
sudo -u "$PODMAN_USER" podman ps --filter pod=moneybook-pod

# 古いイメージの削除（moneybook関係のみ）
echo "[INFO] Cleaning up old moneybook images..."
# 現在のビルドタグ以外のmoneybookイメージを削除
sudo -u "$PODMAN_USER" podman images --filter "reference=localhost/moneybook_gunicorn" --format "{{.Tag}}" | \
  grep -v "^$BUILD_TAG$" | \
  xargs -r -I {} sudo -u "$PODMAN_USER" podman rmi localhost/moneybook_gunicorn:{} || true
sudo -u "$PODMAN_USER" podman images --filter "reference=localhost/moneybook_nginx" --format "{{.Tag}}" | \
  grep -v "^$BUILD_TAG$" | \
  xargs -r -I {} sudo -u "$PODMAN_USER" podman rmi localhost/moneybook_nginx:{} || true

echo "[INFO] done."
