@echo off

cd %~dp0

docker run -v C:\Users\tMorriss\source\MoneyBook:/MoneyBook -p 8000:8000 --rm -it python:latest /bin/bash -c 'pip3 install -r /MoneyBook/build/requirements.txt && python3 /MoneyBook/manage.py makemigrations && python3 /MoneyBook/manage.py migrate && python3 /MoneyBook/manage.py runserver'
