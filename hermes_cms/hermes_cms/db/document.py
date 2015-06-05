# /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import uuid
import json
import arrow
from sqlobject import SQLObject
from sqlobject.sqlbuilder import Select, Update
from hermes_cms.core.registry import Registry
from sqlobject.col import StringCol, DateTimeCol, BoolCol, IntCol
from hermes_aws.s3 import S3


class Document(SQLObject):
    uuid = StringCol()  # this is the version record to be found in S3
    url = StringCol()  # this is unique for URL for each GID.
    created = DateTimeCol()
    published = BoolCol(default=False)
    type = StringCol()  # The document type e.g. Page this is found in the Configuration Registry
    name = StringCol(default=None)  # the name of the document listed in the administration area
    archived = BoolCol(default=False)
    menutitle = StringCol(default=None)  # The title listed in the menu for the document
    show_in_menu = BoolCol(default=False)
    parent = IntCol()
    path = StringCol()  # Uses the gid as parentGID/currentGID etc.
    user = IntCol()

    @staticmethod
    def save(record):
        record['document']['uuid'] = str(uuid.uuid4())
        record['document']['created'] = arrow.utcnow()
        record['document']['parent'] = record['document'].get('parent') or 0
        record['document']['archived'] = record['document'].get('archived', False)

        document_data = {'url': None, 'path': None, 'parent': 0, 'type': None}
        document_data.update(record['document'])

        document = Document(**document_data)
        if not document.path:
            path = "%d/" % (document.id, )
            # todo this query is wrong, fix it.
            parent = Document.selectBy(id=record['document']['parent']).getOne(None)
            if parent:
                path = "%s%s" % (parent.path, path)

            record['document']['path'] = path
            document.set(path=path)

        # upload files
        record['document']['created'] = str(record['document']['created'])
        S3.upload_string(Registry().get('storage')['bucket_name'], record['document']['uuid'], json.dumps(record))

        return document

    @staticmethod
    def get_document(record):
        """

        :type record: Document
        :param record:
        :return:
        """
        if os.path.exists('/tmp/data/%s' % (record.uuid, )):
            with open('/tmp/data/%s' % (record.uuid, ), 'r') as f:
                contents = f.read().strip()
        else:
            key_name = "%s/%s/%s/%s" % (record.created.day, record.created.month,
                                        record.created.year, record.uuid)
            contents = S3.get_string(Registry().get('storage')['bucket_name'], key_name).strip()

            if not os.path.exists('/tmp/data'):
                os.makedirs('/tmp/data')

            with open('/tmp/data/%s' % (record.uuid, ), 'w+') as f:
                f.write(contents)

        return json.loads(contents)

    @staticmethod
    def delete_document(doc_uuid):
        record = Document.selectBy(uuid=doc_uuid).getOne(None)

        # todo must do better exception handling
        if not record:
            raise Exception('Cannot find document')

        update = Update(Document.sqlmeta.table, values={'archived': 1}, where=Document.q.url == record.url)
        print Document._connection.sqlrepr(update)
        Document._connection.query(Document._connection.sqlrepr(update))

    @staticmethod
    def all():
        fields = [Document.q.id]
        for col in Document.sqlmeta.columnList:
            fields.append(getattr(Document.q, col.name))

        return fields

    @staticmethod
    def query(fields, **kwargs):
        """

        :param fields:
        :param kwargs:
        :return:
        """
        connection = Document._connection
        kwargs['staticTables'] = [Document.sqlmeta.table]
        kwargs['items'] = fields
        query = connection.sqlrepr(Select(**kwargs))
        num_columns = len(fields)
        print query

        items = []
        for result in connection.queryAll(query):
            _id, select_results = result[0], result[1:num_columns]
            entry = Document.get(_id, selectResults=select_results)
            items.append(entry)

        return items
