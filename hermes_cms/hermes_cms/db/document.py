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


class DocumentNotFound(Exception):
    pass


class Document(SQLObject):
    uuid = StringCol(length=36)  # this is the version record to be found in S3
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
    user_id = IntCol()

    def _get_url(self):
        return str(self._SO_get_url()).strip()

    def _get_name(self):
        return str(self._SO_get_name()).strip()

    def _get_type(self):
        return str(self._SO_get_type()).strip()

    @staticmethod
    def save(record):
        record['document']['uuid'] = str(uuid.uuid4())
        record['document']['created'] = arrow.utcnow()
        record['document']['parent'] = record['document'].get('parent') or 0
        record['document']['archived'] = record['document'].get('archived', False)

        document_data = {'url': None, 'path': None, 'parent': 0, 'type': None}
        if record.get('id'):
            document_data['id'] = record.get('id')

        document_data.update(record['document'])

        document = Document(**document_data)

        # ensure the path is always updated correctly.
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
    def _write(filename, contents):
        with open(filename, 'w+') as f:
            f.write(contents)

    @staticmethod
    def get_document(record):
        """
        Get the full document from S3

        @param record A `Document` database object
        @return A `dict` of the document
        """
        filename = '/tmp/data/{0}'.format(record.uuid)
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                contents = f.read().strip()
        else:
            key_name = "%s/%s/%s/%s" % (record.created.day, record.created.month,
                                        record.created.year, record.uuid)
            contents = S3.get_string(Registry().get('storage')['bucket_name'], key_name).strip()

            if not os.path.exists('/tmp/data'):
                os.makedirs('/tmp/data')

            Document._write(filename, contents)

        return json.loads(contents)

    @staticmethod
    def delete_document(doc_uuid):
        """
        Marks all documents to archived. No data is deleted.

        @param doc_uuid The uuid of the document to delete
        @return The Document database object
        """
        record = Document.selectBy(uuid=doc_uuid).getOne(None)

        # todo must do better exception handling
        if not record:
            raise Exception('Cannot find document')

        update = Update(Document.sqlmeta.table, values={'archived': True}, where=Document.q.id == record.id)
        Document._connection.query(Document._connection.sqlrepr(update))

        return record

    @staticmethod
    def restore_document(doc_uuid):
        """
        Marks all documents to restored.

        @param doc_uuid The uuid of the document to restore
        @return The Document database object
        """
        record = Document.selectBy(uuid=doc_uuid).getOne(None)

        if not record:
            raise Exception('Cannot find document')

        update = Update(Document.sqlmeta.table, values={'archived': False}, where=Document.q.id == record.id)
        Document._connection.query(Document._connection.sqlrepr(update))

        return record

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

        items = []
        for result in connection.queryAll(query):
            _id, select_results = result[0], result[1:]
            entry = Document.get(_id, selectResults=select_results)
            items.append(entry)

        return items

    @staticmethod
    def query_as_dict(fields, **kwargs):
        connection = Document._connection
        kwargs['staticTables'] = [Document.sqlmeta.table]
        kwargs['items'] = fields
        query = connection.sqlrepr(Select(**kwargs))
        cols = [field.fieldName for field in fields]

        items = []
        for result in connection.queryAll(query):
            items.append(dict(zip(cols, result)))

        return items
