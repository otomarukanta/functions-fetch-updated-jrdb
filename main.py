import os
from google.cloud import pubsub_v1
from jrdb.client import JRDBClient
from jrdb import urlcodec


def main(data, context):
    auth = (os.environ['JRDB_ID'], os.environ['JRDB_PW'])
    jrdbclient = JRDBClient(auth)
    urls = jrdbclient.fetch_latest_urls()

    print(urls)
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path('otomarukanta-a', 'jrdb-urls')
    publisher.publish(topic_path, urlcodec.encode(urls))
