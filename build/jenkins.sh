#!/usr/bin/env bash
set -euo pipefail

# MoneyBookデプロイスクリプト

# リポジトリルートの取得
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# デプロイ先ディレクトリ
DEPLOY_DIR="/home/pluto/programs/Moneybook"

echo "デプロイ開始"

# 安全性チェック
if [ -z "${DEPLOY_DIR}" ] || [ "${DEPLOY_DIR}" = "/" ]; then
    echo "エラー: デプロイ先が不正です"
    exit 1
fi

# デプロイ先ディレクトリを作成
sudo mkdir -p "${DEPLOY_DIR}"

# ファイルを同期
rsync -a --delete \
    --exclude='.git/' \
    --exclude='.github/' \
    --exclude='.gitignore' \
    "${REPO_ROOT}/" "${DEPLOY_DIR}/"

# サービスを再起動
sudo systemctl restart moneybook.service

# ステータスを表示
sudo systemctl --no-pager --full status moneybook.service || true

echo "デプロイ完了"
