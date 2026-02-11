# テスト実行ガイド

## E2Eテスト（Selenium）

### 概要

MoneyBookのE2Eテストは、ブラウザ自動化によるエンドツーエンドテストです。

### 基本的な使い方

```bash
# 基本的な実行
python manage.py test moneybook.e2e --settings config.settings.test
```

### GitHub Actions での実行

GitHub Actionsでは以下のように実行されています：

```yaml
- name: Test
  run: |
    python manage.py test moneybook.e2e.$TEST_MODULE --settings config.settings.test
```

### デバッグモード

ブラウザを表示してデバッグする場合：

```bash
# Mac/Linux
HEADLESS=0 python manage.py test moneybook.e2e --settings config.settings.test

# Windows
$env:HEADLESS="0"; python manage.py test moneybook.e2e --settings config.settings.test
```

### トラブルシューティング

#### 特定のテストのみ実行

```bash
# 特定のテストクラスを実行
python manage.py test moneybook.e2e.login --settings config.settings.test

# 特定のテストメソッドを実行
python manage.py test moneybook.e2e.login.Login.test_login_button --settings config.settings.test
```

#### 詳細なログを表示

```bash
python manage.py test moneybook.e2e --settings config.settings.test --verbosity 2
```

## 単体テスト

単体テストはカバレッジ測定と共に実行することを推奨します：

```bash
# カバレッジ測定付き実行
coverage run --source='moneybook.models,moneybook.views,moneybook.utils,moneybook.middleware,moneybook.forms' manage.py test moneybook.tests --settings config.settings.test

# カバレッジレポート表示
coverage report -m

# 通常の実行
python manage.py test moneybook.tests --settings config.settings.test
```
