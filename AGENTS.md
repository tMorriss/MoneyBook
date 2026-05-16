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
- 🔄 静的ファイルのバージョン管理（キャッシュバスティング）

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

- **Playwright**: e2eテスト（ブラウザ自動化）
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
│   ├── views/                 # ビューハンドラー
│   ├── forms.py               # フォーム定義
│   ├── urls.py                # URLパターン
│   ├── utils.py               # ユーティリティ関数
│   ├── middleware/            # カスタムミドルウェア
│   ├── templates/             # HTMLテンプレート
│   ├── static/                # CSS、JS、画像
│   ├── migrations/            # DBスキーママイグレーション
│   ├── tests/                 # ユニットテスト
│   │   ├── models/            # モデルのテスト
│   │   └── views/             # ビューのテスト
│   ├── e2e/                   # e2eテスト（Playwright）
│   ├── fixtures/              # テストデータ
│   ├── admin.py               # Django管理画面設定
│   └── apps.py                # アプリケーション設定
├── build/                       # ビルド・デプロイ設定
│   ├── Dockerfile.gunicorn    # GunicornコンテナのDockerfile
│   ├── Dockerfile.nginx       # NginxコンテナのDockerfile
│   ├── pod.yaml               # Kubernetes Pod定義
│   └── jenkins.sh             # CI/CDスクリプト
├── nginx/                       # Nginx設定
│   └── nginx.conf             # Nginx設定ファイル
├── requirements/               # Pythonパッケージ依存関係
│   ├── requirements.txt       # 本番環境の依存関係
│   ├── requirements_test.txt  # テストツール
│   ├── requirements_lint.txt  # コード品質チェック
│   ├── requirements_e2e.txt   # e2eテスト（Playwright）
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
├── check_filenames.py          # ファイル名命名規則検証スクリプト（CI用）
├── check_init_py.sh            # __init__.py記載漏れ検証スクリプト（CI用）
├── create_data_yaml.py         # データYAML生成スクリプト
├── create_other_yaml.py        # その他YAML生成スクリプト
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

| モデル         | 説明                                             |
| -------------- | ------------------------------------------------ |
| `Direction`    | 取引方向（収入/支出）                            |
| `Method`       | 支払い方法（銀行、PayPay、現金など）             |
| `Category`     | 費目カテゴリー（生活費フラグ、変動費フラグ付き） |
| `Data`         | メインの取引記録                                 |
| `PeriodicData` | 定期取引データ（毎月の定期的な取引を設定）       |
| `BankBalance`  | 銀行残高                                         |
| `CheckedDate`  | 確認済み日付                                     |

### ビュー（`views/`ディレクトリ）

機能ごとに専門化されたビューモジュール。各ビューは独立したファイルとして構成されています（ただし、機能的に関連性の高いものは一つのファイルにまとめられている場合もあります）：

- **`IndexView`** - ダッシュボード（当月データ表示）
- **`AddView`** - 取引入力ページ
- **`EditView`** - 取引の編集ページ
- **`SearchView`** - 取引検索
- **`StatisticsView`** - 統計・分析（グラフ表示）
- **`PeriodBalanceView`** - 期間別残高トレンド
- **`PeriodicView`** - 定期取引管理（一覧、設定、一括登録）
- **`ToolsView`** - ユーティリティ機能ページ
- **`CustomLoginView`** - 認証
- **`*ApiView`** - JSONを返すAPIエンドポイント（すべて `/api/` プレフィックスを持つ）。`addApiView.py`, `editApiView.py` など、機能ごとに分割されています。

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

- 設定済みの定期取引を表形式で一覧表示（tbl-dataスタイル）
- 年月を指定して「追加」ボタンで一括登録を実行
- 年月のデフォルト値は来月（未入力時に使用、placeholderに表示）
- 「編集」ボタンで編集画面に遷移

#### 2. 編集画面（`/periodic/edit`）

- 定期取引データの追加・編集・削除
- tbl-commonスタイルを使用したテーブル形式で全項目を編集可能
- 各入力フィールド:
  - 日付・金額: type="text"、黄色背景（#fffacd）、spinnerなし
  - 品目: type="text"、黄色背景
  - select box: 緑色（#a1b91d）、オプションはhoverで緑（.select-greenクラス）
- 「行を追加」ボタンで新規行を追加（中央配置）
- 「削除」ボタンで行を削除（confirmダイアログなし、DOM上で即座に削除）
- 「更新」ボタンで保存して一覧画面に戻る（form POST + リダイレクト）
- 「キャンセル」ボタンで変更を破棄して一覧画面に戻る

#### 3. 一括登録処理

