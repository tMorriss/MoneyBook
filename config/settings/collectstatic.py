from django.core.management.utils import get_random_secret_key

from .common import *  # NOQA F403

# collectstatic専用の設定ファイル
# DBへの接続は不要のため、DATABASES設定は省略
DEBUG = False

# collectstaticの実行のみに使用するため、実行ごとにランダムなシークレットキーを生成
SECRET_KEY = get_random_secret_key()

ALLOWED_HOSTS = ['localhost']
