# /usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import logging
import sys
import daemon.runner

from hermes_cms.core.registry import Registry
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

logger = logging.getLogger("DaemonLog")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("testdaemon.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

class ServiceRunner(object):

    def __init__(self, name, region, config_file):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/null'
        self.stderr_path = '/dev/null'
        self.pidfile_path = '/var/run/{0}.pid'.format(name)
        self.pidfile_timeout = 10

        self.name = name
        self.region = region
        self.config = Registry().get(config_file)

    def run(self):
        module_name = self.config['jobs'][self.name]['module_name']
        class_name = self.config['jobs'][self.name]['class_name']

        mod = __import__(module_name, fromlist=[class_name])
        service_class = getattr(mod, class_name)
        job_class = service_class(self.name, self.region, self.config)

        seconds = int(self.config['jobs'][self.name]['frequency'])

        scheduler = BlockingScheduler()
        scheduler.add_job(job_class.do_action, IntervalTrigger(seconds=seconds))
        scheduler.start()

        logger.warn('Daemon seemed to stop???')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['start', 'stop', 'restart'], help='Start service action')
    parser.add_argument('-j', '--job', required=True)
    parser.add_argument('-c', '--config', required=True)
    args = parser.parse_args()

    sys.argv = (sys.argv[0], args.action)

    service = ServiceRunner(args.job, Registry().get('region').get('region'), args.config)
    daemon_runner = daemon.runner.DaemonRunner(service)
    daemon_runner.daemon_context.detach_process = False
    daemon_runner.daemon_context.files_preserve = [handler.stream]

    try:
        daemon_runner.do_action()
    except Exception as e:
        print 'error', e


if __name__ == '__main__':
    sys.exit(main())
