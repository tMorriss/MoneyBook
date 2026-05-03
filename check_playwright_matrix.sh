#!/bin/bash
# Playwright Matrix Validation Script
#
# このスクリプトは、moneybook/playwrightディレクトリ内のテストモジュールと
# GitHub ActionsのMatrixで定義されているテストモジュールを比較し、
# 漏れがないかをチェックします。

set -e

WORKFLOW_FILE=".github/workflows/ci.yml"
PLAYWRIGHT_DIR="moneybook/playwright"

echo "playwright Matrix Validation"
echo "=================================================="

# playwrightディレクトリ内のテストモジュールを取得（カンマ+スペース区切り、ソート済み）
playwright_modules=$(grep -rl " def test_" "$PLAYWRIGHT_DIR" 2>/dev/null | sed 's/moneybook\/playwright\///g' | sed 's/.py//g' | sort | paste -sd "," - | sed 's/,/, /g')

# Matrix設定からテストモジュールを取得（カンマ+スペース区切り、ソート済み）
matrix_modules=$(yq eval '.jobs.playwright.strategy.matrix.test-module | sort | join(", ")' "$WORKFLOW_FILE")

echo "playwrightディレクトリ: $playwright_modules"
echo "Matrix設定: $matrix_modules"
echo

# 文字列比較
if [ "$playwright_modules" = "$matrix_modules" ]; then
    echo "✅ Matrix設定は正常です。"
    exit 0
else
    echo "❌ エラー: 差分があります。"
    exit 1
fi
