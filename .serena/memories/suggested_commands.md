# よく使うコマンド（Windows想定）
## 環境構築
- `python -m venv .venv`
- `Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process`
- `.\.venv\Scripts\activate`
- `pip install -r requirements/requirements.txt`
- `pip install -r requirements/requirements_test.txt`
- `pip install -r requirements/requirements_lint.txt`
- `pip install -r requirements/requirements_dev.txt`

## 実行
- `python manage.py migrate`
- `python manage.py runserver`

## 品質チェック
- `tox -e lint`
- `tox -e unittest`
- `tox -e e2e`
- `tox`

## e2e補助
- `$env:TEST_MODULE="moneybook.e2e.index"; tox -e e2e`
- `$env:HEADLESS="0"; tox -e e2e`

## Git/シェル基本（PowerShell）
- `Get-ChildItem` / `Set-Location` / `Select-String`
- `git status` / `git fetch` / `git merge origin/master`
