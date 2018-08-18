import os
import requests
import zlib
from lxml import html
from urllib.parse import urljoin
from google.cloud import pubsub_v1


def main(data, context):
    URL = 'http://www.jrdb.com/member/data/'
    auth = (os.environ['JRDB_ID'], os.environ['JRDB_PW'])
    session = requests.Session()
    session.auth = auth
    res = session.get(URL)
    page = html.fromstring(res.content)
    urls = ','.join([urljoin(URL, x)
                    for x in page.xpath('//a/@href') if x.endswith('zip')])
    print(f"Extracted urls: {urls}")

    compressed_urls = zlib.compress(urls.encode('utf-8'))
    print(f"Compressed urls: {compressed_urls}")

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path('otomarukanta-a', 'jrdb-urls')
    publisher.publish(topic_path, compressed_urls)
