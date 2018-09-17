import logging

import flask
import kubernetes
import ruamel.yaml
import requests

logger = logging.getLogger(__name__)

app = flask.Flask(__name__)
kubernetes.config.load_incluster_config()

api = kubernetes.client.BatchV1Api()
core = kubernetes.client.CoreV1Api()


def start_webconsole(uname):
    with open('job-template.yaml') as fo:
        job = ruamel.yaml.safe_load(fo)
    job['metadata'] = {
        'name': 'webconsole-{}'.format(uname),
    }
    job['spec']['template']['metadata'] = {
        'labels': {'uname': uname, 'managed-by': 'provisioner'}
    }

    try:
        api.create_namespaced_job(
            'default', job, pretty=True,
            _request_timeout=(15, 15),
        )
    except Exception as exc:
        logger.exception('Error starting webconsole')
        return str(exc)


@app.route('/api/<uname>/start/', methods=['POST'])
def start(uname):
    err = start_webconsole(uname)
    return flask.jsonify({'error': err})


@app.route('/api/<uname>/run/', methods=['POST'])
def run(uname):
    result = core.list_namespaced_pod('default', label_selector='uname={}'.format(uname), _request_timeout=(15, 15))
    ip = result.items[0].status.pod_ip
    return requests.post('http://{}:5000/run/'.format(ip), json=flask.request.get_json(), timeout=(15, 15)).content
