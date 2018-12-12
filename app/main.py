import base64

from pyelucidate.pyelucidate import async_manifests_by_topic
from flask import Flask
from flask import request, jsonify, abort
from iiif import collection_gen, process_manifest
from logzero import logger
from flask_caching import Cache
from flask_cors import CORS
import settings
import logging
import sys


app = Flask(__name__)
CORS(app)
cache = Cache(app, config={"CACHE_TYPE": "filesystem", "CACHE_DIR": "./"})


def main():
    if __name__ == "__main__":
        logging.basicConfig(
            stream=sys.stdout,
            level=logging.DEBUG,
            format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
        )
        app.run(debug=True)


@app.route("/metadata", methods=["GET"])
def metadata():
    """
    return request URL for DLCS service checking.

    :return: json
    """
    logger.info("metadata request received")

    mdata = {
        "@context": "http://digirati.com/api/services/metadata.json",
        "@id": request.url,
        "@type": "digirati:ServiceMetadata",
    }

    return jsonify(mdata)


@app.route("/collection/<path:topic>", methods=["GET"])
@cache.cached(timeout=300)  # 20 second caching.
def default(topic: str):
    if "/" in topic:
        if not settings.TOPIC_BASE.endswith("/"):
            settings.TOPIC_BASE += "/"
        t = "".join([settings.TOPIC_BASE, topic])
    else:
        t = base64.b64decode(topic.encode("utf-8"))
    logger.info("Request received")
    manifests = [
        process_manifest(m)
        for m in (
            set(async_manifests_by_topic(topic=t, elucidate="https://elucidate.dlcs-ida.org/"))
        )
    ]
    collection = collection_gen(
        resources=manifests, topic_uri=str(t), uri=request.url, members=True
    )
    if collection:
        return jsonify(collection)
    else:
        abort(404)


if __name__ == "__main__":
    main()
