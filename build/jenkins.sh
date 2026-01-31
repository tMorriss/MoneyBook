#!/usr/bin/env bash
set -euo pipefail

DEPLOY_DIR="/home/pluto/programs/Moneybook"
SERVICE_NAME="moneybook.service"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "[INFO] repo_root: ${REPO_ROOT}"
echo "[INFO] deploy_dir: ${DEPLOY_DIR}"

# 誤爆防止
if [[ -z "${DEPLOY_DIR}" || "${DEPLOY_DIR}" == "/" ]]; then
  echo "[ERROR] DEPLOY_DIR is invalid: '${DEPLOY_DIR}'"
  exit 1
fi

sudo mkdir -p "${DEPLOY_DIR}"

# 配布先をリポジトリと完全一致にする（不要ファイルも削除）
sudo rsync -a --delete \
  --exclude ".git/" \
  --exclude ".github/" \
  --exclude ".gitignore" \
  "${REPO_ROOT}/" "${DEPLOY_DIR}/"

echo "[INFO] restarting service: ${SERVICE_NAME}"
sudo systemctl restart "${SERVICE_NAME}"

echo "[INFO] service status:"
sudo systemctl --no-pager --full status "${SERVICE_NAME}" || true

echo "[INFO] done."
