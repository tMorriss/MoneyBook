FROM python:3
ADD requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
WORKDIR /MoneyBook
CMD ["gunicorn", "--bind", "0.0.0.0:80", "config.wsgi"]