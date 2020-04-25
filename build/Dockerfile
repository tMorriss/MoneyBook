FROM centos:8
RUN dnf -y update && dnf -y upgrade
RUN dnf -y install python36 git mysql-devel gcc python36-devel nginx

COPY ./ /MoneyBook
RUN pip3 install -r /MoneyBook/build/requirements.txt

# nginx
RUN ln -s /MoneyBook/build/nginx.conf /etc/nginx/conf.d/default.conf
RUN nginx

WORKDIR /MoneyBook
CMD ["gunicorn", "--bind", "0.0.0.0:8081", "config.wsgi"]