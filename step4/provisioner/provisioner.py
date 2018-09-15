import logging
import os
import argparse

import kubernetes
import ruamel.yaml
from redis import Redis
from redis import exceptions as redis_exceptions

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

redis_hostname = os.getenv('REDIS_HOSTNAME', 'localhost')

redis = Redis(redis_hostname, socket_connect_timeout=5, socket_timeout=5)

kubernetes.config.load_incluster_config()

batch = kubernetes.client.BatchV1Api()
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
        batch.create_namespaced_job(
            'default', job, pretty=True,
            _request_timeout=(15, 15),
        )
    except Exception as exc:
        logger.exception('Error starting webconsole')
        return str(exc)


def provision():
    while True:
        try:
            item = redis.blpop('console_requests', timeout=10)
        except redis_exceptions.TimeoutError:
            continue
        logger.debug('item: %s', item)

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
            uname = event['object'].metadata.labels['uname']
            if event['type'].lower() == 'deleted':
                logger.info('webconsole %s finished', uname)
                redis.delete('webconsole-{}'.format(uname))
            else:
                ip = event['object'].status.pod_ip
                logger.info('webconsole %s ip: %s', uname, ip)
                redis.set('webconsole-{}'.format(uname), ip)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('worker', choices=('pod-monitor', 'job-monitor', 'provisioner'),
                        default='provisioner')
    args = parser.parse_args()
    if args.worker == 'pod-monitor':
        watch_pod_loop()
    elif args.worker == 'provisioner':
        provision()
