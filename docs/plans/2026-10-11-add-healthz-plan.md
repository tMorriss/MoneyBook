# `/healthz` エンドポイント追加計画

## 目的

Podman QuadletのヘルスチェックからMoneyBookのHTTPアプリケーションが応答可能か確認できるよう、認証なしでアクセスできる `GET /healthz` を追加する。

## 現状

- `config/urls.py` から `moneybook.urls` をルートURLとして読み込んでいる。
- 認証は `moneybook/middleware/auth.py` の `AuthMiddleware` が一括して制御している。
- 現在は `moneybook:login` のパスだけが認証不要で、ミドルウェア内で個別に判定している。
- 未認証アクセスは、通常ページではログイン画面へリダイレクトされ、`/api/` では403を返す。
- ビューは `moneybook/views/` にクラスベースで配置され、`moneybook/urls.py` で名前付きURLとして登録されている。
- この計画書の作成前は `docs/plans/` は存在しなかった。

## 方針

1. `moneybook/views/health_view.py` に `HealthView` を追加する。
2. `GET /healthz` に対応する名前付きURL（`moneybook:health`）を `moneybook/urls.py` に登録する。
3. `AuthMiddleware` に認証不要URL名のリスト（例: `AUTH_EXEMPT_VIEW_NAMES = ['moneybook:login', 'moneybook:health']`）を設け、`resolve(request.path_info).view_name` がリストに含まれる場合は認証判定を通さずビューへ渡す。
4. URL解決に失敗したパスは認証不要扱いにせず、従来どおりの未認証処理（APIなら403、それ以外はログイン画面へリダイレクト）を適用する。
5. ビューはDBや外部サービスへ接続せず、応答可能な場合にHTTP 200と短い本文（`ok`）を返す。これはアプリの生存確認とし、DBを含む準備状態確認は今回の範囲に含めない。
6. `moneybook/tests/views/health_view_tests.py` ではヘルスビュー単体の応答を確認する。
7. `moneybook/tests/middleware/auth_tests.py` を追加し、未認証でのヘルスチェック・ログインURLへのアクセス、通常ページ/API/未登録パスの未認証時挙動を確認する。

## 受け入れ条件

- ヘルスビュー単体のテストでHTTP 200、本文 `ok`、DBアクセスがないことを確認する。
- ミドルウェアテストで認証なしの `GET /healthz` がログイン画面へリダイレクトされずHTTP 200を返し、認証済みの場合もHTTP 200を返す。
- `moneybook:login` と `moneybook:health` が認証不要URL名のリストで管理される。
- 認証不要判定がURLパスの直書き比較ではなく、URL解決結果の名前に基づく。
- ヘルスチェック処理でDBアクセスが発生しない。
- 未認証の通常ページは引き続きログイン画面へリダイレクトされ、未認証の `/api/` は引き続き403を返す。
- 既存の命名規則、シングルクォート、HTTPステータスには `http.HTTPStatus` を使う規約に従う。

## 実装・確認手順

1. ビュー、URL、認証ミドルウェアのURL名リスト管理を実装する。
2. ビュー単体テストと、`moneybook/tests/middleware/` 配下のミドルウェアテストを追加する。
3. 関連テストを実行し、必要に応じてlintを実行する。
4. 差分を確認し、`AGENTS.md` の更新が必要か判断する。今回の追加だけなら通常は不要。

## 対象外

- Quadletユニットファイルの作成・変更
- DB接続や依存サービスを含めたreadiness確認
- URL名リスト方式を超える認証ミドルウェア全体の設計変更
