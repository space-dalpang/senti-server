FROM ubuntu:14.04
ENV DEBIAN_FRONTEND noninteractive

RUN sudo sed -i 's/archive.ubuntu.com/ftp.daumkakao.com/g' /etc/apt/sources.list
RUN apt-get update && apt-get -y install \
        nginx \
        sed \
        python3-pip \
        python3-dev \
        uwsgi-plugin-python3 \
        python3-psycopg2 \
        libpq-dev \
        curl \
        g++\
        openjdk-7-jdk \
        supervisor && \
    apt-get clean && rm -rf /var/cache/apt/* && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/log/nginx/app
RUN mkdir -p /var/log/uwsgi/app
RUN mkdir -p /var/log/supervisor

RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh)"

RUN rm /etc/nginx/sites-enabled/default
RUN ln -s /etc/nginx/sites-available/flask.conf /etc/nginx/sites-enabled/flask.conf
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

COPY data/flask/requirements.txt /var/www/flask/requirements.txt
RUN pip3 install -r /var/www/flask/requirements.txt

EXPOSE 80
EXPOSE 443

CMD ["/usr/bin/supervisord"]
