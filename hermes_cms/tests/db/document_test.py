# /usr/bin/env python
# -*- coding: utf-8 -*-
import boto
import json
import arrow
import pytest
from boto.s3.key import Key
from datetime import datetime
from moto import mock_s3
from mock import patch, MagicMock, mock_open
from hermes_cms.db import Document


@mock_s3
@patch('hermes_cms.db.document.Registry')
@patch('hermes_cms.db.document.arrow')
@patch('hermes_cms.db.document.Document')
def test_db_save_no_parent(document_mock, arrow_mock, registry_mock):
    conn_s3 = boto.connect_s3()
    conn_s3.create_bucket('storage-bucket')

    registry = MagicMock()
    registry.get.return_value = {'bucket_name': 'storage-bucket'}
    registry_mock.return_value = registry

    arrow_mock.utcnow.return_value = arrow.get('2015-01-01 00:00:00', 'YYYY-MM-DD HH:mm:ss')

    record = {
        'document': {
            'url': '/',
            'name': 'Document Name',
            'show_in_menu': True
        }
    }

    document = {
        'id': 1,
        'uuid': 'some-id',
        'url': '/',
        'name': 'Document Name',
        'show_in_menu': True,
        'path': None
    }

    document_mock.return_value = MagicMock(**document)

    result = Document.save(record)
    assert result.uuid == document['uuid']
    assert result.url == document['url']


@mock_s3
@patch('hermes_cms.db.document.os')
@patch('hermes_cms.db.document.Registry')
def test_get_document(registry_mock, os_mock):
    conn_s3 = boto.connect_s3()
    bucket = conn_s3.create_bucket('storage-bucket')
    key = Key(bucket=bucket, name='25/7/2015/some-id')
    key.set_contents_from_string(json.dumps({
        'document': {}
    }))

    registry = MagicMock()
    registry.get.return_value = {'bucket_name': 'storage-bucket'}
    registry_mock.return_value = registry

    def side_effect(value):
        return value == '/tmp/data'

    os_mock.path.exists = MagicMock(side_effect=side_effect)

    with patch.object(Document, '_write'):
        contents = Document.get_document(MagicMock(**{
            'uuid': 'some-id',
            'created': datetime(2015, 7, 25)
        }))

        assert {'document': {}} == contents


@patch('hermes_cms.db.document.Document')
def test_delete_document_exception(document_mock):
    document_mock.selectBy.return_value.getOne.return_value = None

    with pytest.raises(Exception):
        Document.delete_document('')
