# IDA Topic Collection Service

## Introduction

This service accepts an IDA topic, for example:

`tribe/jemez`

From a URL formatted like:

`https://collections.dlcs-ida.org/collection/tribe/jemez`

And returns a IIIF collection, with one member per manifest.

The service uses PyElucidate's [async_manifests_by_topic](https://pyelucidate.readthedocs.io/en/latest/pyelucidate.html#pyelucidate.pyelucidate.async_manifests_by_topic) function
to return a list of all manifests any of whom's canvases are tagged with a particular topic.

## Installation

The service provides a `Dockerfile` which uses uWSGI to run a Flask app to provide the topic collection service.


```bash
docker build -t topic-collection .
docker run -p 3000:80 topic-collection:latest
```

The shell script above will spin up the service on port 3000.


## Contribution Guidelines

ida-topic-collection has been tested using Python 3.5+. 

Feel free to raise Github issues. 

If you find an issue you are interested in fixing you can:


* Fork the repository
* Clone the repository to your local machine
* Create a new branch for your fix using `git checkout -b branch-name-here`.
* Fix the issue.
* Commit and push the code to your remote repository.
* Submit a pull request to the `ida-topic-collection` repository, with a description of your fix and the issue number.
* The PR will be reviewed by the maintainer [https://github.com/mattmcgrattan](https://github.com/mattmcgrattan) and either merge the PR or response with comments.

Thanks!

## License

MIT License

Copyright (c) Digirati 2018

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.





