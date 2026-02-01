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
if sudo podman pod exists moneybook-pod; then
  sudo podman pod stop moneybook-pod
  sudo podman pod rm moneybook-pod
fi

# Create pod with shared network
echo "[INFO] Creating pod..."
sudo podman pod create --name moneybook-pod -p 8080:80

# Run DB migration
echo "[INFO] Running DB migration..."
sudo podman run --rm \
  --pod moneybook-pod \
  -e DB_NAME=$DB_NAME \
  -e DB_USER=$DB_USER \
  -e DB_PASS=$DB_PASS \
  -e DB_HOST=$DB_HOST \
  -e SECRET_KEY=$SECRET_KEY \
  moneybook_gunicorn:latest \
  python /MoneyBook/manage.py migrate --settings config.settings.prod

# Start gunicorn container in the pod
echo "[INFO] Starting gunicorn container..."
sudo podman run -d \
  --name moneybook_gunicorn \
  --pod moneybook-pod \
  --restart=always \
  -e DB_NAME=$DB_NAME \
  -e DB_USER=$DB_USER \
  -e DB_PASS=$DB_PASS \
  -e DB_HOST=$DB_HOST \
  -e ALLOWED_HOSTS=$ALLOWED_HOSTS \
  -e SECRET_KEY=$SECRET_KEY \
  moneybook_gunicorn:latest

# Wait for gunicorn to be ready
echo "[INFO] Waiting for gunicorn to be ready..."
sleep 5

# Start nginx container in the pod
echo "[INFO] Starting nginx container..."
sudo podman run -d \
  --name moneybook_nginx \
  --pod moneybook-pod \
  --restart=always \
  moneybook_nginx:latest

# Show pod and container status
echo "[INFO] Pod status:"
sudo podman pod ps

echo "[INFO] Container status:"
sudo podman ps --filter pod=moneybook-pod

# Delete old images
echo "[INFO] Cleaning up old images..."
sudo podman image prune -f

echo "[INFO] done."
