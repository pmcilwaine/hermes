# /usr/bin/env python
# -*- coding: utf-8 -*-
import json
import boto
import arrow
import logging
from hermes_cms.core.log import setup_logging

setup_logging(logfile='service.ini')
log = logging.getLogger('hermes.service.migration_upload')

import zipfile
from boto.s3.key import Key
from cStringIO import StringIO
from hermes_cms.core.registry import Registry
from hermes_cms.db import Job as JobDB, Document
from hermes_cms.service.job import Job, InvalidJobError
from sqlobject import sqlhub, connectionForURI
from sqlobject.sqlbuilder import DESC
import mimetypes


class MigrationUploadJob(Job):

    def __init__(self):
        self.registry = Registry(log=log)
        database_url = str(self.registry.get('database').get('database'))
        sqlhub.processConnection = connectionForURI(database_url)

        conn = boto.connect_s3()
        file_conn = boto.connect_s3()

        self.bucket = conn.get_bucket(self.registry.get('storage').get('bucket_name'))
        self.files_bucket = file_conn.get_bucket(self.registry.get('files').get('bucket_name'))

    @staticmethod
    def _get_manifest(handle):
        """

        :type handle: zipfile.ZipFile
        :param handle:
        :return:
        :raises Exception
        """
        return json.loads(handle.read('manifest'))

    @staticmethod
    def _validate_manifest(documents):
        lookup = {}

        for document in documents:
            if not (document.get('parent_uuid') and document.get('parent_url')):
                lookup[document['uuid']] = document['url']
                continue

            if not lookup.get(document['parent_uuid']):
                parent_document = Document.selectBy(url=document['parent_url']).getOne(None)
                if not parent_document:
                    return False

                lookup[document['uuid']] = document['url']

        return True

    @staticmethod
    def _get_document_from_archive(uuid, handle):
        """

        :param uuid:
        :type handle: zipfile.ZipFile
        :param handle:
        :return:
        """
        return json.loads(handle.read(uuid))

    # pylint: disable=no-self-use
    def _update_from_parent(self, contents, parent_url):
        document = Document.selectBy(url=parent_url, orderBy=DESC(Document.q.created), limit=1).getOne(None)
        contents['document']['parent'] = document.id
        contents['document']['path'] = document.path

    # pylint: disable=no-self-use
    def _save_document(self, user_id, contents):
        """

        :param user_id:
        :param contents:
        :return:
        :rtype: arrow.Arrow
        """
        created = arrow.get(contents['document']['created'])
        contents['document']['created'] = created.datetime
        contents['document']['user_id'] = user_id
        document = Document(**contents['document'])

        path = '{0}{1}/'.format(document.path, document.id)
        contents['document']['created'] = str(created)
        contents['document']['path'] = path

        return created

    def _upload_file(self, contents, handle):
        """

        :param contents:
        :type handle: zipfile.ZipFile
        :param handle:
        :return:
        """
        bucket_name = self.registry.get('storage').get('bucket_name')
        filename = contents['file']['key']
        contents['bucket'] = bucket_name

        key = Key(self.bucket, filename)
        key.set_contents_from_string(handle.read('file/{0}'.format(filename)))

    def _upload_multipage(self, contents, handle):
        """

        :type contents: dict
        :param contents:
        :type handle: zipfile.ZipFile
        :param handle:
        :return:
        """
        for item in handle.namelist():
            part = 'files/{0}/'.format(contents['document']['uuid'])
            if item.startswith(part):
                filename = item.split(part).pop()
                key = Key(self.files_bucket, '{0}/{1}'.format(contents['document']['uuid'], filename))
                key.content_type = mimetypes.guess_type(item)[0]
                key.set_contents_from_string(handle.read(item))

    def do_work(self, message=None):
        """

        ZipFile stored in storage. read from Job Message

        {
            "archive": "path/in/s3"
        }

        # documents order matter

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

        :param message:
        :return:
        """
        if not message:
            return

        contents = json.loads(message.get_body())

        job_id = str(contents['Message'])
        job = JobDB.selectBy(uuid=job_id).getOne(None)
        if not job:
            log.error('Cannot find job %s', job_id)
            raise InvalidJobError('Invalid Job ID: {0}'.format(job_id))

        job.set(status='running')
        message = job.message

        # get archive file
        archive_key = self.bucket.get_key(job.message['file']['key'])
        if not archive_key:
            message['reason'] = 'Cannot find the archive in the S3 bucket.'
            job.set(status='failed', message=message)
            raise InvalidJobError('Cannot find archive in S3 bucket.')

        fp = StringIO(archive_key.get_contents_as_string())

        handle = zipfile.ZipFile(fp, mode='r', compression=zipfile.ZIP_DEFLATED)
        try:
            manifest_content = MigrationUploadJob._get_manifest(handle)
        except Exception:
            message['reason'] = 'Unable to retrieve manifest in archive'
            job.set(status='failed', message=message)
            raise InvalidJobError('Unable to retrieve manifest')

        if not MigrationUploadJob._validate_manifest(manifest_content['documents']):
            message['reason'] = 'Manifest found is not valid'
            job.set(status='failed', message=message)
            raise InvalidJobError('Manifest is not valid')

        for document in manifest_content['documents']:
            contents = MigrationUploadJob._get_document_from_archive(document['uuid'], handle)
            if document.get('parent_uuid') and document.get('parent_url'):
                self._update_from_parent(contents, document['parent_url'])

            created = self._save_document(job.message['user_id'], contents)
            if contents.get('file') and contents['document']['type'] == 'File':
                self._upload_file(contents, handle)
            elif contents.get('file') and contents['document']['type'] == 'MultiPage':
                self._upload_multipage(contents, handle)

            key_name = '{0}/{1}/{2}/{3}'.format(created.day, created.month, created.year, contents['document']['uuid'])
            key = Key(self.bucket, key_name)
            key.set_contents_from_string(json.dumps(contents))

        job.set(status='complete')
        log.info('Setting job=%s to complete', job_id)
