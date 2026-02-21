#!/bin/bash
# __init__.py Validation Script
#
# このスクリプトは、.pyファイルを含むディレクトリに
# __init__.pyが存在するかをチェックします。

set -e

SEARCH_DIRS=("moneybook" "config")

echo "__init__.py Validation"
echo "=================================================="

missing=()

for base_dir in "${SEARCH_DIRS[@]}"; do
    # .pyファイル（__init__.py以外）を含むディレクトリを検索
    while IFS= read -r dir; do
        py_files=$(find "$dir" -maxdepth 1 -name "*.py" ! -name "__init__.py" 2>/dev/null)
        if [ -n "$py_files" ] && [ ! -f "$dir/__init__.py" ]; then
            missing+=("$dir")
        fi
    done < <(find "$base_dir" -type d | sort)
done

echo "チェック対象ディレクトリ: ${SEARCH_DIRS[*]}"
echo

if [ ${#missing[@]} -eq 0 ]; then
    echo "✅ すべてのPythonパッケージディレクトリに__init__.pyが存在します。"
    exit 0
else
    echo "❌ エラー: 以下のディレクトリに__init__.pyが見つかりません:"
    for dir in "${missing[@]}"; do
        echo "  - $dir"
    done
    exit 1
fi
