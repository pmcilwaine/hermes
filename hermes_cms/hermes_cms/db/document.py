# /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import uuid
import json
import arrow
from sqlobject import SQLObject
from hermes_cms.core.registry import Registry
from sqlobject.col import StringCol, DateTimeCol, BoolCol, IntCol
from hermes_aws.s3 import S3


class Document(SQLObject):
    gid = IntCol()  # the global document id, is the same across all versions
    url = StringCol()  # this is unique for URL for each GID.
    uid = StringCol()  # this is the version record to be found in S3
    path = StringCol()  # Uses the gid as parentGID/currentGID etc.
    parent = IntCol()
    created = DateTimeCol()
    published = BoolCol(default=False)
    archived = BoolCol(default=False)
    type = StringCol()  # The document type e.g. Page this is found in the Configuration Registry
    name = StringCol(default=None)  # the name of the document listed in the administration area
    menutitle = StringCol(default=None)  # The title listed in the menu for the document
    show_in_menu = BoolCol(default=False)

    @staticmethod
    def save(record):
        record['document']['uid'] = str(uuid.uuid4())
        record['document']['created'] = arrow.utcnow()
        record['document']['parent'] = record['document'].get('parent') or 0
        record['document']['gid'] = 1  # this is a hack, todo remove hack

        document_data = {'gid': None, 'url': None, 'path': None, 'parent': None, 'type': None}
        document_data.update(record['document'])

        document = Document(**document_data)
        if not document.path:
            path = "%d/" % (document.gid, )
            # todo this query is wrong, fix it.
            parent = Document.selectBy(uid=record['document']['uid']).getOne(None)
            if parent:
                path = "%s%s" % (parent.path, path)

            document.set(path=path)

        # upload files
        record['document']['created'] = str(record['document']['created'])
        S3.upload_string(Registry().get('storage')['bucket_name'], record['document']['uid'], json.dumps(record))

        return document

    @staticmethod
    def get_document(record):
        """

        :type record: Document
        :param record:
        :return:
        """
        if os.path.exists('/tmp/data/%s' % (record.uid, )):
            with open('/tmp/data/%s' % (record.uid, ), 'r') as f:
                contents = f.read().strip()
        else:
            key_name = "%s/%s/%s/%s" % (record.created.day, record.created.month,
                                        record.created.year, record.uid)
            contents = S3.get_string(Registry().get('storage')['bucket_name'], key_name).strip()

            with open('/tmp/data/%s' % (record.uid, ), 'w+') as f:
                f.write(contents)

        return json.loads(contents)
