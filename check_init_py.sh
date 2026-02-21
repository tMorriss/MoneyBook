#!/bin/bash
# __init__.py Validation Script
#
# このスクリプトは、.pyファイルを含むディレクトリに__init__.pyが存在するか、
# また非空の__init__.pyを持つディレクトリで各モジュールのインポートが
# 漏れていないかをチェックします。

set -e

SEARCH_DIRS=("moneybook" "config")

echo "__init__.py Validation"
echo "=================================================="

missing_files=()
missing_imports=()

for base_dir in "${SEARCH_DIRS[@]}"; do
    # .pyファイル（__init__.py以外）を含むディレクトリを検索
    while IFS= read -r dir; do
        py_files=$(find "$dir" -maxdepth 1 -name "*.py" ! -name "__init__.py" 2>/dev/null)
        if [ -z "$py_files" ]; then
            continue
        fi

        init_py="$dir/__init__.py"

        # __init__.pyの存在チェック
        if [ ! -f "$init_py" ]; then
            missing_files+=("$dir")
            continue
        fi

        # __init__.pyが空の場合はインポートチェックをスキップ
        if [ ! -s "$init_py" ]; then
            continue
        fi

        # 非空の__init__.pyに対して各モジュールのインポート漏れをチェック
        # （base.pyはヘルパークラス用のため除外）
        while IFS= read -r py_file; do
            module=$(basename "$py_file" .py)
            if [ "$module" = "base" ]; then
                continue
            fi
            if ! grep -q "from \.$module " "$init_py" && ! grep -q "from \.$module$" "$init_py"; then
                missing_imports+=("$init_py: $module が未インポート")
            fi
        done < <(find "$dir" -maxdepth 1 -name "*.py" ! -name "__init__.py" | sort)
    done < <(find "$base_dir" -type d | sort)
done

echo "チェック対象ディレクトリ: ${SEARCH_DIRS[*]}"
echo

exit_code=0

if [ ${#missing_files[@]} -gt 0 ]; then
    echo "❌ エラー: 以下のディレクトリに__init__.pyが見つかりません:"
    for dir in "${missing_files[@]}"; do
        echo "  - $dir"
    done
    exit_code=1
fi

if [ ${#missing_imports[@]} -gt 0 ]; then
    echo "❌ エラー: 以下のモジュールが__init__.pyにインポートされていません:"
    for item in "${missing_imports[@]}"; do
        echo "  - $item"
    done
    exit_code=1
fi

if [ $exit_code -eq 0 ]; then
    echo "✅ すべてのPythonパッケージディレクトリの__init__.pyに問題はありません。"
fi

exit $exit_code
