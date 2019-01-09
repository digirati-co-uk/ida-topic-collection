FROM alpine:3.6

RUN apk add --update --no-cache --virtual=run-deps python3-dev build-base linux-headers pcre-dev uwsgi uwsgi-http uwsgi-python3

ENV TOPIC_BASE https://omeka.dlcs-ida.org/s/ida/page/topics/

WORKDIR /opt/app

COPY app /opt/app/

RUN pip3 install --no-cache-dir -r /opt/app/requirements.txt


CMD [ "uwsgi", "--plugins", "http,python3", \
               "--http", "0.0.0.0:80", \
               "--protocol", "uwsgi", \
               "--enable-threads", \
               "--master", \
               "--http-timeout", "600", \
               "--lazy", \
               "--module", "main:app" ]