import logging
import os

import flask
import requests
from redis import Redis

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = flask.Flask(__name__)
redis_hostname = os.getenv('REDIS_HOSTNAME', 'localhost')

redis = Redis(redis_hostname, socket_connect_timeout=5, socket_timeout=5)


def start_webconsole(uname):
    redis.rpush('console_requests', uname.encode('utf-8'))


@app.route('/api/<uname>/start/', methods=['POST'])
def start(uname):
    start_webconsole(uname)
    return flask.jsonify({})


@app.route('/api/<uname>/run/', methods=['POST'])
def run(uname):
    ip = redis.get('webconsole-{}'.format(uname)).decode('utf-8')
    return requests.post('http://{}:5000/run/'.format(ip), json=flask.request.get_json(), timeout=(15, 15)).content
