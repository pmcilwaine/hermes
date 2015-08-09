# /usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys
import time
import daemon.runner
import logging
from boto.exception import S3ResponseError
from hermes_cms.core.log import setup_logging
from hermes_cms.core.registry import Registry
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger


class DaemonApplication(object):

    def __init__(self, name, region, config_file):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/null'
        self.stderr_path = '/dev/null'
        self.pidfile_path = '/tmp/{0}.pid'.format(name)
        self.pidfile_timeout = 5

        self.name = name
        self.region = region
        self.config_file = config_file

    def run(self):
        setup_logging()
        log = logging.getLogger('hermes_cms.service.runner')

        while True:
            try:
                config = Registry().get(self.config_file)
            except Exception as e:
                log.exception(e)

            module_name = config['jobs'][self.name]['module_name']
            class_name = config['jobs'][self.name]['class_name']

            mod = __import__(module_name, fromlist=[class_name])
            service_class = getattr(mod, class_name)

            job_class = service_class(self.name, self.region, config)

            seconds = int(config['jobs'][self.name]['frequency'])

            scheduler = BlockingScheduler()
            scheduler.add_job(job_class.do_action, IntervalTrigger(seconds=seconds))
            log.info('Starting Scheduled job %s', self.name)
            scheduler.start()


class ServiceRunner(daemon.runner.DaemonRunner):

    def __init__(self, app):
        self.app_save = app
        daemon.runner.DaemonRunner.__init__(self, app)
        self.daemon_context.detach_process = False

    def parse_args(self, argv=None):
        self.action = sys.argv[1]

        if not self.action:
            print 'Killing Service Runner'
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['start', 'stop', 'restart'], help='Start service action')
    parser.add_argument('-j', '--job', required=True)
    parser.add_argument('-c', '--config', required=True)
    args = parser.parse_args()

    sys.argv = (sys.argv[0], args.action)

    region = None
    while not region:
        try:
            region = Registry().get('region').get('region')
        except (TypeError, KeyError, S3ResponseError):
            time.sleep(5)

    app = DaemonApplication(args.job, region, args.config)
    daemon_runner = ServiceRunner(app)
    try:
        daemon_runner.do_action()
    except (daemon.runner.DaemonRunnerStartFailureError, daemon.runner.DaemonRunnerStopFailureError):
        pass

    return 0

if __name__ == '__main__':
    main()
