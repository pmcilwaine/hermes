# /usr/bin/env python
# -*- coding: utf-8 -*-
import json
import boto
import logging
import zipfile
from boto.s3.key import Key
from cStringIO import StringIO
from hermes_cms.core.registry import Registry
from hermes_cms.db import Job as JobDB, Document
from sqlobject import sqlhub, connectionForURI
from sqlobject.sqlbuilder import LIKE, IN, AND
from hermes_cms.service.job import Job, InvalidJobError
from hermes_cms.core.log import setup_logging

setup_logging()


class MigrationDownloadJob(Job):

    def __init__(self):
        self.registry = Registry()
        self.log = logging.getLogger('hermes_cms.service.migration_download')
        database_url = str(self.registry.get('database').get('database'))
        sqlhub.processConnection = connectionForURI(database_url)

        conn = boto.connect_s3()
        file_conn = boto.connect_s3()

        self.bucket = conn.get_bucket(self.registry.get('storage').get('bucket_name'))
        self.files_bucket = file_conn.get_bucket(self.registry.get('files').get('bucket_name'))

    def _get_document_query(self, documents):
        uuids = []
        for item in documents:
            document = Document.selectBy(uuid=item['parent_id']).getOne(None)
            for doc in Document.select(LIKE(Document.q.path, '{0}%'.format(document.path))):
                uuids.append(doc.uuid)

        return IN(Document.q.uuid, uuids)

    def _handle_document(self, document, zip_handle):
        """

        :type document: hermes_cms.db.document.Document
        :param document:
        :type zip_handle: zipfile.ZipFile
        :param zip_handle:
        :return:
        """
        key_name = '{0}/{1}/{2}/{3}'.format(document.created.day, document.created.month,
                                            document.created.year, document.uuid)

        contents = self.bucket.get_key(key_name).get_contents_as_string()
        json_content = json.loads(contents)
        zip_handle.writestr(document.uuid, contents)

        if 'file' in json_content:
            file_contents = self.bucket.get_key(json_content['file']['key']).get_contents_as_string()
            zip_handle.writestr(json_content['file']['key'], file_contents)

        if 'MultiPage' == document.type:
            for item in self.files_bucket.list(document.uuid):
                zip_handle.writestr('files/{0}'.format(item.name), item.get_contents_as_string())

    def _get_document_parent_url(self, parent):
        document = Document.selectBy(id=parent).getOne(None)
        if not document:
            return ''

        return document.url

    def do_work(self, message=None):
        """

        {
            "documents": [{
                "parent_id": "uuid"
            }],
            "all_documents": false
        }

        {
            "documents": [],
            "all_documents": true
        }

        uuid as filename
        {
            "document": {},
            "file": {},
        }

        full key name for file

        Manifest
        {
            "uuid": "/parent/url"
        }

        :type message: boto.sqs.message.Message | None
        :param message:
        :return:
        """

        if not message:
            return

        contents = json.loads(message.get_body())

        job_id = str(contents['Message'])
        job = JobDB.selectBy(uuid=job_id).getOne(None)
        if not job:
            self.log.error('Cannot find job %s', job_id)
            raise InvalidJobError('Invalid Job ID: {0}'.format(job_id))

        job.set(status='running')

        and_ops = [Document.q.archived == False, Document.q.published == True]
        if not job.message.get('all_documents'):
            and_ops.append(self._get_document_query(job.message.get('documents')))

        manifest = {
            'documents': {},
            'full_list': job.message.get('all_documents', False)
        }

        zip_contents = StringIO()
        zip_handle = zipfile.ZipFile(zip_contents, 'w', compression=zipfile.ZIP_DEFLATED)
        for document in Document.query(Document.all(), where=AND(*and_ops)):
            manifest['documents'].update({document.uuid: self._get_document_parent_url(document.parent)})
            self._handle_document(document, zip_handle)
            self.log.info('Adding document uuid=%s to zip archive', str(document.uuid))

        zip_handle.writestr('manifest', json.dumps(manifest))
        zip_handle.close()

        zip_key = Key(self.bucket, job_id)
        zip_key.content_type = 'application/zip'
        zip_key.set_contents_from_string(zip_contents.getvalue())
        self.log.info("Created ZIP for Job '%s'", str(job_id))

        job.set(status='complete')
