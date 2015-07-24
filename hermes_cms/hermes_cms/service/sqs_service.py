# /usr/bin/env python
# -*- coding: utf-8 -*-
import boto.sqs
from hermes_cms.service.service import Service


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
        self.job_class.do_work(messages)
