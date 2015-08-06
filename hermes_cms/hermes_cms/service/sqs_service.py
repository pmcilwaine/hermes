# /usr/bin/env python
# -*- coding: utf-8 -*-
import boto.sqs
import logging
from hermes_cms.service.service import Service

log = logging.getLogger('hermes_cms.service.sqs_service')


class SQSNotExistError(Exception):
    pass


class SQSService(Service):

    def __init__(self, name, region, config):
        """

        :param name:
        :param region:
        :param config:
        :return:
        :raise: SQSNotExistError
        """
        super(SQSService, self).__init__(name, region, config)
        self._sqs_conn = boto.sqs.connect_to_region(self.region)

        queue_name = self._resolve.resolver(self.service_config['queue'])
        self.queue = self._sqs_conn.get_queue(queue_name)
        if not self.queue:
            raise SQSNotExistError('Queue "{0}" does not exist'.format(queue_name))

    def do_action(self):
        """

        :return:
        """
        messages = self.queue.get_messages(num_messages=self.service_config['messages'])
        for message in messages:
            log.info('Got message for job %s', self.name)
            try:
                self.job_class.do_work(message)
                self._sqs_conn.delete_message(self.queue, message)
            except Exception as e:
                log.exception(e)
