FROM python:3.9

WORKDIR /opt/app-root/src

ADD . /opt/app-root/src

RUN pip install -r requirements.txt

CMD gunicorn wsgi -k --bind 0.0.0.0:8080 stocks.wsgi:application