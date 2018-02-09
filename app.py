import os

from flask import Flask
from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch()

app = Flask(__name__)

import base64
import json

# Use str(base64.b64decode()) for py3k compatibility.
relationships = os.environ['PLATFORM_RELATIONSHIPS']
relationships = json.loads(str(base64.b64decode(relationships), 'utf-8'))

myes = relationships['elasticsearch'][0]

INDEX = "logs"

es = Elasticsearch(
    [myes['ip']],
    scheme="http",
    port=myes['port'],
)

@app.route('/')
def hello_world():
    log.info("Serving all env vars and relationships")
    lines = []
    log.info("Relationships = %s", repr(relationships))
    lines.append( "<tt>relationships={0}</tt>".format(repr(relationships)))
    for k, v in os.environ.items():
        log.info("Env %s = %s", k, v)
        lines.append( "<li>{0}={1}</li>".format(k, v) )
    doc = {
        'author': 'kimchy',
        'text': 'Elasticsearch: cool. bonsai cool.',
        'timestamp': datetime.now(),
    }
    res = es.index(index="test-index", doc_type='tweet', id=1, body=doc)
    res = es.get(index="test-index", doc_type='tweet', id=1)
    es.indices.refresh(index="test-index")
    res = es.search(index="test-index", body={"query": {"match_all": {}}})
    lines.append("Got %d Hits from Elastic Search:" % res['hits']['total'])
    for hit in res['hits']['hits']:
        lines.append("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
    return "\n".join(lines)
