FROM python:3-alpine

RUN apk add python3-dev build-base linux-headers pcre-dev uwsgi-python3

ENV TOPIC_BASE https://omeka.dlcs-ida.org/s/ida/page/topics/

WORKDIR /opt/app

COPY app /opt/app/

RUN pip install uwsgi
RUN pip install --no-cache-dir -r /opt/app/requirements.txt


CMD [ "uwsgi", "--http", "0.0.0.0:80", \
               "--protocol", "uwsgi", \
               "--enable-threads", \
               "--master", \
               "--http-timeout", "600", \
               "--lazy", \
               "--module", "main:app" ]