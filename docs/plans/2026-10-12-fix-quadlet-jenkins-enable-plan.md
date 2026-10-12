# 計画: jenkins.shにおけるQuadletサービスのenableエラー修正

## 課題の概要
Jenkins上で `jenkins.sh` を実行した際、以下のエラーが発生してビルドが失敗する。
`Failed to enable unit: Unit /run/user/1000/systemd/generator/moneybook-pod.service is transient or generated.`

この原因は、Quadletが生成したsystemdユニットファイルに対して `systemctl --user enable` コマンドを実行しているためである。
systemdの仕様上、ジェネレータによって動的に生成されたユニット（generated unit）に対して明示的に `enable` を実行することは禁止されている。
Quadletではテンプレートファイル内の `[Install] WantedBy=default.target` により、`systemctl --user daemon-reload` 実行時に自動的に有効化される。

## 変更内容
1. `build/jenkins.sh` から不要な `systemctl --user enable` の実行行を削除する。
2. 作業計画ファイル `docs/plans/2026-10-12-fix-quadlet-jenkins-enable-plan.md` を追加する。
3. プレコミットの検証ステップを実施する。
4. 変更をコミット・送信する。

## 手順
1. `docs/plans/2026-10-12-fix-quadlet-jenkins-enable-plan.md` に計画ドキュメントを作成する。
2. `build/jenkins.sh` から `systemctl --user enable` を削除する。
3. プレコミット手順を実施し、検証および各種チェックを行う。
4. 変更内容を送信する。
