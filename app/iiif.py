from collections import OrderedDict
import json
import requests
from typing import Tuple, Optional, Any


def json_get(iiif_uri: str) -> Tuple[int, Optional[Any]]:
    """
    Return an OrderedDict from a URI which returns JSON.

    :param iiif_uri: ID/URI for the JSON
    :return: html status code, OrderedDict
    """
    r = requests.get(iiif_uri)
    if r.status_code == requests.codes.ok:
        od = json.loads(r.text, object_pairs_hook=OrderedDict)
        return r.status_code, od
    else:
        return r.status_code, None


def process_manifest(manifest_uri: str, get: bool=False) -> Optional[dict]:
    """
    Get label from a manifest, where the target of a
    bookmarking annotation is of type manifest.

    1) Retrieve a manifest based on the target id
    2) Parse returned JSON-LD
    3) Generate a simple OrderedDict to go in the Collection

    :param manifest_uri: manifest id
    :param get: boolean, if False, return empty label and don't dereference the manifest @id
    :return: Ordered Dict with manifest @id, label, and @type
    """
    label = "-"
    id = manifest_uri
    if manifest_uri:
        if get:
            _, m_json = json_get(manifest_uri)
            label = m_json.get("label")
            id = m_json.get("@id")
        m_dict = OrderedDict()
        m_dict['@id'] = id
        m_dict['@type'] = 'sc:Manifest'
        m_dict['label'] = label
        return m_dict
    else:
        return


def collection_gen(resources: list, topic_uri: str, uri: str, members: bool=False) -> Optional[Any]:
    """
    Generate an OrderedDict for a IIIF Presentation API collection from
    a list of manifest Ordered Dicts (with @type, @id, and label),
    setting the @id of the Collection based on the annotation 'creator'.

    :param resources: List of IIIF Presentation API Ordered Dicts
    :param topic_uri: id of the topic
    :param uri: base URI where the collection can be retrieved
    :param members: Boolean to set whether to use members or manifests. Members
    would allow Collections to be part of the Collection.

    :return: OrderedDict for IIIF Collection
    """
    if resources and topic_uri and uri:
        at_id = uri  # + 'topic/?topic=' + topic_uri
        coll = OrderedDict()
        coll['@context'] = 'http://iiif.io/api/presentation/2/context.json'
        coll['@id'] = at_id
        coll['@type'] = 'sc:Collection'
        coll['label'] = ' '.join(['IDA Topic Collection for', topic_uri.split('/')[-1]])
        if members:
            coll['members'] = [r for r in resources]
        else:
            coll['manifests'] = [r for r in resources]
        return coll
    else:
        return None
