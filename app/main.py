import base64
from pyelucidate.pyelucidate import async_manifests_by_topic
from flask import Flask
from flask import request, jsonify, abort
from iiif import collection_gen, process_manifest
from logzero import logger
from flask_caching import Cache
import settings
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
cache = Cache(app, config={"CACHE_TYPE": "filesystem", "CACHE_DIR": "./"})


def main():
    app.run(threaded=True, debug=True, port=5001, host="0.0.0.0")


@app.route("/metadata", methods=["GET"])
def metadata():

    logger.info("metadata request received")

    metadata = {
        "@context": "http://digirati.com/api/services/metadata.json",
        "@id": request.url,
        "@type": "digirati:ServiceMetadata",
    }

    return jsonify(metadata)


@app.route("/collection/<path:topic>", methods=["GET"])
@cache.cached(timeout=300)  # 5 minutes caching
def default(topic):
    if "/" in topic:
        if not settings.TOPIC_BASE.endswith("/"):
            settings.TOPIC_BASE += "/"
        t = "".join([settings.TOPIC_BASE, topic])
    else:
        t = base64.b64decode(topic.encode("utf-8"))
    logger.info("Request received")
    manifests = [
        process_manifest(m)
        for m in async_manifests_by_topic(topic=t, elucidate=settings.ELUCIDATE)
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
