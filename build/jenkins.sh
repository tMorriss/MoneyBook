#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

# ベースイメージのpull
echo "[INFO] Pulling base images..."
sudo podman pull python:3.10-slim
sudo podman pull nginx:alpine

# イメージのビルド
echo "[INFO] Building images..."
sudo podman build -t moneybook_gunicorn:latest -f build/Dockerfile.gunicorn .
sudo podman build -t moneybook_nginx:latest -f build/Dockerfile.nginx .

# 既存のPodが存在する場合は停止・削除
echo "[INFO] Stopping existing pod..."
sudo podman play kube --down build/pod.yaml || true

# DBマイグレーション実行
echo "[INFO] Running DB migration..."
sudo podman run --rm \
  -e DB_NAME=$DB_NAME \
  -e DB_USER=$DB_USER \
  -e DB_PASS=$DB_PASS \
  -e DB_HOST=$DB_HOST \
  -e SECRET_KEY=$SECRET_KEY \
  moneybook_gunicorn:latest \
  python /MoneyBook/manage.py migrate --settings config.settings.prod

# 環境変数を置換してPod定義YAMLを生成・起動
echo "[INFO] Generating pod configuration with environment variables..."
envsubst < build/pod.yaml | sudo podman play kube -

# サービスの起動を待機
echo "[INFO] Waiting for services to be ready..."
sleep 5

# PodとコンテナのステータスをCLI表示
echo "[INFO] Pod status:"
sudo podman pod ps

echo "[INFO] Container status:"
sudo podman ps --filter pod=moneybook-pod

# 古いイメージの削除
echo "[INFO] Cleaning up old images..."
sudo podman image prune -f

echo "[INFO] done."
