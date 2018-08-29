import logging
import os

import flask
import ruamel.yaml
import requests
from redis import Redis

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = flask.Flask(__name__)
settings = os.getenv('SETTINGS', None)
app.config.update({
    'REDIS': 'localhost',
})
if settings:
    with open(settings) as fo:
        app.config.update(ruamel.yaml.safe_load(fo))

redis = Redis(app.config['REDIS'], socket_connect_timeout=5, socket_timeout=5)


def start_webconsole(uname):
    redis.rpush('console_requests', uname.encode('utf-8'))


@app.route('/api/start/<uname>/', methods=['POST'])
def start(uname):
    start_webconsole(uname)
    return flask.jsonify({})


@app.route('/api/<uname>/run/', methods=['POST'])
def run(uname):
    ip = redis.get('webconsole-{}'.format(uname))
    return requests.post('http://{}:5000/run/'.format(ip), json=flask.request.get_json(), timeout=(15, 15)).content
