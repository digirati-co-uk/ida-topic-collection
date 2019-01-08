FROM python:3-alpine

FROM python:3-alpine

RUN apk add python3-dev build-base linux-headers pcre-dev uwsgi-python3

ENV TOPIC_BASE https://omeka.dlcs-ida.org/s/ida/page/topics/
ENV ELUCIDATE https://elucidate.dlcs-ida.org

WORKDIR /opt/app

COPY app/requirements.txt /opt/app/
RUN pip install --upgrade pip
RUN pip install uwsgi
RUN pip install -r /opt/app/requirements.txt

COPY app /opt/app/
RUN chmod a+rwx /opt/app

CMD [ "uwsgi", "--http", ":5000", \
               "--uid", "uwsgi", \
               "--plugins", "http, python3", \
#               "--protocol", "uwsgi", \
               "--enable-threads", \
               "--master", \
               "--http-timeout", "600", \
               "--lazy", \
               "--module", "main:app" ]