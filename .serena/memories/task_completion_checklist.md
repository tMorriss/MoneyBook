# タスク完了時チェック
1. 変更影響範囲（モデル/ビュー/テンプレート/静的ファイル）を確認
2. 関連する単体テストを実行（必要ならe2eも）
3. `tox -e lint` を実行し新規lint違反がないことを確認
4. モデル変更時は migration の有無を確認（`makemigrations`）
5. e2eテスト追加時は `.github/workflows/ci.yml` の matrix 更新
6. 新規Pythonパッケージには `__init__.py` を追加
7. push前に `master` 取り込み（`git fetch` + `git merge origin/master`）
8. PRタイトル/説明は変更全体を包含（本番影響なしなら `[skip ci]` を検討）
