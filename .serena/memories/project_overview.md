# MoneyBook プロジェクト概要
- 個人向け家計簿Webアプリ（Django）
- 主機能: 収支登録/編集/削除、検索、統計、期間残高、各種チェック（実残高・確認日）
- ルーティングの主入口は `config/urls.py` -> `moneybook/urls.py`
- ビューは `moneybook/views/*.py` に機能分割されたクラスベースビュー
- ドメイン中心は `moneybook/models/data.py` の `Data` モデルで、検索・集計系メソッドが多い
- `moneybook/middleware/auth.py` に未ログイン時のAPI/画面遷移制御あり
- 環境設定は `config/settings/{common,dev,test,prod}.py` で分離
- 本番はMySQL、開発/テストはSQLiteが基本
