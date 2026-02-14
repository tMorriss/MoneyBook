#!/usr/bin/env python
"""
Pythonパッケージディレクトリに__init__.pyファイルが存在するかチェックするスクリプト。

このスクリプトは、Pythonファイル(.py)を含むディレクトリを検索し、
それらがPythonパッケージとして適切に__init__.pyを持っているかを確認します。
"""
import os
import sys
from pathlib import Path


def is_python_package_directory(directory: Path) -> bool:
    """
    ディレクトリがPythonパッケージであるべきかを判定する。

    以下の条件を満たす場合、Pythonパッケージとみなす：
    - ディレクトリ直下にPythonファイル(.py)が存在する、または
    - サブディレクトリに__init__.pyが存在する（既にパッケージ化されたサブディレクトリ）

    Args:
        directory: チェック対象のディレクトリパス

    Returns:
        Pythonパッケージであるべき場合True
    """
    if not directory.is_dir():
        return False

    # 直下のPythonファイルをチェック
    python_files = list(directory.glob('*.py'))
    if python_files:
        # __init__.py以外のPythonファイルがある場合
        non_init_files = [f for f in python_files if f.name != '__init__.py']
        if non_init_files:
            return True

    # サブディレクトリに__init__.pyがある場合もパッケージとみなす
    for subdir in directory.iterdir():
        if subdir.is_dir() and (subdir / '__init__.py').exists():
            return True

    return False


def check_init_py_files(root_dir: Path, exclude_dirs: set) -> list:
    """
    __init__.pyが欠落しているディレクトリを検出する。

    Args:
        root_dir: 検索を開始するルートディレクトリ
        exclude_dirs: 除外するディレクトリ名のセット

    Returns:
        __init__.pyが欠落しているディレクトリパスのリスト
    """
    missing_init_dirs = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 除外ディレクトリをスキップ
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]

        current_dir = Path(dirpath)

        # ルートディレクトリ自体はスキップ
        if current_dir == root_dir:
            continue

        # Pythonパッケージとして扱うべきディレクトリかチェック
        if is_python_package_directory(current_dir):
            init_file = current_dir / '__init__.py'
            if not init_file.exists():
                # ルートディレクトリからの相対パスで記録
                relative_path = current_dir.relative_to(root_dir)
                missing_init_dirs.append(str(relative_path))

    return missing_init_dirs


def main():
    """メイン処理"""
    # プロジェクトルートディレクトリ
    root_dir = Path(__file__).parent

    # 除外するディレクトリ
    exclude_dirs = {
        '.git',
        '.github',
        '.vscode',
        '__pycache__',
        '.pytest_cache',
        '.mypy_cache',
        'build',
        'dist',
        '*.egg-info',
        'node_modules',
        '.venv',
        'venv',
        'env',
        'static',  # 静的ファイルディレクトリ
        'templates',  # テンプレートディレクトリ
        'fixtures',  # フィクスチャディレクトリ
        'migrations',  # Djangoマイグレーションは自動生成されるため除外
    }

    # チェック実行
    missing_dirs = check_init_py_files(root_dir, exclude_dirs)

    if missing_dirs:
        print('Error: 以下のディレクトリに__init__.pyが欠落しています:')
        print()
        for dir_path in sorted(missing_dirs):
            print(f'  - {dir_path}')
        print()
        print('各ディレクトリに__init__.pyファイルを作成してください。')
        sys.exit(1)
    else:
        print('Success: すべてのPythonパッケージディレクトリに__init__.pyが存在します。')
        sys.exit(0)


if __name__ == '__main__':
    main()
