# MoneyBook - エージェント向けリポジトリガイド

このドキュメントは、MoneyBookリポジトリに対してコード変更やレビューを行うエージェント向けの包括的なガイドです。

## 前提

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
│   ├── requirements_e2e.txt   # e2eテスト（Selenium、ChromeDriver）
│   └── requirements_dev.txt   # 開発ツール（tox等）
├── .github/                    # GitHub関連
│   └── workflows/             # GitHub Actionsワークフロー
├── .vscode/                    # VSCode設定
│   └── settings.json          # エディタ設定
├── .dockerignore               # Dockerビルド除外設定
├── .flake8                     # Flake8リンター設定
├── .gitignore                  # Git除外設定
├── tox.ini                     # Tox設定（lint、テスト実行）
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

---

## 主要コンポーネント

### データベースモデル（`models/`）

MoneyBookの中核となるデータモデル：

| モデル           | 説明                                             |
| ---------------- | ------------------------------------------------ |
| `Direction`      | 取引方向（収入/支出）                            |
| `Method`         | 支払い方法（銀行、PayPay、現金など）             |
| `Category`       | 費目カテゴリー（生活費フラグ、変動費フラグ付き） |
| `Data`           | メインの取引記録                                 |
| `FixedCost`      | 固定費（定期的な支出）                           |
| `BankBalance`    | 銀行残高                                         |
| `CheckedDate`    | 確認済み日付                                     |
| `PreCheckedDate` | 事前確認日付                                     |

### ビュー（`views/`ディレクトリ）

10個の専門化されたビューモジュール：

1. **`IndexView`** - ダッシュボード（当月データ表示）
2. **`AddView`** - 取引入力
3. **`AddIntraMoveView`** - 内部移動の入力
4. **`EditView`** - 取引の編集
5. **`DeleteView`** - 取引の削除
6. **`SearchView`** - 取引検索
7. **`StatisticsView`** - 統計・分析（グラフ表示）
8. **`PeriodBalanceView`** - 期間別残高トレンド
9. **`ToolsView`** - ユーティリティ機能（実際の現金、残高チェック、事前確認マーク）
10. **`CustomLoginView`** - 認証

### フォーム（`forms.py`）

- データ入力フォーム
- 検索フォーム
- 各種バリデーション

### ユーティリティ（`utils.py`）

- 日付処理関数
- 集計計算
- データ変換

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
pip install -r requirements/requirements_dev.txt

# データベースマイグレーション
python manage.py migrate

# 開発サーバー起動
python manage.py runserver
```

---

## テスト実行

### 推奨: toxを使用した実行

toxを使用することで、環境を分離して一貫性のあるテストが可能です。

```bash
# リント確認
tox -e lint

# 単体テスト
tox -e unittest

# e2eテスト
tox -e e2e

# 全て実行
tox
```

### リント確認

プロジェクトでは `flake8` を使用してコード品質をチェックしています。

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

#### カバレッジ対象

- `moneybook.models`
- `moneybook.views`
- `moneybook.utils`
- `moneybook.middleware`
- `moneybook.forms`

[![codecov](https://codecov.io/gh/tMorriss/MoneyBook/branch/master/graph/badge.svg?token=E522OPRLRM)](https://codecov.io/gh/tMorriss/MoneyBook)

### E2Eテスト

Seleniumを使用したブラウザ自動化テストです。`moneybook.e2e` パッケージ内に配置されています。

#### 実行例

```bash
# 特定のテストモジュールを実行（例：indexモジュールのみ）
TEST_MODULE=moneybook.e2e.index.Index.test_index tox -e e2e

# ブラウザ表示モード（Mac）
HEADLESS=0 tox -e e2e

# ブラウザ表示モード（Windows）
$env:HEADLESS="0"; tox -e e2e
```

#### トラブルシューティング

```bash
# 詳細なログを表示
python manage.py test moneybook.e2e --settings config.settings.test --verbosity 2
```

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

| ファイル                             | 用途                                |
| ------------------------------------ | ----------------------------------- |
| `requirements/requirements.txt`      | 本番環境の依存関係                  |
| `requirements/requirements_test.txt` | テストツール                        |
| `requirements/requirements_e2e.txt`  | e2eテスト（Selenium、ChromeDriver） |
| `requirements/requirements_lint.txt` | コード品質チェック                  |
| `requirements/requirements_dev.txt`  | 開発ツール（tox等）                 |

### CI/CD

#### Jenkins

- `build/jenkins.sh` スクリプトによる自動ビルド・テスト・デプロイ

#### GitHub Actions

- **ワークフロー**: `.github/workflows/python-lint-test.yml`
- **トリガー**: Pull Request時に自動実行
- **ジョブ構成**:
  - `lint`: コード品質チェック（flake8）
  - `check-e2e-matrix`: e2e Matrix設定の整合性検証
  - `unittest`: カバレッジ付き単体テスト
  - `e2e`: matrix戦略によるe2eテスト並列実行

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
   - `moneybook/e2e/` ディレクトリに新しいテストファイルを追加した場合
   - **必ず** `.github/workflows/python-lint-test.yml` のe2eジョブのmatrixを更新する
   - 具体的には、以下の箇所に新しいテストモジュール名を追加：
     ```yaml
     strategy:
       matrix:
         test-module: [index, add, login, edit] # 新規モジュール名を追加
     ```
   - CI上で新しいe2eテストが自動実行されるようになる
   - ⚠️ GitHub Actionsの`check-e2e-matrix`ジョブが自動的にmatrix設定の漏れを検出し、CIをエラーにする

5. **マイグレーション**
   - モデル変更時は`makemigrations`を実行
   - マイグレーションファイルをレビュー

6. **ブランチの最新化（必須）**
   - **git pushする前に、必ずPRのマージ先ブランチ（通常は`master`）を取り込んで最新化すること**
   - コンフリクトがある場合は解決してからpushする
   - 例: `git fetch origin && git merge origin/master` または `git pull origin master`

7. **コミット**
   - 小さな単位でコミット
   - 日本語のコミットメッセージ

8. **PRのタイトルと説明**
   - PRのタイトルと説明は、このPRでの修正すべてを含んだものにする
   - 個別のコミットメッセージは各変更の詳細を記載し、PRの説明は全体のサマリーとする
   - 本番環境に影響がない場合（ドキュメント更新、テストのみの変更など）はPRタイトルに`[skip ci]`を付ける

9. **AGENTS.mdの更新**
   - 修正結果に応じて、このドキュメント自体の更新が必要か確認する
   - 新しいディレクトリ、ファイル、技術スタック、開発手順などを追加した場合は反映する

### 既知の問題・制約

- **データベース**: MySQL使用
- **ブラウザサポート**: モダンブラウザのみ（IE非対応）
- **認証**: カスタムミドルウェアを使用

---

## 関連ドキュメント

- [README.md](./README.md) - プロジェクト概要とクイックスタート

---

**注意**: このドキュメントは、エージェントがMoneyBookリポジトリを理解し、効率的にコード変更やレビューを行うために作成されました。人間の開発者向けの詳細は`README.md`を参照してください。