- 既存の`/api/add`エンドポイントを1件ずつ呼び出し
- async/awaitとfor文による実装
- 100ms間隔で順次登録
- 日付の早いものから順に登録
- 重複チェックなし（常に登録）
- 月の日数を超える日付は最終日に自動調整
- 成功時: `Success!`メッセージ（showResultMsg使用）
- エラー時: `Error...`メッセージ（showResultMsg使用）

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
pip install -r requirements/requirements_e2e.txt
pip install -r requirements/requirements_dev.txt

# データベースマイグレーション
python manage.py migrate

# 開発サーバー起動
python manage.py runserver
```

### 依存関係

| ファイル                             | 用途                                |
| ------------------------------------ | ----------------------------------- |
| `requirements/requirements.txt`      | 本番環境の依存関係                  |
| `requirements/requirements_test.txt` | テストツール                        |
| `requirements/requirements_e2e.txt`  | e2eテスト（Selenium、ChromeDriver） |
| `requirements/requirements_lint.txt` | コード品質チェック                  |
| `requirements/requirements_dev.txt`  | 開発ツール（tox等）                 |

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

JSはlintが導入できていないが、各行末尾の不要なスペースは削除してください。

#### 設定詳細 (`.flake8`)

**PEP 8準拠** - ただし、一部カスタマイズあり

- **無視するルール**: `E722` (bare except), `W503` (line break before binary operator)
- **最大行長**: 140文字
- **除外**: マイグレーション、`__init__.py`
- **インポート順序スタイル**: smarkets
- **ファイル名**: すべてスネークケース（`snake_case.py`）で統一する。
- **文字リテラル**:
  - **原則**: シングルクオート `'...'` を使用
  - **docstring**: 常にダブルクオート `"""..."""` を使用

### 単体テスト

`moneybook.tests` パッケージ内のテストを実行します。カバレッジ測定も合わせて行うことを推奨します。

テストコードは機能ごとに以下のディレクトリに配置してください：

- **モデルのテスト**: `moneybook/tests/models/`
- **ビューのテスト**: `moneybook/tests/views/`
- **ユーティリティ等のテスト**: `moneybook/tests/` 直下

#### カバレッジ対象

- `moneybook.models`
- `moneybook.views`
- `moneybook.utils`
- `moneybook.middleware`
- `moneybook.forms`

### E2Eテスト

Playwrightを使用したブラウザ自動化テストです。`moneybook.e2e` パッケージ内に配置されています。

#### 実行例

```bash
# 特定のテストモジュールを実行（例：indexモジュールのみ）
TEST_MODULE=moneybook.e2e.index.Index.test_index tox -e e2e

# ブラウザ表示モード
HEADLESS=0 tox -e e2e
```

#### Playwrightテストの実装指針と注意点

- **Django ORMの制限**: Playwrightの非同期イベントループ内でのDjango ORM操作は `SynchronousOnlyOperation` エラーを引き起こすため、テストメソッド内での直接的なDB操作（`PeriodicData.objects.create` など）は避けること。データ準備や検証はブラウザ操作または事前に用意されたフィクスチャを通じて行う。
- **AJAX同期**: インデックスページなどのAJAX駆動の要素を検証する際は、`window.jQuery.active === 0` を待機し、さらに特定のDOM要素の状態（例: `#summary-count` が初期値 '件' から更新されるまで）を確認することで、 stale な状態でのアサーションを回避する。
- **入力操作**: JavaScriptによるフォーマット処理（カンマの自動挿入など）が行われる入力フィールドについては、`.focus()` を呼び出してフォーマットを解除してから `fill()` を行う。
- **視認性の検証**: CSSクラス（`.hidden-row` など）によって非表示にされている要素を検証する場合、`expect(locator).to_have_class(re.compile(r'hidden-row'))` を使用して、DOM上に存在するが不可視であることを明示的に確認する。
- **トラブルシューティング**:
  - テスト失敗時には `playwright-artifact/` ディレクトリにトレース（スクリーンショット、スナップショット含む）が保存される。
  - 手動で `manage.py test` を実行して詳細を確認する場合、`export DJANGO_ALLOW_ASYNC_UNSAFE=true` を設定することで、テスト中のDBアクセスを許可できる（ただし、ソースコードやCI設定にこれをハードコードしないこと）。

---

## コーディング規約

基本的にはコードスタイルや実装方針、仕様やデザインは既存のものに沿うようにします。

### Djangoベストプラクティス

