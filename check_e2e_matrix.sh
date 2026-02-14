#!/bin/bash
# E2E Matrix Validation Script
#
# このスクリプトは、moneybook/e2eディレクトリ内のテストモジュールと
# GitHub ActionsのMatrixで定義されているテストモジュールを比較し、
# 漏れがないかをチェックします。

set -e

WORKFLOW_FILE=".github/workflows/python-lint-test.yml"
E2E_DIR="moneybook/e2e"

echo "E2E Matrix Validation"
echo "=================================================="

# E2Eディレクトリ内のテストモジュールを取得
# 除外するファイル: __init__.py, base.py
e2e_modules=()
for file in "$E2E_DIR"/*.py; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        module_name="${filename%.py}"
        
        # 除外ファイルをスキップ
        if [ "$module_name" != "__init__" ] && [ "$module_name" != "base" ]; then
            e2e_modules+=("$module_name")
        fi
    fi
done

# ソートして表示
IFS=$'\n' sorted_e2e=($(sort <<<"${e2e_modules[*]}"))
unset IFS

echo -n "E2Eディレクトリ内のテストモジュール: ["
for i in "${!sorted_e2e[@]}"; do
    if [ $i -gt 0 ]; then
        echo -n ", "
    fi
    echo -n "'${sorted_e2e[$i]}'"
done
echo "]"

# Matrix設定からテストモジュールを取得
# yqを使用してYAMLをパース
matrix_modules_json=$(yq eval '.jobs.e2e.strategy.matrix.test-module' "$WORKFLOW_FILE" -o=json)
matrix_modules=()
while IFS= read -r module; do
    matrix_modules+=("$module")
done < <(echo "$matrix_modules_json" | jq -r '.[]')

# ソートして表示
IFS=$'\n' sorted_matrix=($(sort <<<"${matrix_modules[*]}"))
unset IFS

echo -n "Matrix設定で定義されているモジュール: ["
for i in "${!sorted_matrix[@]}"; do
    if [ $i -gt 0 ]; then
        echo -n ", "
    fi
    echo -n "'${sorted_matrix[$i]}'"
done
echo "]"
echo

# 差分をチェック
missing_in_matrix=()
for module in "${e2e_modules[@]}"; do
    found=0
    for matrix_module in "${matrix_modules[@]}"; do
        if [ "$module" = "$matrix_module" ]; then
            found=1
            break
        fi
    done
    if [ $found -eq 0 ]; then
        missing_in_matrix+=("$module")
    fi
done

extra_in_matrix=()
for matrix_module in "${matrix_modules[@]}"; do
    found=0
    for module in "${e2e_modules[@]}"; do
        if [ "$matrix_module" = "$module" ]; then
            found=1
            break
        fi
    done
    if [ $found -eq 0 ]; then
        extra_in_matrix+=("$matrix_module")
    fi
done

# エラーチェック
if [ ${#missing_in_matrix[@]} -gt 0 ]; then
    echo "❌ エラー: Matrix設定に以下のモジュールが不足しています:"
    IFS=$'\n' sorted_missing=($(sort <<<"${missing_in_matrix[*]}"))
    unset IFS
    for module in "${sorted_missing[@]}"; do
        echo "  - $module"
    done
    echo
    
    # 全てのモジュールを結合してソート
    all_modules=("${matrix_modules[@]}" "${missing_in_matrix[@]}")
    IFS=$'\n' sorted_all=($(sort <<<"${all_modules[*]}"))
    unset IFS
    
    echo "以下のモジュールを $WORKFLOW_FILE のmatrix.test-moduleに追加してください:"
    echo -n "  test-module: ["
    for i in "${!sorted_all[@]}"; do
        if [ $i -gt 0 ]; then
            echo -n ", "
        fi
        echo -n "'${sorted_all[$i]}'"
    done
    echo "]"
    exit 1
fi

if [ ${#extra_in_matrix[@]} -gt 0 ]; then
    echo "⚠️  警告: Matrix設定に以下の不要なモジュールが含まれています:"
    IFS=$'\n' sorted_extra=($(sort <<<"${extra_in_matrix[*]}"))
    unset IFS
    for module in "${sorted_extra[@]}"; do
        echo "  - $module"
    done
    echo
    echo "これらのモジュールは存在しないため、Matrix設定から削除してください。"
    exit 1
fi

echo "✅ Matrix設定は正常です。すべてのE2Eテストモジュールが含まれています。"
exit 0
