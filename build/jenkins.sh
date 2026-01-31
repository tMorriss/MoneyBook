#!/usr/bin/env bash
set -euo pipefail

# Jenkins deployment script for MoneyBook
# This script deploys the repository contents to the target directory and restarts the service

# Determine the repository root directory (one level up from the script location)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Target deployment directory
DEPLOY_DIR="/home/pluto/programs/Moneybook"

echo "[INFO] Starting deployment process"
echo "[INFO] Repository root: ${REPO_ROOT}"
echo "[INFO] Deploy directory: ${DEPLOY_DIR}"

# Safety guard: Fail if DEPLOY_DIR is empty or root
if [ -z "${DEPLOY_DIR}" ] || [ "${DEPLOY_DIR}" = "/" ]; then
    echo "[ERROR] DEPLOY_DIR is empty or set to root directory. Refusing to continue."
    exit 1
fi

# Create deployment directory if it doesn't exist
echo "[INFO] Creating deployment directory (if needed)"
sudo mkdir -p "${DEPLOY_DIR}"

# Sync repository contents to deployment directory
echo "[INFO] Syncing files to deployment directory"
rsync -av --delete \
    --exclude='.git/' \
    --exclude='.github/' \
    --exclude='.gitignore' \
    "${REPO_ROOT}/" "${DEPLOY_DIR}/"

echo "[INFO] Deployment sync completed successfully"

# Restart the systemd service
echo "[INFO] Restarting moneybook.service"
sudo systemctl restart moneybook.service

# Print service status
echo "[INFO] Service status:"
sudo systemctl --no-pager --full status moneybook.service || true

echo "[INFO] Deployment completed successfully"
