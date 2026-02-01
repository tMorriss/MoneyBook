#!/usr/bin/env bash
set -euo pipefail

# 必須環境変数のチェック
for VAR in PODMAN_USER DB_NAME DB_USER DB_PASS DB_HOST ALLOWED_HOSTS SECRET_KEY; do
  if [ -z "${!VAR:-}" ]; then
    echo "[ERROR] Required environment variables are not set."
    echo "Please set: PODMAN_USER, DB_NAME, DB_USER, DB_PASS, DB_HOST, ALLOWED_HOSTS, SECRET_KEY"
    exit 1
  fi
done

# ベースイメージのpull
echo "[INFO] Pulling base images..."
sudo -u "$PODMAN_USER" podman pull python:3.11-slim
sudo -u "$PODMAN_USER" podman pull nginx:alpine

# イメージのビルド
echo "[INFO] Building images..."
sudo -u "$PODMAN_USER" podman build -t moneybook_gunicorn:latest -f build/Dockerfile.gunicorn .
sudo -u "$PODMAN_USER" podman build -t moneybook_nginx:latest -f build/Dockerfile.nginx .

# 既存のPodが存在する場合は停止・削除
echo "[INFO] Stopping existing pod..."
sudo -u "$PODMAN_USER" podman play kube --down build/pod.yaml || true

# DBマイグレーション実行
echo "[INFO] Running DB migration..."
sudo -u "$PODMAN_USER" podman run --rm \
  -e DB_NAME=$DB_NAME \
  -e DB_USER=$DB_USER \
  -e DB_PASS=$DB_PASS \
  -e DB_HOST=$DB_HOST \
  -e SECRET_KEY=$SECRET_KEY \
  moneybook_gunicorn:latest \
  python /MoneyBook/manage.py migrate --settings config.settings.prod

# 環境変数を置換してPod定義YAMLを生成・起動
echo "[INFO] Generating pod configuration with environment variables..."
envsubst < build/pod.yaml | sudo -u "$PODMAN_USER" podman play kube -

# サービスの起動を待機
echo "[INFO] Waiting for services to be ready..."
sleep 5

# PodとコンテナのステータスをCLI表示
echo "[INFO] Pod status:"
sudo -u "$PODMAN_USER" podman pod ps

echo "[INFO] Container status:"
sudo -u "$PODMAN_USER" podman ps --filter pod=moneybook-pod

# 古いイメージの削除
echo "[INFO] Cleaning up old images..."
sudo -u "$PODMAN_USER" podman image prune -f

echo "[INFO] done."
