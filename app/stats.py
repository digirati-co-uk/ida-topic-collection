import requests
from tqdm import tqdm
import asyncio
from aiohttp import ClientSession, TCPConnector


async def fetch_all(urls):
    """Launch requests for all web pages."""
    tasks = []
    fetch.start_time = dict()  # dictionary of start times for each url
    async with ClientSession(connector=TCPConnector(limit=5)) as session:
        for url in urls:
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)  # create list of tasks
        results = await asyncio.gather(*tasks)  # gather task responses
        return results


async def fetch(url, session):
    """Fetch a url, using specified ClientSession."""
    async with session.get(url) as response:
        print('.')
        resp = await response.json()
        return resp


def items_async(manifests):
    loop = asyncio.get_event_loop()  # event loop
    future = asyncio.ensure_future(fetch_all([p for p in manifests]))  # tasks to do
    m_list = loop.run_until_complete(future)  # loop until done
    return m_list


def collection_size(collection):
    r = requests.get(collection)
    total = 0
    if r.status_code == requests.codes.ok:
        j = r.json()
        manifests = [x['@id'] for x in j['members']]
        m = items_async(manifests)
        for manifest in tqdm(m):
                canvas_count = len(manifest['sequences'][0]['canvases'])
                total += canvas_count
    return total


print('Rolls', collection_size('https://manifests.dlcs-ida.org/rollcollection'))
print('IDA', collection_size('https://manifests.dlcs-ida.org/refreshtop'))