# /usr/bin/env python
# -*- coding: utf-8 -*-
import json
import boto
import arrow
import logging
import zipfile
from boto.s3.key import Key
from cStringIO import StringIO
from hermes_cms.core.registry import Registry
from hermes_cms.db import Job as JobDB, Document
from hermes_cms.service.job import Job, InvalidJobError
from sqlobject import sqlhub, connectionForURI
from sqlobject.sqlbuilder import DESC
from hermes_cms.core.log import setup_logging
setup_logging()


class MigrationUploadJob(Job):

    def __init__(self):
        self.registry = Registry()
        self.log = logging.getLogger('hermes_cms.service.migration_upload')
        database_url = str(self.registry.get('database').get('database'))
        sqlhub.processConnection = connectionForURI(database_url)

        conn = boto.connect_s3()
        self.bucket = conn.get_bucket(self.registry.get('storage').get('bucket_name'))

    def _get_manifest(self, handle):
        """

        :type handle: zipfile.ZipFile
        :param handle:
        :return:
        :raises Exception
        """
        return json.loads(handle.read('manifest'))

    def _validate_manifest(self, documents):
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

    def _get_document_from_archive(self, uuid, handle):
        """

        :param uuid:
        :type handle: zipfile.ZipFile
        :param handle:
        :return:
        """
        return json.loads(handle.read(uuid))

    def _update_from_parent(self, contents, parent_url):
        document = Document.selectBy(url=parent_url, orderBy=DESC(Document.q.created), limit=1).getOne(None)
        contents['document']['parent'] = document.id
        contents['document']['path'] = document.path

    def _save_document(self, user_id, contents):
        created = arrow.get(contents['document']['created'])
        contents['document']['created'] = created.datetime
        contents['document']['user'] = user_id
        document = Document(**contents['document'])

        path = '{0}{1}/'.format(document.path, document.id)
        contents['document']['created'] = str(created)
        contents['document']['path'] = path

        key_name = '{0}/{1}/{2}/{3}'.format(created.day, created.month, created.year, contents['document']['uuid'])
        key = Key(self.bucket, key_name)
        key.set_contents_from_string(json.dumps(contents))

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
            print 'invalid job'
            self.log.error('Cannot find job %s', job_id)
            raise InvalidJobError('Invalid Job ID: {0}'.format(job_id))

        # get archive file
        archive_key = self.bucket.get_key(job.message['archive'])
        if not archive_key:
            raise InvalidJobError('Cannot find archive in S3 bucket.')

        fp = StringIO(archive_key.get_contents_as_string())

        handle = zipfile.ZipFile(fp, mode='r', compression=zipfile.ZIP_DEFLATED)
        try:
            manifest_content = self._get_manifest(handle)
        except Exception:
            raise InvalidJobError('Some error occurred')  # todo probably need to push some exception stuff elsewhere

        #if not self._validate_manifest(manifest_content['documents']):
        #    raise Exception('Invalid manifest')

        for document in manifest_content['documents']:
            contents = self._get_document_from_archive(document['uuid'], handle)
            if document.get('parent_uuid') and document.get('parent_url'):
                self._update_from_parent(contents, document['parent_url'])

            self._save_document(job.message['user_id'], contents)
            if contents.get('file'):
                pass
