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
        conn = boto.connect_sqs()
        self.queue = conn.get_queue(self.service_config['queue'])
        if not self.queue:
            raise SQSNotExistError('Queue does not exist')

    def do_action(self):
        """

        :return:
        """
        messages = self.queue.get_messages(num_messages=self.service_config['messages'])
        self.job_class.do_work(messages)
