# コーディング規約・設計慣習
- Python/Djangoプロジェクト。ビューは機能単位のモジュール分割。
- 文字列はシングルクオート基調（flake8-quotes）。docstringはダブルクオート。
- 最大行長 140、ignore は E722/W503（tox内flake8設定）。
- インポート順序は smarkets スタイル。
- `views/__init__.py` で各ビューをワイルドカード再エクスポートする構成。
- 変更は最小範囲で、関連テスト（unit/e2e）を優先実行する運用。
- 新しいPythonパッケージディレクトリには `__init__.py` 必須。
- `moneybook/e2e` に新規テスト追加時は GitHub Actions の e2e matrix 更新が必要。
