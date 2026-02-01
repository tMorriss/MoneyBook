#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

# Pull base images
echo "[INFO] Pulling base images..."
sudo podman pull python:3.13-slim
sudo podman pull nginx:alpine

# Build images
echo "[INFO] Building images..."
sudo podman build -t moneybook_gunicorn:latest -f build/Dockerfile.gunicorn .
sudo podman build -t moneybook_nginx:latest -f build/Dockerfile.nginx .

# Stop and remove existing pod if it exists
echo "[INFO] Stopping existing pod..."
sudo podman play kube --down build/pod.yaml 2>/dev/null || true

# Run DB migration
echo "[INFO] Running DB migration..."
sudo podman run --rm \
  -e DB_NAME=$DB_NAME \
  -e DB_USER=$DB_USER \
  -e DB_PASS=$DB_PASS \
  -e DB_HOST=$DB_HOST \
  -e SECRET_KEY=$SECRET_KEY \
  moneybook_gunicorn:latest \
  python /MoneyBook/manage.py migrate --settings config.settings.prod

# Create pod YAML with environment variables substituted
echo "[INFO] Generating pod configuration with environment variables..."
envsubst < build/pod.yaml | sudo podman play kube -

# Wait for services to be ready
echo "[INFO] Waiting for services to be ready..."
sleep 5

# Show pod and container status
echo "[INFO] Pod status:"
sudo podman pod ps

echo "[INFO] Container status:"
sudo podman ps --filter pod=moneybook-pod

# Delete old images
echo "[INFO] Cleaning up old images..."
sudo podman image prune -f

echo "[INFO] done."
