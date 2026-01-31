FROM quay.io/centos/centos:stream8
RUN dnf -y update && dnf -y upgrade
RUN dnf -y install python38 git mysql-devel gcc python38-devel nginx

COPY ./ /MoneyBook
RUN pip3 install -r /MoneyBook/build/requirements.txt

# nginx
RUN ln -s /MoneyBook/build/nginx.conf /etc/nginx/conf.d/default.conf

WORKDIR /MoneyBook
CMD ["/bin/bash", "/MoneyBook/build/start.sh"]
