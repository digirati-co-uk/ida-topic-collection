# IDA Topic Collection Service

## Introduction

This service accepts an IDA topic, for example:

`tribe/jemez`

From a URL formatted like:

`https://collections.dlcs-ida.org/collection/tribe/jemez`

And returns a IIIF collection, with one member per manifest.

The service uses PyElucidate's [async_manifests_by_topic](https://pyelucidate.readthedocs.io/en/latest/pyelucidate.html#pyelucidate.pyelucidate.async_manifests_by_topic) function
to return a list of all manifests any of whom's canvases are tagged with a particular topic.

## Deploy

The service provides a `Dockerfile` which uses uWSGI to run a Flask app to provide the topic collection service.


```bash
docker build -t topic-collection .
docker run -p 3000:80 topic-collection:latest
```

The shell script above will spin up the service on port 3000.







