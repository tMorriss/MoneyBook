# テスト実行ガイド

## E2Eテスト（Selenium）の並列実行

### 概要

MoneyBookのSeleniumテストは、Djangoの並列テスト機能を使用して高速化できます。並列実行により、テスト時間を大幅に短縮できます。

### 基本的な使い方

#### 並列実行（推奨）

```bash
# 自動的にCPUコア数に応じた並列数を設定
python manage.py test moneybook.selenium --settings config.settings.test --parallel auto

# 並列数を手動で指定（例：4並列）
python manage.py test moneybook.selenium --settings config.settings.test --parallel 4
```

#### シングルプロセス実行

```bash
# デバッグや問題の特定時に有用
python manage.py test moneybook.selenium --settings config.settings.test
```

### 並列実行の仕組み

1. **ポート分離**: `StaticLiveServerTestCase`を使用しているため、各テストプロセスで自動的に異なるポートが割り当てられます
2. **データベース分離**: 各プロセスが独自のテストデータベースを使用します
3. **ブラウザインスタンス**: 各テストで独立したChromeインスタンスが起動します

### パフォーマンス最適化

以下のChrome起動オプションにより、並列実行時のパフォーマンスと安定性が向上しています：

- `--disable-dev-shm-usage`: /dev/shmの容量不足を回避
- `--disable-gpu`: GPU使用を無効化（安定性向上）
- `--disable-extensions`: 拡張機能を無効化
- `--disable-software-rasterizer`: ソフトウェアラスタライザを無効化
- `--headless`: デフォルトでヘッドレスモード

### GitHub Actions での実行

GitHub Actionsでは自動的に並列実行が有効になっています：

```yaml
- name: Test
  run: |
    python manage.py test moneybook.selenium --settings config.settings.test --parallel auto
```

### デバッグモード

ブラウザを表示してデバッグする場合：

```bash
# Mac/Linux
HEADLESS=0 python manage.py test moneybook.selenium --settings config.settings.test

# Windows
$env:HEADLESS="0"; python manage.py test moneybook.selenium --settings config.settings.test
```

**注意**: 並列実行時にブラウザを表示すると、複数のブラウザウィンドウが同時に開きます。デバッグ時は以下のいずれかを推奨：

- 並列数を1に制限: `--parallel 1`
- 並列実行を無効化: `--parallel`オプションを外す
- 特定のテストクラスのみ実行: `python manage.py test moneybook.selenium.login`

### トラブルシューティング

#### メモリ不足

並列数が多すぎる場合、メモリ不足になる可能性があります。以下の対処法を試してください：

```bash
# 並列数を減らす
python manage.py test moneybook.selenium --settings config.settings.test --parallel 2
```

#### テストの失敗

並列実行で失敗する場合、シングルプロセスで実行して問題を特定してください：

```bash
python manage.py test moneybook.selenium --settings config.settings.test --verbosity 2
```

#### 特定のテストのみ実行

```bash
# 特定のテストクラスを実行
python manage.py test moneybook.selenium.login --settings config.settings.test

# 特定のテストメソッドを実行
python manage.py test moneybook.selenium.login.Login.test_login_button --settings config.settings.test
```

### パフォーマンス比較（参考）

| 実行方法 | 概算時間 |
|---------|---------|
| シングルプロセス | 基準（100%） |
| --parallel 2 | 約50-60% |
| --parallel 4 | 約30-40% |
| --parallel auto（8コア） | 約15-25% |

※実際の時間はテスト内容、マシンスペック、I/O性能により変動します。

## 単体テスト

単体テストも並列実行が可能ですが、カバレッジ測定時は並列実行を避けてください：

```bash
# 通常の実行（カバレッジ測定）
coverage run --source='moneybook.models,moneybook.views,moneybook.utils,moneybook.middleware,moneybook.forms' manage.py test moneybook.tests --settings config.settings.test

# 並列実行（カバレッジなし）
python manage.py test moneybook.tests --settings config.settings.test --parallel auto
```
