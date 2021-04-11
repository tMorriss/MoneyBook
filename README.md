# MoneyBook
自分用家計簿Webアプリケーション

## lint確認
```
$ flake8 . --count --ignore=E722,W503 --max-line-length=120 --exclude moneybook/migrations,__init__.py --show-source --statistics --import-order-style smarkets
```

## テスト方法
```
$ coverage run --source='moneybook.models,moneybook.views,moneybook.utils,moneybook.middleware,moneybook.forms' manage.py test moneybook.tests --settings config.settings.test
# レポートを表示
$ coverage report -m

# VSCodeでハイライト
$ coverage xml
# vscodeのコマンド
>code coverage: Toggle coverage display
```
