import requests
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse, quote_plus, parse_qs
import asyncio
from aiohttp import ClientSession, TCPConnector


async def fetch_all(urls):
    """Launch requests for all web pages."""
    tasks = []
    fetch.start_time = dict() # dictionary of start times for each url
    async with ClientSession(connector=TCPConnector(limit=5)) as session:
        for url in urls:
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task) # create list of tasks
        results = await asyncio.gather(*tasks) # gather task responses
        return results


async def fetch(url, session):
    """Fetch a url, using specified ClientSession."""
    async with session.get(url) as response:
        resp = await response.json()
        return resp


def set_query_field(url, field, value, replace=False):
    # Parse out the different parts of the URL.
    components = urlparse(url)
    query_pairs = parse_qsl(urlparse(url).query)

    if replace:
        query_pairs = [(f, v) for (f, v) in query_pairs if f != field]
    query_pairs.append((field, value))

    new_query_str = urlencode(query_pairs)

    # Finally, construct the new URL
    new_components = (
        components.scheme,
        components.netloc,
        components.path,
        components.params,
        new_query_str,
        components.fragment
    )
    return urlunparse(new_components)


def annotation_pages(result):
    if result['total'] > 0:
        last = urlparse(result['last'])
        last_page = parse_qs(last.query)['page'][0]
        for p in range(0, int(last_page) + 1):
            page = set_query_field(result['last'], field='page', value=p, replace=True)
            yield page
    else:
        return


def items_by_topic_async(elucidate, topic):
    t = quote_plus(topic)
    sample_uri = elucidate + 'annotation/w3c/services/search/body?fields=source&value=' + t
    print(sample_uri)
    r = requests.get(sample_uri)
    if r.status_code == requests.codes.ok:
        loop = asyncio.get_event_loop()  # event loop
        future = asyncio.ensure_future(fetch_all([p for p in annotation_pages(r.json())]))  # tasks to do
        pages = loop.run_until_complete(future)  # loop until done
        for page in pages:
            for item in page['items']:
                yield item


def items_by_topic(elucidate, topic):
    t = quote_plus(topic)
    sample_uri = elucidate + 'annotation/w3c/services/search/body?fields=source&value=' + t
    print(sample_uri)
    r = requests.get(sample_uri)
    if r.status_code == requests.codes.ok:
        for page in annotation_pages(r.json()):
            items = requests.get(page).json()['items']
            for item in items:
                yield item


def manifest_from_annotation(content):
    if isinstance(content['target'], str):
        # hack that derives the manifest URI from the canvas URI
        manifest = content['target'].split('canvas')[0] + 'manifest'
    else:
        try:
            if isinstance(content['target']['dcterms:isPartOf'], str):
                manifest = content['target']['dcterms:isPartOf']
            else:
                manifest = content['target']['dcterms:isPartOf']['id']
        except TypeError:
            manifest = content['target'][0]['dcterms:isPartOf']['id']
        except KeyError:
            # annotations with no dcterms:isPartOf
            manifest = content['target']['source']
    return manifest


def manifests_by_topic(elucidate='https://elucidate.dlcs-ida.org/', topic=None):
    if topic:
        for count, anno in enumerate(items_by_topic(elucidate, topic)):
            m = manifest_from_annotation(anno)
            if m:
                yield m


def manifests_by_topic_async(elucidate='https://elucidate.dlcs-ida.org/', topic=None):
    if topic:
        return [manifest_from_annotation(anno) for anno in items_by_topic_async(elucidate, topic)]


for x in manifests_by_topic_async(elucidate='https://elucidate.dlcs-ida.org/',
                            topic='https://omeka.dlcs-ida.org/s/ida/page/topics/virtual:norp/indian'):
    print(x)