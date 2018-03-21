import base64

from elucidate import manifests_by_topic
from flask import Flask
from flask import request, jsonify, make_response, current_app, abort
from iiif import collection_gen, process_manifest
from logzero import logger
from flask_cache import Cache
from datetime import timedelta
from functools import update_wrapper


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    """
    Add CORS headers to Flask results.
    :param origin:
    :param methods:
    :param headers:
    :param max_age:
    :param attach_to_all:
    :param automatic_options:
    :return:
    """
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)

    return decorator


app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'filesystem', 'CACHE_DIR': './'})


def main():
    app.run(threaded=True, debug=True, port=5001, host='0.0.0.0')


@app.route('/metadata', methods=['GET'])
def metadata():

    logger.info("metadata request received")

    metadata = {
        "@context": "http://digirati.com/api/services/metadata.json",
        "@id": request.url,
        "@type": "digirati:ServiceMetadata"
    }

    return jsonify(metadata)


@app.route('/collection/<path:topic>', methods=['GET'])
@crossdomain(origin='*')  # add CORS
@cache.cached(timeout=300)  # 20 second caching.
def default(topic):
    t = base64.b64decode(topic.encode('utf-8'))
    logger.info("Request received")
    manifests = [process_manifest(m) for m in (set(manifests_by_topic(topic=t)))]
    collection = collection_gen(resources=manifests, topic_uri=str(t), uri=request.url,
                                members=True)
    if collection:
        return jsonify(collection)
    else:
        abort(404)


if __name__ == "__main__":
    main()
