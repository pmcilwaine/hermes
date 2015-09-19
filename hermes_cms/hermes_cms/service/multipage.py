# /usr/bin/env python
# -*- coding: utf-8 -*-
import json
import zipfile
import mimetypes
import logging
from hermes_cms.core.log import setup_logging

setup_logging(logfile='service.ini')
log = logging.getLogger('hermes.service.multipage')

from hermes_cms.service.job import Job, InvalidJobError, FatalJobError
from hermes_cms.db import Job as JobDB, Document
from hermes_cms.core.registry import Registry
from sqlobject import sqlhub, connectionForURI
from cStringIO import StringIO
import boto
from boto.s3.key import Key
from hermes_aws import S3


class MultipageJob(Job):

    def __init__(self):
        self.registry = Registry(log=log)
        database_url = str(self.registry.get('database').get('database'))
        sqlhub.processConnection = connectionForURI(database_url)

    def do_work(self, message=None):
        """

        :type message: boto.sqs.message.Message | None
        :param message:
        :return:
        """

        if not message:
            return

        conn = boto.connect_s3()
        bucket = conn.get_bucket(self.registry.get('files').get('bucket_name'))
        contents = json.loads(message.get_body())

        job_id = str(contents['Message'])
        job = JobDB.selectBy(uuid=job_id).getOne(None)
        if not job:
            log.error('Cannot find job %s', job_id)
            raise InvalidJobError('Invalid Job ID: {0}'.format(job_id))

        job.set(status='running')

        document = Document.selectBy(uuid=job.message['document']).getOne(None)
        if not document:
            job.message['reason'] = 'No Document exists'
            job.set(status='failed', message=job.message)
            raise FatalJobError('No Document Exists')

        record = Document.get_document(document)

        fp = StringIO(S3.get_string(self.registry.get('storage').get('bucket_name'), record['file']['key']))
        with zipfile.ZipFile(fp, 'r') as zip_handle:
            for name in zip_handle.namelist():
                if name.endswith('/'):
                    continue
                key_name = '{0}/{1}'.format(document.uuid, name)
                key = Key(bucket=bucket, name=key_name)
                key.content_type = mimetypes.guess_type(name)[0]
                key.set_contents_from_string(zip_handle.read(name))
                log.info('Uploaded %s', key_name)

        job.set(status='complete')
        if job.message.get('on_complete', {}).get('alter'):
            document.set(**job.message['on_complete']['alter'])

        log.info('Setting job=%s to complete', job_id)
