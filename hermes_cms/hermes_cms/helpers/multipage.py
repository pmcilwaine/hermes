# /usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import boto.sns
from boto.exception import BotoServerError
from hermes_cms.core.registry import Registry
from hermes_cms.helpers import DocumentHelper
from hermes_cms.db import Job


log = logging.getLogger('hermes_cms.helpers.multipage')


class Multipage(DocumentHelper):

    def do_work(self):
        updated_record = {}
        alter_record = {}
        if self.document.published:
            alter_record.update({
                'published': True
            })
            updated_record.update({
                'published': False
            })
            log.debug('Document: %s removing published status', self.document.uuid)

        # create job
        name = '{0} multipage job'.format(self.document.name)
        job = Job.save({
            'name': name,
            'status': 'pending',
            'message': {
                'document': self.document.uuid,
                'on_complete': {
                    'alter': alter_record
                }
            }
        })

        log.info('Created Job for Document %s as JobID=%s', self.document.uuid, job.uuid)

        # push this to sns job topic
        topic_arn = Registry().get('topics').get('topic').get('multipage')
        conn = boto.sns.connect_to_region(Registry().get('region').get('region'))
        try:
            conn.publish(topic_arn, str(job.uuid), name)
        except BotoServerError as e:
            log.error('Cannot publish Job=%s to Topic=%s', job.uuid, topic_arn)
            log.exception(e)

        if updated_record:
            self.document.set(**updated_record)
