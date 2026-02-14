#!/bin/bash
# E2E Matrix Validation Script
#
# このスクリプトは、moneybook/e2eディレクトリ内のテストモジュールと
# GitHub ActionsのMatrixで定義されているテストモジュールを比較し、
# 漏れがないかをチェックします。

set -e

WORKFLOW_FILE=".github/workflows/python-lint-test.yml"
E2E_DIR="moneybook/e2e"

echo "e2e Matrix Validation"
echo "=================================================="

# e2eディレクトリ内のテストモジュールを取得（カンマ+スペース区切り、ソート済み）
e2e_modules=$(grep -rl " def test_" "$E2E_DIR" 2>/dev/null | sed 's/moneybook\/e2e\///g' | sed 's/.py//g' | sort | paste -sd "," - | sed 's/,/, /g')

# Matrix設定からテストモジュールを取得（カンマ+スペース区切り、ソート済み）
matrix_modules=$(yq eval '.jobs.e2e.strategy.matrix.test-module | sort | join(", ")' "$WORKFLOW_FILE")

echo "e2eディレクトリ: $e2e_modules"
echo "Matrix設定: $matrix_modules"
echo

# 文字列比較
if [ "$e2e_modules" = "$matrix_modules" ]; then
    echo "✅ Matrix設定は正常です。"
    exit 0
else
    echo "❌ エラー: 差分があります。"
    exit 1
fi


