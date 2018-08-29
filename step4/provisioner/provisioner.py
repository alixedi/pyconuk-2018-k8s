import logging
import os
import threading

import kubernetes
import ruamel.yaml
from redis import Redis

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

settings = os.getenv('SETTINGS', None)
config = {
    'REDIS': 'localhost',
}
if settings:
    with open(settings) as fo:
        config.update(ruamel.yaml.safe_load(fo))

logger.debug('config: %s', config)
redis = Redis(config['REDIS'], socket_connect_timeout=5, socket_timeout=5)

kubernetes.config.load_incluster_config()

api = kubernetes.client.BatchV1Api()
core = kubernetes.client.CoreV1Api()


def start_webconsole(uname):
    logger.info('Starting webconsole %s', uname)
    with open('job-template.yaml') as fo:
        job = ruamel.yaml.safe_load(fo)
    job['metadata'] = {
        'name': 'webconsole-{}'.format(uname),
        'labels': {'uname': uname, 'managed-by': 'provisioner'}
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


def create_loop():
    while True:
        item = redis.blpop('console_requests', timeout=10)
        logger.debug('item: %s', item)
        if not item:
            continue

        queue, uname = item
        uname = uname.decode('utf-8')

        if redis.get('webconsole-{}'.format(uname)):
            logger.debug('Skipping %s, already running', uname)
            continue

        start_webconsole(uname)


def watch_pod_loop():
    w = kubernetes.watch.Watch()
    while True:
        for event in w.stream(
                core.list_namespaced_pod, 'default',
                label_selector='managed-by=provisioner',
                timeout_seconds=14,  # timeout before the read exception
                _request_timeout=(5, 15),
        ):
            uname = event['object'].metadata.labels.uname
            if event['type'].lower() == 'deleted':
                logger.info('webconsole %s finished', uname)
                redis.delete('webconsole-{}'.format(uname))
            else:
                ip = event['object'].status.pod_ip
                logger.info('webconsole %s ip: %s', uname, ip)
                redis.set('webconsole-{}'.format(uname), ip)


loops = [threading.Thread(target=create_loop), threading.Thread(target=watch_pod_loop)]

for loop in loops:
    loop.start()

for loop in loops:
    loop.join()
