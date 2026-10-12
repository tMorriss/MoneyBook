# Podman Quadlet 移行計画および作業記録

## 目的

Podman Pod を Podman Quadlet（systemd 管理）で運用するように移行し、ホスト再起動やコンテナ障害発生時に自動で再起動する構成を実現する。
あわせて、機密情報（DB接続パスワードやSECRET_KEY等）の安全な管理のために Podman Secrets を採用する。

## 現状

- `build/pod.yaml` に記載された Kubernetes 互換 YAML を元に、`jenkins.sh` から `podman play kube` を実行して Pod を起動している。
- `jenkins.sh` で毎回 `podman pod stop` / `podman pod rm` して再作成している。
- ホスト再起動時の自動起動設定（systemd 連携等）は未設定。
- 環境変数は `jenkins.sh` の `envsubst` で `pod.yaml` に埋め込まれて展開されていた。

## 方針・設計選定

1. **Quadlet 構成方式**:
   - Quadlet ネイティブ形式（`.pod` + `.container`）を採用する。
   - `build/quadlet/moneybook.pod.template`: Pod 定義およびポートマッピング（8081:80）。
   - `build/quadlet/moneybook-gunicorn.container.template`: Gunicorn コンテナ定義。`Pod=moneybook.pod`。
   - `build/quadlet/moneybook-nginx.container.template`: Nginx コンテナ定義。`Pod=moneybook.pod`。

2. **実行ユーザーと自動起動（Rootless + Linger）**:
   - セキュリティと既存構成との親和性を重視し、一般ユーザー（`$PODMAN_USER`）配下の Rootless Quadlet (`~/.config/containers/systemd/`) で運用する。
   - ホスト起動時にログインなしでユーザー systemd インスタンスおよび Pod が自動起動するよう、`loginctl enable-linger "$PODMAN_USER"` を有効化する。
   - コンテナ停止/障害時の再起動は、Quadlet ユニット内の `Restart=always`（`[Service]` セクション）で担保する。

3. **機密情報管理（Podman Secrets）**:
   - 機密情報（`DB_NAME`, `DB_USER`, `DB_PASS`, `DB_HOST`, `HOST_NAME`, `SECRET_KEY` 等）は、`jenkins.sh` 内で `podman secret create`（または更新）により Podman Secrets に登録する。
   - Gunicorn コンテナ定義にて `Secret=DB_PASS,type=env,target=DB_PASS` の形式で参照し、ファイルシステム上に平文の環境変数を残さない。
   - キャッシュ無効化のための動的イメージタグ（`STATIC_VERSION` / `BUILD_TAG`）は、デプロイ時に `envsubst` を用いてユニットファイルに展開する。

4. **デプロイスクリプト（`build/jenkins.sh`）の更新**:
   - 既存の `podman play kube` 処理を Quadlet のデプロイ処理へ置き換える。
   - Podman Secrets の設定/更新処理を追加。
   - テンプレートから Quadlet ユニットファイルを生成し、`~/.config/containers/systemd/` へ配置。
   - `loginctl enable-linger "$PODMAN_USER"` の実行確認。
   - `systemctl --user daemon-reload` および `systemctl --user restart moneybook-pod.service` により Quadlet サービスを起動・更新。

5. **ドキュメントの更新**:
   - `README.md` のデプロイ手順を Quadlet ベースの運用手順に書き換える。

## 受け入れ条件

- `build/quadlet/` 配下に `.template` 形式の Quadlet ユニットファイルが作成されている。
- `jenkins.sh` で Podman Secrets の登録、Quadlet ユニットファイルの配置、`systemctl --user daemon-reload`、`systemctl --user restart` が実行される。
- `loginctl enable-linger` によりホスト再起動時の自動起動が有効化される。
- `README.md` に Quadlet でのデプロイ手順および運用方法が明確に記載されている。
- `tox -e lint` および `tox -e unittest` が正常に通過する。

## 作業手順

1. `build/quadlet/` 配下に `.pod.template`, `moneybook-gunicorn.container.template`, `moneybook-nginx.container.template` を作成。
2. `build/jenkins.sh` を Quadlet + Podman Secrets 対応に書き換え。
3. `README.md` のデプロイセクションを更新。
4. 設定ファイルおよびスクリプトの検証、lint / テストの実行。