1. **設定の分離**: 環境別設定を`config/settings/`で管理
2. **静的ファイル**: `{% static %}`タグを使用してパスを生成
3. **HTTPステータスコード**: ステータスコードを指定または検証する際は、数値（例: 200, 400）を直接使用せず、`http.HTTPStatus`を使用してください。
   - インポート形式: `from http import HTTPStatus`
   - 利用方法: `HTTPStatus.OK`, `HTTPStatus.BAD_REQUEST` など
   - ただし、Djangoが提供する特定のステータスコード用クラス（例: `HttpResponseRedirect`）が利用可能な場合は、それらを使用しても構いません。

### CSS/スタイル規約

1. **共通スタイルの使用**:
   - 基本的なスタイルは`static/style.css`に定義し、全ページで共有する
   - ボタン（`.btn-green`, `.btn-blue`, `.btn-red`）
   - テーブル（`.tbl-periodic`, `.tbl-periodic-config`）
   - コンテンツエリア（`.main-content`, `.control-panel`）
   - 進捗表示（`#progress_area`, `.progress-item`）
   - レスポンシブデザイン（メディアクエリ）

2. **ページ固有CSSファイル**:
   - 各ページ専用のCSSファイル（例: `periodic.css`, `tools.css`）には、そのページ固有のスタイルのみを記載
   - 共通スタイルの重複定義は避ける
   - ページ固有の例: 特定の入力フィールドの幅調整、特殊なレイアウト調整

3. **CSS読み込み**:
   - `style.css`は`_base.html`で自動的に読み込まれる
   - ページ固有のCSSは各テンプレートの`{% block header %}`内で読み込む
   ```html
   {% block header %}
   <link rel="stylesheet" type="text/css" href="{% static 'periodic.css' %}" />
   {% endblock %}
   ```

### レビュー規則

- **言語**: レビューやサマリーは日本語で記載
- **変更範囲**: 最小限の変更を心がける
- **テストカバレッジ**: 新機能には必ずテストを追加

---

## デプロイメント

### CI/CD

#### Jenkins

`build/jenkins.sh` スクリプトによる自動ビルド・テスト・デプロイ
(jenkins上から`build/jenkins.sh`が直接呼び出される)

#### GitHub Actions

- **ワークフロー**: `.github/workflows/ci.yml`
- **ジョブ構成**:
  - `lint`: コード品質チェック（flake8）
  - `check-e2e-matrix`: e2e Matrix設定の整合性検証
  - `unittest`: カバレッジ付き単体テスト
  - `e2e`: matrix戦略によるe2eテスト並列実行（Playwright）

---

## エージェント向け注意事項

### コード変更時の推奨手順

1. **影響範囲の確認**
2. **リント実行**
3. **テスト実行**
   - 関連する単体テストを実行
   - 必要に応じてe2eテストを実行
4. **新しいPythonパッケージディレクトリ追加時の手順**
   - **必ず** `__init__.py` も一緒に追加する（`check-init-py` ジョブで検証）。
5. **e2eテストファイル追加時の手順**
   - `moneybook/e2e/` ディレクトリに新しいテストファイルを追加した場合、**必ず** `.github/workflows/ci.yml` のe2eジョブのmatrixを更新する。
   - `check-e2e-matrix` ジョブが不整合を検出し、CIをエラーにする。

6. **マイグレーション**
   - モデル変更時は`makemigrations`を実行
   - マイグレーションファイルをレビュー

7. **ブランチの最新化（必須）**
   - **git pushする前に、必ずPRのマージ先ブランチ（通常は`master`）を取り込んで最新化すること**
   - 他の開発者による更新がある場合、マージ先のブランチを自身のブランチに取り込む
   - ユーザが作業用ブランチを更新（GitHub上の「Update branch」実行など）した場合も同様とする
   - マージ作業やユーザによる更新によって発生した差分は、自身のPRにおける修正分として扱う
   - 取り込み後、PRとして実質的な差分がない場合はそのままpushしてよい
   - コンフリクトがある場合は解決してからpushする
   - 例: `git fetch origin && git merge origin/master` または `git pull origin master`

8. **PRのタイトルと説明**

- PRのタイトルと説明は、このPRでの修正すべてを含んだものにする
- 個別のコミットメッセージは各変更の詳細を記載し、PRの説明は全体のサマリーとする
- 本番環境に影響がない場合（ドキュメント更新、テストのみの変更など）はPRタイトルに`[skip ci]`を付ける

9. **AGENTS.mdの更新**

- 修正結果に応じて、このドキュメント自体の更新が必要か確認する
- 新しいディレクトリ、ファイル、技術スタック、開発手順などを追加した場合は反映する

---

**注意**: このドキュメントは、エージェントがMoneyBookリポジトリを理解し、効率的にコード変更やレビューを行うために作成されました。人間の開発者向けの詳細は`README.md`を参照してください。
