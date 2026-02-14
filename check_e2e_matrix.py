#!/usr/bin/env python
"""
E2E Matrix Validation Script

このスクリプトは、moneybook/e2eディレクトリ内のテストモジュールと
GitHub ActionsのMatrixで定義されているテストモジュールを比較し、
漏れがないかをチェックします。
"""

import os
import sys

import yaml


def get_e2e_test_modules():
    """
    moneybook/e2eディレクトリからテストモジュールを取得する。

    Returns:
        set: テストモジュール名のセット
    """
    e2e_dir = 'moneybook/e2e'
    test_modules = set()

    # 除外するファイル名
    exclude_files = {'__init__.py', 'base.py', '__pycache__'}

    for filename in os.listdir(e2e_dir):
        # ディレクトリや除外ファイルをスキップ
        if os.path.isdir(os.path.join(e2e_dir, filename)):
            continue
        if filename in exclude_files:
            continue

        # .pyファイルのみを対象とする
        if filename.endswith('.py'):
            module_name = filename[:-3]  # .pyを除去
            test_modules.add(module_name)

    return test_modules


def get_matrix_test_modules(workflow_file):
    """
    GitHub Actionsワークフローファイルからmatrix設定を取得する。

    Args:
        workflow_file: ワークフローファイルのパス

    Returns:
        set: matrix設定で定義されているテストモジュール名のセット
    """
    with open(workflow_file, 'r', encoding='utf-8') as f:
        workflow = yaml.safe_load(f)

    # e2eジョブのmatrix設定を取得
    e2e_job = workflow.get('jobs', {}).get('e2e', {})
    strategy = e2e_job.get('strategy', {})
    matrix = strategy.get('matrix', {})
    test_modules = matrix.get('test-module', [])

    return set(test_modules)


def main():
    """メイン処理"""
    workflow_file = '.github/workflows/python-lint-test.yml'

    print('E2E Matrix Validation')
    print('=' * 50)

    # E2Eテストモジュールを取得
    e2e_modules = get_e2e_test_modules()
    print(f'E2Eディレクトリ内のテストモジュール: {sorted(e2e_modules)}')

    # Matrix設定を取得
    matrix_modules = get_matrix_test_modules(workflow_file)
    print(f'Matrix設定で定義されているモジュール: {sorted(matrix_modules)}')

    # 差分をチェック
    missing_in_matrix = e2e_modules - matrix_modules
    extra_in_matrix = matrix_modules - e2e_modules

    print()
    if missing_in_matrix:
        print('❌ エラー: Matrix設定に以下のモジュールが不足しています:')
        for module in sorted(missing_in_matrix):
            print(f'  - {module}')
        print()
        print(f'以下のモジュールを {workflow_file} のmatrix.test-moduleに追加してください:')
        print(f'  test-module: {sorted(matrix_modules | missing_in_matrix)}')
        sys.exit(1)

    if extra_in_matrix:
        print('⚠️  警告: Matrix設定に以下の不要なモジュールが含まれています:')
        for module in sorted(extra_in_matrix):
            print(f'  - {module}')
        print()
        print('これらのモジュールは存在しないため、Matrix設定から削除してください。')
        sys.exit(1)

    print('✅ Matrix設定は正常です。すべてのE2Eテストモジュールが含まれています。')
    sys.exit(0)


if __name__ == '__main__':
    main()
