#!/bin/bash
# __init__.py Validation Script
#
# このスクリプトは、.pyファイルを含むディレクトリに__init__.pyが存在するか、
# また__init__.pyの内容が正しいかをチェックします。
# - 非空の__init__.pyを持つディレクトリ: 各モジュールのインポート漏れを検出
# - 空の__init__.pyを持つディレクトリ: ALLOW_EMPTY_INITに含まれているかを検証

set -e

SEARCH_DIRS=("moneybook" "config")

# 空の__init__.pyが許可されるディレクトリ一覧
# （意図的に空にすることが正当なディレクトリのみ列挙する）
ALLOW_EMPTY_INIT=(
    "moneybook"           # トップレベルDjangoアプリ
    "moneybook/migrations" # Djangoマイグレーション（標準パターン）
    "moneybook/middleware"  # 単一モジュール、直接インポートで使用
    "config"              # Djangoプロジェクトパッケージ
    "config/settings"     # DJANGO_SETTINGS_MODULE環境変数でimport
)

echo "__init__.py Validation"
echo "=================================================="

missing_files=()
unexpected_empty=()
missing_imports=()

is_allow_empty() {
    local dir="$1"
    for allowed in "${ALLOW_EMPTY_INIT[@]}"; do
        if [ "$dir" = "$allowed" ]; then
            return 0
        fi
    done
    return 1
}

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

        # __init__.pyが空の場合
        if [ ! -s "$init_py" ]; then
            # ALLOW_EMPTY_INITに含まれていない場合はエラー
            if ! is_allow_empty "$dir"; then
                unexpected_empty+=("$dir")
            fi
            continue
        fi

        # 非空の__init__.pyに対して各モジュールのインポート漏れをチェック
        while IFS= read -r py_file; do
            module=$(basename "$py_file" .py)
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

if [ ${#unexpected_empty[@]} -gt 0 ]; then
    echo "❌ エラー: 以下のディレクトリの__init__.pyが空です（ALLOW_EMPTY_INITへの追加またはインポートの記載が必要です）:"
    for dir in "${unexpected_empty[@]}"; do
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
