#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "[INFO] repo_root: ${REPO_ROOT}"

cd "${REPO_ROOT}"

# Pull base images
echo "[INFO] Pulling base images..."
sudo docker pull python:3.13-slim
sudo docker pull nginx:alpine

# Build docker images
echo "[INFO] Building docker images..."
sudo docker-compose build

# Run DB migration
echo "[INFO] Running DB migration..."
sudo docker-compose run --rm gunicorn \
  python /MoneyBook/manage.py migrate --settings config.settings.prod

# Stop and remove existing containers
echo "[INFO] Stopping existing containers..."
sudo docker-compose down

# Start containers
echo "[INFO] Starting containers..."
sudo docker-compose up -d

# Show container status
echo "[INFO] Container status:"
sudo docker-compose ps

# Delete old images
echo "[INFO] Cleaning up old images..."
sudo docker image prune -f

echo "[INFO] done."
