# MoneyBook - エージェント向けリポジトリガイド

このドキュメントは、MoneyBookリポジトリに対してコード変更やレビューを行うエージェント向けの包括的なガイドです。

対話やレビュー、サマリー作成、PRタイトル作成やコメント(ソースコード上のコメントも含む)などは日本語で行うこと。

## 📋 目次

1. [プロジェクト概要](#プロジェクト概要)
2. [技術スタック](#技術スタック)
3. [ディレクトリ構造](#ディレクトリ構造)
4. [主要コンポーネント](#主要コンポーネント)
5. [開発ワークフロー](#開発ワークフロー)
6. [テスト実行](#テスト実行)
7. [コーディング規約](#コーディング規約)
8. [デプロイメント](#デプロイメント)

---

## プロジェクト概要

**MoneyBook** は、個人用の家計簿管理を行うDjangoベースのWebアプリケーションです。

### 主な機能
- 📊 収支データの記録と管理
- 💰 カテゴリー別の支出・収入の分類
- 🏦 銀行残高の追跡
- 📈 統計・分析機能（グラフ表示）
- 🔄 固定費の管理
- 🔍 取引履歴の検索機能
- ✅ 残高チェック機能

---

## 技術スタック

### バックエンド
- **Python**: プログラミング言語
- **Django 4.2.27+**: Webフレームワーク
- **MySQL**: データベース
- **mysqlclient**: MySQLデータベースアダプター
- **Gunicorn**: WSGIサーバー

### フロントエンド
- **HTML/CSS/JavaScript**: 基本的なWeb技術
- **AmCharts4**: チャートライブラリ（統計グラフ表示）
- **django-mathfilters**: Djangoテンプレートの数学フィルター

### 開発・テスト
- **Selenium**: e2eテスト（ブラウザ自動化）
- **Coverage.py**: コードカバレッジ測定
- **Flake8**: コード品質チェック（リンター）
  - **flake8-quotes**: クオートスタイルチェック（シングルクオート強制）
  - **flake8-import-order**: インポート順序チェック
  - **pep8-naming**: 命名規則チェック
- **python-dateutil**: 日付処理ユーティリティ

### DevOps
- **Docker**: コンテナ化
- **Nginx**: リバースプロキシ・Webサーバー
- **Jenkins**: CI/CDパイプライン
- **GitHub Actions**: ワークフロー自動化

---

## ディレクトリ構造

```
MoneyBook/
├── manage.py                    # Django管理スクリプト
├── config/                      # Django設定パッケージ
│   ├── settings/               # 環境別設定
│   │   ├── common.py          # 共通設定
│   │   ├── dev.py             # 開発環境設定
│   │   ├── prod.py            # 本番環境設定
│   │   └── test.py            # テスト環境設定
│   ├── urls.py                # メインURLルーティング
│   └── wsgi.py                # WSGIアプリケーションエントリーポイント
├── moneybook/                   # メインDjangoアプリ
│   ├── models/                # データベースモデル（1モデル1ファイル）
│   ├── views/                 # ビューハンドラー（10個の専門化されたビュー）
│   ├── forms.py               # フォーム定義
│   ├── urls.py                # URLパターン
│   ├── utils.py               # ユーティリティ関数
│   ├── middleware/            # カスタムミドルウェア
│   ├── templates/             # HTMLテンプレート
│   ├── static/                # CSS、JS、画像
│   ├── migrations/            # DBスキーママイグレーション
│   ├── tests/                 # ユニットテスト
│   ├── e2e/                   # e2eテスト（Selenium）
│   ├── fixtures/              # テストデータ
│   ├── admin.py               # Django管理画面設定
│   └── apps.py                # アプリケーション設定
├── build/                       # ビルド・デプロイ設定
│   ├── Dockerfile.gunicorn    # GunicornコンテナのDockerfile
│   ├── Dockerfile.nginx       # NginxコンテナのDockerfile
│   ├── nginx.conf             # Nginx設定ファイル
│   ├── pod.yaml               # Kubernetes Pod定義
│   └── jenkins.sh             # CI/CDスクリプト
├── requirements/               # Pythonパッケージ依存関係
│   ├── requirements.txt       # 本番環境の依存関係
│   ├── requirements_test.txt  # テストツール
│   ├── requirements_lint.txt  # コード品質チェック
│   └── requirements_selenium.txt # e2eテスト（Selenium、ChromeDriver）
├── .github/                    # GitHub関連
│   └── workflows/             # GitHub Actionsワークフロー
├── .vscode/                    # VSCode設定
│   └── settings.json          # エディタ設定
├── .dockerignore               # Dockerビルド除外設定
├── .flake8                     # Flake8リンター設定
├── .gitignore                  # Git除外設定
├── check_e2e_matrix.sh         # e2e Matrix検証スクリプト（CI用）
├── createDataYaml.py           # データYAML生成スクリプト
├── createOtherYaml.py          # その他YAML生成スクリプト
├── generate_secretkey_setting.py # シークレットキー生成
├── yaml_utils.py               # YAML処理ユーティリティ
├── copyDB.cmd                  # データベースコピースクリプト（Windows）
├── copyDB.sh                   # データベースコピースクリプト（Unix）
├── AGENTS.md                   # エージェント向けガイド
├── CLAUDE.md                   # AGENTS.mdへのシンボリックリンク
└── README.md                   # プロジェクトREADME
```

### ディレクトリ詳細

| ディレクトリ | 目的 |
|-----------|---------|
| `config/settings/` | 環境別のDjango設定（開発、本番、テスト） |
| `moneybook/models/` | データベースモデル定義（Direction, Method, Category, Dataなど） |
| `moneybook/views/` | ビューロジック（10個のモジュールに分割） |
| `moneybook/templates/` | Djangoテンプレート（ベースレイアウト、フォーム、データテーブル、チャート） |
| `moneybook/static/` | クライアント側アセット（CSS、JS、画像） |
| `moneybook/migrations/` | データベーススキーマバージョニング（22マイグレーション） |
| `moneybook/tests/` | ユニットテスト（モデル、ビュー、フォーム、ユーティリティ） |
| `moneybook/e2e/` | e2eブラウザ自動化テスト |
| `moneybook/middleware/` | カスタム認証ミドルウェア |
| `build/` | 依存関係、Docker、デプロイ設定 |
| `requirements/` | Pythonパッケージの依存関係ファイル |

---

## 主要コンポーネント

### データベースモデル（`models/`）

MoneyBookの中核となるデータモデル：

| モデル | 説明 |
|--------|------|
| `Direction` | 取引方向（収入/支出） |
| `Method` | 支払い方法（銀行、PayPay、現金など） |
| `Category` | 費目カテゴリー（生活費フラグ、変動費フラグ付き） |
| `Data` | メインの取引記録 |
| `PeriodicData` | 定期取引データ（毎月の定期的な取引を設定） |
| `BankBalance` | 銀行残高 |
| `CheckedDate` | 確認済み日付 |
| `PreCheckedDate` | 事前確認日付 |

### ビュー（`views/`ディレクトリ）

11個の専門化されたビューモジュール：

1. **`IndexView`** - ダッシュボード（当月データ表示）
2. **`AddView`** - 取引入力
3. **`AddIntraMoveView`** - 内部移動の入力
4. **`EditView`** - 取引の編集
5. **`DeleteView`** - 取引の削除
6. **`SearchView`** - 取引検索
7. **`StatisticsView`** - 統計・分析（グラフ表示）
8. **`PeriodBalanceView`** - 期間別残高トレンド
9. **`PeriodicView`** - 定期取引管理（一覧、設定、一括登録）
10. **`ToolsView`** - ユーティリティ機能（実際の現金、残高チェック、事前確認マーク）
11. **`CustomLoginView`** - 認証

### フォーム（`forms.py`）

- **DataForm** - データ入力フォーム
- **PeriodicDataForm** - 定期取引設定フォーム
- **IntraMoveForm** - 内部移動フォーム
- 検索フォーム
- 各種バリデーション

### ユーティリティ（`utils.py`）

- 日付処理関数
- 集計計算
- データ変換

---

## 定期取引機能（Periodic）

### 概要
家賃やサブスク支払い、貯金など、毎月定期的に発生する取引を一括登録する機能です。

### 機能詳細

#### 1. 一覧表示（`/periodic`）
- 設定済みの定期取引を表形式で一覧表示
- 年月を指定して「追加」ボタンで一括登録を実行
- 年月のデフォルト値は来月（未入力時に使用）
- 「設定」ボタンで設定画面に遷移

#### 2. 設定画面（`/periodic/config`）
- 定期取引データの追加・編集・削除
- テーブル形式で全項目を編集可能
- 「更新」ボタンで保存して一覧画面に戻る

#### 3. 一括登録API（`/periodic/add_bulk`）
- 指定された年月に対して定期取引を登録
- 日付の早いものから順にAjax送信
- 重複チェックなし（常に登録）
- 月の日数を超える日付は最終日に自動調整

### データモデル
```python
class PeriodicData:
    day         # 日（1-31）
    item        # 品目
    price       # 金額
    direction   # 方向（収入/支出）
    method      # 支払い方法
    category    # 分類
    temp        # 立替フラグ
```

### URL設計
- `/moneybook/periodic` - 一覧表示
- `/moneybook/periodic/config` - 設定画面
- `/moneybook/periodic/add_bulk` - 一括登録API（POST）

### テスト
- **モデルテスト**: 5個のテストケース
- **ビューテスト**: 14個のテストケース（重複登録、日付オーバーフロー等）
- **E2Eテスト**: 7個のテストケース（ナビゲーション、CRUD、一括登録、デフォルト値）

---

## 開発ワークフロー

### 環境セットアップ

```bash
# 仮想環境の作成（Windows）
python -m venv .venv

# アクティベート（Windows）
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\.venv\Scripts\activate

# 依存関係のインストール
pip install -r requirements/requirements.txt
pip install -r requirements/requirements_test.txt
pip install -r requirements/requirements_lint.txt

# データベースマイグレーション
python manage.py migrate

# 開発サーバー起動
python manage.py runserver
```

### コード変更時の確認事項

1. **リント実行** - コード品質チェック
2. **単体テスト** - 機能の正常性確認
3. **e2eテスト** - 統合動作確認
4. **マイグレーション** - モデル変更時

---

## テスト実行

### リント確認

プロジェクトでは `flake8` を使用してコード品質をチェックしています。

#### 実行コマンド

```bash
flake8 . --count --ignore=E722,W503 --max-line-length=140 \
  --exclude moneybook/migrations,__init__.py \
  --show-source --statistics --import-order-style smarkets
```

#### 設定詳細 (`.flake8`)

- **無視するルール**: `E722` (bare except), `W503` (line break before binary operator)
- **最大行長**: 140文字
- **除外**: マイグレーション、`__init__.py`
- **インポート順序スタイル**: smarkets
- **クオートスタイル**: `flake8-quotes`により、シングルクオート `'...'` を強制
  - 文字列内にシングルクオートが含まれる場合のみダブルクオート `"..."` を使用
  - docstringは常にダブルクオート `"""..."""` を使用（PEP 257準拠）

### 単体テスト

`moneybook.tests` パッケージ内のテストを実行します。カバレッジ測定も合わせて行うことを推奨します。

#### 実行コマンド

```bash
# カバレッジ付きテスト実行
coverage run --source='moneybook.models,moneybook.views,moneybook.utils,moneybook.middleware,moneybook.forms' \
  manage.py test moneybook.tests --settings config.settings.test

# レポート表示
coverage report -m

# XML形式で出力（VSCode連携など）
coverage xml

# 通常の実行（カバレッジなし）
python manage.py test moneybook.tests --settings config.settings.test
```

#### カバレッジ対象
- `moneybook.models`
- `moneybook.views`
- `moneybook.utils`
- `moneybook.middleware`
- `moneybook.forms`

[![codecov](https://codecov.io/gh/tMorriss/MoneyBook/branch/master/graph/badge.svg?token=E522OPRLRM)](https://codecov.io/gh/tMorriss/MoneyBook)

### E2Eテスト

Seleniumを使用したブラウザ自動化テストです。`moneybook.e2e` パッケージ内に配置されています。

#### 実行コマンド

```bash
# ヘッドレスモード（デフォルト・CI環境）
python manage.py test moneybook.e2e --settings config.settings.test

# ブラウザ表示モード（Mac）
HEADLESS=0 python manage.py test moneybook.e2e --settings config.settings.test

# ブラウザ表示モード（Windows）
$env:HEADLESS="0"; python manage.py test moneybook.e2e --settings config.settings.test
```

#### トラブルシューティング

**特定のテストのみ実行**:

```bash
# 特定のテストクラスを実行
python manage.py test moneybook.e2e.login --settings config.settings.test

# 特定のテストメソッドを実行
python manage.py test moneybook.e2e.login.Login.test_login_button --settings config.settings.test
```

**詳細なログを表示**:

```bash
python manage.py test moneybook.e2e --settings config.settings.test --verbosity 2
```

**重要**: `moneybook/e2e/` ディレクトリに新しいテストファイルを追加した場合、GitHub Actionsのワークフロー (`.github/workflows/python-lint-test.yml`) のe2eジョブのmatrixも更新する必要があります。詳細は「[エージェント向け注意事項 > コード変更時の推奨手順 > e2eテストファイル追加時の手順](#エージェント向け注意事項)」を参照してください。

---

## コーディング規約

### Pythonコードスタイル

1. **PEP 8準拠** - ただし、一部カスタマイズあり
2. **最大行長**: 140文字
3. **インポート順序**: smarketsスタイル
   - 標準ライブラリ
   - サードパーティライブラリ
   - ローカルアプリケーション
4. **文字リテラル**: 
   - **原則**: シングルクオート `'...'` を使用
   - **例外**: 文字列内にシングルクオートが含まれる場合はダブルクオート `"..."` を使用（エスケープ回避のため）
   - **docstring**: 常にダブルクオート `"""..."""` を使用（PEP 257に準拠）
   - `flake8-quotes`プラグインにより自動チェック（`.flake8`に`inline-quotes = single`を設定）
5. **例外処理**: bare exceptは避ける（E722は特定箇所で許可）

### Djangoベストプラクティス

1. **設定の分離**: 環境別設定を`config/settings/`で管理
2. **ビューの分割**: 機能ごとに専門化されたビューモジュール
3. **URL命名**: 明確なURL名を使用（`name=`パラメータ）
4. **テンプレート**: ベーステンプレート継承パターン
5. **静的ファイル**: `{% static %}`タグを使用

### レビュー規則

- **言語**: レビューやサマリーは日本語で記載
- **変更範囲**: 最小限の変更を心がける
- **テストカバレッジ**: 新機能には必ずテストを追加

---

## デプロイメント

### Docker

```bash
# イメージビルド
docker build -f build/docker/Dockerfile -t moneybook:latest .

# コンテナ起動
docker run -p 8000:8000 moneybook:latest
```

### 依存関係

| ファイル | 用途 |
|---------|------|
| `requirements/requirements.txt` | 本番環境の依存関係 |
| `requirements/requirements_test.txt` | テストツール |
| `requirements/requirements_selenium.txt` | e2eテスト（Selenium、ChromeDriver） |
| `requirements/requirements_lint.txt` | コード品質チェック |

### CI/CD

- **Jenkins**: `build/jenkins.sh`スクリプトでビルド・テスト・デプロイを自動化
- **GitHub Actions**: `.github/workflows/`でワークフロー定義
  - `python-lint-test.yml`: Pull Request時に自動実行
    - **lint**: Flake8によるコード品質チェック
    - **check-e2e-matrix**: e2e Matrix設定の検証（`check_e2e_matrix.sh`シェルスクリプトを実行）
      - `moneybook/e2e/`ディレクトリ内で` def test_`パターンを含むファイル（実際のテストを含むファイル）を自動検出
      - matrix設定との整合性をチェック
      - 漏れがある場合はCIをエラーにする
      - `yq`コマンドを使用してYAML解析
    - **unittest**: カバレッジ付き単体テスト
    - **e2e**: e2eテスト（matrix戦略でテストモジュール別に並列実行）
      - 現在のテストモジュール: `index`, `add`, `login`
      - ⚠️ 新規e2eテストファイル追加時は、matrixを更新してCI上で実行されるようにすること（`check-e2e-matrix`ジョブが自動チェックする）

---

## エージェント向け注意事項

### コード変更時の推奨手順

1. **影響範囲の確認**
   - 変更するファイルの依存関係を確認
   - 関連するテストを特定

2. **リント実行**
   - コード変更前に既存のリントエラーを確認
   - 新規エラーのみを修正

3. **テスト実行**
   - 関連する単体テストを実行
   - 必要に応じてe2eテストを実行

4. **e2eテストファイル追加時の手順**
   - `moneybook/e2e/` ディレクトリに新しいテストファイル（例: `edit.py`）を追加した場合
   - **必ず** `.github/workflows/python-lint-test.yml` のe2eジョブのmatrixを更新する
   - 具体的には、以下の箇所に新しいテストモジュール名を追加：
     ```yaml
     strategy:
       matrix:
         test-module: [index, add, login, edit]  # 新規モジュール名を追加
     ```
   - これにより、CI上でも新しいe2eテストが自動実行される
   - ⚠️ この更新を忘れると、新しいe2eテストがCI上で実行されないため注意
   - **自動チェック**: GitHub Actionsの`check-e2e-matrix`ジョブが自動的にmatrix設定の漏れをチェックし、漏れがある場合はCIをエラーにする

5. **マイグレーション**
   - モデル変更時は`makemigrations`を実行
   - マイグレーションファイルをレビュー

6. **ブランチの最新化（必須）**
   - **git pushする前に、必ずPRのマージ先ブランチを取り込んで最新化すること**
   - マージ先ブランチ（通常は`master`または`main`）の最新変更を取り込む
   - コンフリクトがある場合は解決してからpushする
   - 例: `git fetch origin && git merge origin/master` または `git pull origin master`

7. **コミット**
   - 小さな単位でコミット
   - 日本語のコミットメッセージ

8. **PRのタイトルと説明**
   - PRのタイトルやコメント（説明）は、直近の修正のみではなく、このPRでの修正すべてを含んだものにする
   - PR全体の目的と変更内容を網羅的に記載する
   - 個別のコミットメッセージは各変更の詳細を記載し、PRの説明は全体のサマリーとする
   - アプリケーション本体の本番環境に影響がないとき（ドキュメント更新、テストのみの変更など）はPRタイトルに`[skip ci]`を付ける

9. **AGENTS.mdの更新**
   - 修正結果に応じて、このAGENTS.mdドキュメント自体の更新が必要か確認する
   - 新しいディレクトリ、ファイル、技術スタック、開発手順などを追加した場合は、AGENTS.mdに反映する
   - ドキュメントがリポジトリの実態と常に同期するよう維持する

### 既知の問題・制約

- **データベース**: MySQL使用
- **ブラウザサポート**: モダンブラウザのみ（IE非対応）
- **認証**: カスタムミドルウェアを使用

---

## 関連ドキュメント

- [README.md](./README.md) - プロジェクト概要とクイックスタート

---

**注意**: このドキュメントは、エージェントがMoneyBookリポジトリを理解し、効率的にコード変更やレビューを行うために作成されました。人間の開発者向けの詳細は`README.md`を参照してください。
