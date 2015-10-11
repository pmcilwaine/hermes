# /usr/bin/env python
# -*- coding: utf-8 -*-
import json
import boto
import logging
from hermes_cms.core.log import setup_logging

setup_logging(logfile='service.ini')
log = logging.getLogger('hermes.service.migration_download')

import zipfile
from boto.s3.key import Key
from cStringIO import StringIO
from hermes_cms.core.registry import Registry
from hermes_cms.db import Job as JobDB, Document
from sqlobject import sqlhub, connectionForURI
from sqlobject.sqlbuilder import LIKE, IN, AND, DESC
from hermes_cms.service.job import Job, InvalidJobError


class MigrationDownloadJob(Job):

    def __init__(self):
        self.registry = Registry(log=log)
        database_url = str(self.registry.get('database').get('database'))
        sqlhub.processConnection = connectionForURI(database_url)

        self.bucket = None
        self.files_bucket = None

    # pylint: disable=no-self-use
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

        if 'file' in json_content and document.type == 'File':
            file_contents = self.bucket.get_key(json_content['file']['key']).get_contents_as_string()
            zip_handle.writestr(json_content['file']['key'], file_contents)

        if 'MultiPage' == document.type:
            for item in self.files_bucket.list(document.uuid):
                zip_handle.writestr('files/{0}'.format(item.name), item.get_contents_as_string())

    # pylint: disable=no-self-use
    def _get_document_parent_url(self, parent):
        """

        :param parent:
        :return:
        :rtype: hermes_cms.db.document.Document | None
        """
        if not parent:
            return None

        return Document.select(Document.q.id == parent, orderBy=DESC(Document.q.created), limit=1).getOne(None)

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

        Manifest file structure
        {
            'documents': [
                {
                    'uuid': 'some-uuid',
                    'url': 'some-url',
                    'parent_url': 'some-parent-url',
                    'parent_uuid': 'some-parent-uuid'
                },
                ...
            ],
            'full': bool
        }

        :type message: boto.sqs.message.Message | None
        :param message:
        :return:
        """

        if not message:
            return

        conn = boto.connect_s3()
        file_conn = boto.connect_s3()

        self.bucket = conn.get_bucket(self.registry.get('storage').get('bucket_name'))
        self.files_bucket = file_conn.get_bucket(self.registry.get('files').get('bucket_name'))

        contents = json.loads(message.get_body())

        job_id = str(contents['Message'])
        job = JobDB.selectBy(uuid=job_id).getOne(None)
        if not job:
            log.error('Cannot find job %s', job_id)
            raise InvalidJobError('Invalid Job ID: {0}'.format(job_id))

        job.set(status='running')

        and_ops = [Document.q.archived == False, Document.q.published == True]
        if not job.message.get('all_documents'):
            and_ops.append(self._get_document_query(job.message.get('document')))

        manifest = {
            'documents': [],
            'full': job.message.get('all_documents', False)
        }

        zip_contents = StringIO()
        zip_handle = zipfile.ZipFile(zip_contents, 'w', compression=zipfile.ZIP_DEFLATED)
        for document in Document.query(Document.all(), where=AND(*and_ops)):
            parent_document = self._get_document_parent_url(document.parent)
            manifest['documents'].append({
                'uuid': document.uuid,
                'url': document.url,
                'parent_url': None if not parent_document else parent_document.url,
                'parent_uuid': None if not parent_document else parent_document.uuid
            })

            self._handle_document(document, zip_handle)
            log.info('Adding document uuid=%s to zip archive', str(document.uuid))

        zip_handle.writestr('manifest', json.dumps(manifest))
        zip_handle.close()

        zip_key = Key(self.bucket, job_id)
        zip_key.content_type = 'application/zip'
        zip_key.set_contents_from_string(zip_contents.getvalue())
        log.info("Created ZIP for Job '%s'", str(job_id))

        message = job.message
        message['download'] = {
            'bucket': self.bucket.name,
            'key': job_id
        }
        job.set(status='complete', message=message)
        log.info('Setting job=%s to complete', job_id)
