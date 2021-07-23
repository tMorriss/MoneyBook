# MoneyBook
自分用家計簿Webアプリケーション

## lint確認
```
$ flake8 . --count --ignore=E722,W503 --max-line-length=140 --exclude moneybook/migrations,__init__.py --show-source --statistics --import-order-style smarkets
```

## 単体テスト
[![codecov](https://codecov.io/gh/tMorriss/MoneyBook/branch/master/graph/badge.svg?token=E522OPRLRM)](https://codecov.io/gh/tMorriss/MoneyBook)
```
$ coverage run --source='moneybook.models,moneybook.views,moneybook.utils,moneybook.middleware,moneybook.forms' manage.py test moneybook.tests --settings config.settings.test
# レポートを表示
$ coverage report -m

# VSCodeでハイライト
$ coverage xml
# vscodeのコマンド
>code coverage: Toggle coverage display
```

## E2Eテスト
```
$ python manage.py test moneybook.selenium --settings config.settings.test
```

## E2Eテスト(docker centos)
```
$ docker run --rm -it -v /d/source/MoneyBook:/MoneyBook --name selenium -h selenium centos
$ cd /MoneyBook && dnf -y update && dnf -y upgrade && dnf -y install python38 mysql-devel gcc python38-devel && pip3 install -r build/requirements.txt && pip3 install -r build/requirements_selenium.txt && \
echo '[google-chrome]
name=google-chrome
baseurl=http://dl.google.com/linux/chrome/rpm/stable/$basearch
enabled=1
gpgcheck=1
gpgkey=https://dl-ssl.google.com/linux/linux_signing_key.pub' > /etc/yum.repos.d/google.chrome.repo && \
dnf install -y google-chrome-stable && \
num=`dnf list installed |grep google-chrome-stable |awk '{print $2}' |awk -F "[.]" '{print $1}'`
pip3 install chromedriver-binary==${num}.* && \
python3 manage.py test moneybook.selenium --settings config.settings.test
```

python3 manage.py test moneybook.selenium.add --settings config.settings.test
