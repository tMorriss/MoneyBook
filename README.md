# MoneyBook
自分用家計簿Webアプリケーション

## テスト方法
```
coverage run --source='moneybook.models,moneybook.views' manage.py test moneybook --settings config.settings.test
# レポートを表示
$ coverage report -m

# VSCodeでハイライト
$ coverage xml
# vscodeのコマンド
>code coverage: Toggle coverage display
```
