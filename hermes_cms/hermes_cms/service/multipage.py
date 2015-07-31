# /usr/bin/env python
# -*- coding: utf-8 -*-
import json
import zipfile
import logging
import mimetypes
from hermes_cms.service.job import Job, InvalidJobError, FatalJobError
from hermes_cms.db import Job as JobDB, Document
from hermes_cms.core.registry import Registry
from sqlobject import sqlhub, connectionForURI
from cStringIO import StringIO
import boto
from boto.s3.key import Key
from hermes_aws import S3
from hermes_cms.core.log import setup_logging

setup_logging()


class MultipageJob(Job):

    def __init__(self):
        self.registry = Registry()
        self.log = logging.getLogger('hermes_cms.service.multipage')
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
            self.log.error('Cannot find job %s', job_id)
            raise InvalidJobError('Invalid Job ID: {0}'.format(job_id))

        document = Document.selectBy(uuid=job.message['document']).getOne(None)
        if not document:
            raise FatalJobError('No Document Exists')

        record = Document.get_document(document)

        fp = StringIO(S3.get_string(self.registry.get('storage').get('bucket_name'), record['file']['key']))
        with zipfile.ZipFile(fp, 'r') as zip_handle:
            for name in zip_handle.namelist():
                key_name = '{0}/{1}'.format(document.uuid, name)
                key = Key(bucket=bucket, name=key_name)
                key.content_type = mimetypes.guess_type(name)[0]
                key.set_contents_from_string(zip_handle.read(name))
                self.log.info('Uploaded %s', key_name)